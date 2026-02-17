"""
core.py
Point d'entrée UNIQUE pour la validation de TOUS les fichiers DayZ
Détecte automatiquement le type de fichier et applique le bon validateur
"""

from typing import Dict, Optional, List
from .detector import DayZFileDetector


class ValidationResult:
    """Résultat de validation unifié"""
    
    def __init__(self):
        self.valid = True
        self.file_type = None
        self.format = None
        self.confidence = 0.0
        self.errors = []
        self.warnings = []
        self.info = []
        self.metadata = {}
    
    def to_dict(self) -> Dict:
        """Convertit en dictionnaire"""
        return {
            'valid': self.valid,
            'file_type': self.file_type,
            'format': self.format,
            'confidence': self.confidence,
            'num_errors': len(self.errors),
            'num_warnings': len(self.warnings),
            'num_info': len(self.info),
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info,
            'metadata': self.metadata
        }
    
    def get_summary(self) -> str:
        """Résumé textuel"""
        if self.valid:
            return f"✅ Fichier {self.file_type} valide ({self.num_warnings} avertissements)"
        else:
            return f"❌ {len(self.errors)} erreur(s) dans {self.file_type}"


class DayZValidator:
    """
    Validateur universel pour TOUS les fichiers DayZ
    
    Usage:
        validator = DayZValidator()
        result = validator.validate(content, filename)
        
        if result.valid:
            print("Fichier valide !")
        else:
            for error in result.errors:
                print(error)
    """
    
    def __init__(self, version: str = '1.28'):
        """
        Initialise le validateur
        
        Args:
            version: Version DayZ par défaut (ex: '1.28')
        """
        self.version = version
        self.detector = DayZFileDetector()
        self._validators_cache = {}  # Cache des validateurs instanciés
    
    def validate(self, content: str, filename: Optional[str] = None) -> ValidationResult:
        """
        Valide n'importe quel fichier DayZ
        
        Args:
            content: Contenu du fichier (string)
            filename: Nom du fichier (optionnel, aide à la détection)
        
        Returns:
            ValidationResult: Résultat complet de validation
        """
        result = ValidationResult()
        
        # ========================================
        # ÉTAPE 1 : DÉTECTION DU TYPE DE FICHIER
        # ========================================
        detection = self.detector.detect(content, filename)
        
        result.format = detection['format']
        result.file_type = detection['file_type']
        result.confidence = detection['confidence']
        result.metadata['detection'] = detection
        
        # Vérifier la confiance de détection
        if detection['confidence'] < 0.5:
            result.valid = False
            result.errors.append({
                'severity': 'error',
                'message': f"Impossible de détecter le type de fichier DayZ (confiance: {detection['confidence']:.0%})",
                'suggestion': "Vérifiez que c'est bien un fichier DayZ valide",
                'context': f"Format détecté: {detection['format']}, Type: {detection['file_type']}"
            })
            return result
        
        if detection['confidence'] < 0.8:
            result.warnings.append({
                'severity': 'warning',
                'message': f"Détection incertaine du type de fichier (confiance: {detection['confidence']:.0%})",
                'suggestion': "La validation pourrait être imprécise"
            })
        
        # Si type inconnu
        if not detection['file_type']:
            result.valid = False
            result.errors.append({
                'severity': 'error',
                'message': f"Type de fichier DayZ inconnu ({detection['format']} valide mais non supporté)",
                'suggestion': f"Types supportés: {', '.join(self.get_supported_files()['xml'] + self.get_supported_files()['json'])}"
            })
            return result
        
        # ========================================
        # ÉTAPE 2 : CHARGER LE VALIDATEUR APPROPRIÉ
        # ========================================
        validator = self._get_validator(detection['file_type'], detection['format'])
        
        if not validator:
            result.valid = False
            result.errors.append({
                'severity': 'error',
                'message': f"Type de fichier '{detection['file_type']}' détecté mais validateur non implémenté",
                'suggestion': f"Le support pour {detection['file_type']} sera ajouté prochainement"
            })
            return result
        
        # ========================================
        # ÉTAPE 3 : VALIDER LE FICHIER
        # ========================================
        validation_errors = validator.validate(content)
        
        # Organiser les erreurs par sévérité
        for error in validation_errors:
            error_dict = error.to_dict()
            
            if error.severity == 'error':
                result.errors.append(error_dict)
                result.valid = False
            elif error.severity == 'warning':
                result.warnings.append(error_dict)
            elif error.severity == 'info':
                result.info.append(error_dict)
        
        # ========================================
        # ÉTAPE 4 : MÉTADONNÉES ADDITIONNELLES
        # ========================================
        result.metadata['validator'] = validator.__class__.__name__
        result.metadata['version'] = self.version
        
        return result
    
    def _get_validator(self, file_type: str, format: str):
        """
        Charge le validateur approprié pour le type de fichier
        
        Args:
            file_type: Type de fichier (ex: 'types', 'cfggameplay')
            format: Format (ex: 'xml', 'json')
        
        Returns:
            Instance du validateur ou None si non disponible
        """
        cache_key = f"{format}_{file_type}"
        
        # Vérifier le cache
        if cache_key in self._validators_cache:
            return self._validators_cache[cache_key]
        
        # Charger selon le format
        validator = None
        
        if format == 'xml':
            validator = self._load_xml_validator(file_type)
        elif format == 'json':
            validator = self._load_json_validator(file_type)
        
        # Mettre en cache
        if validator:
            self._validators_cache[cache_key] = validator
        
        return validator
    
    def _load_xml_validator(self, file_type: str):
        """Charge un validateur XML"""
        try:
            if file_type == 'types':
                from .validators.xml_validators.types_validator import TypesValidator
                return TypesValidator(version=self.version)
            
            elif file_type == 'events':
                from .validators.xml_validators.events_validator import EventsValidator
                return EventsValidator(version=self.version)
            
            elif file_type == 'globals':
                from .validators.xml_validators.globals_validator import GlobalsValidator
                return GlobalsValidator(version=self.version)
            
            elif file_type == 'economy':
                from .validators.xml_validators.economy_validator import EconomyValidator
                return EconomyValidator(version=self.version)
            
            elif file_type == 'messages':
                from .validators.xml_validators.messages_validator import MessagesValidator
                return MessagesValidator(version=self.version)
            
            elif file_type == 'spawnable_types':
                from .validators.xml_validators.spawnable_types_validator import SpawnableTypesValidator
                return SpawnableTypesValidator(version=self.version)
            
            elif file_type == 'zombie_territories':
                from .validators.xml_validators.zombie_territories_validator import ZombieTerritoriesValidator
                return ZombieTerritoriesValidator(version=self.version)
            
            # Ajouter les autres validateurs XML au fur et à mesure...
            
        except ImportError as e:
            print(f"⚠️ Validateur XML '{file_type}' non disponible: {e}")
            return None
        
        return None
    
    def _load_json_validator(self, file_type: str):
        """Charge un validateur JSON"""
        try:
            if file_type == 'cfggameplay':
                from .validators.json_validators.cfggameplay_validator import CfgGameplayValidator
                return CfgGameplayValidator(version=self.version)
            
            elif file_type == 'cfgeffectarea':
                from .validators.json_validators.cfgeffectarea_validator import CfgEffectAreaValidator
                return CfgEffectAreaValidator(version=self.version)
            
            elif file_type == 'cfgeventspawns':
                from .validators.json_validators.cfgeventspawns_validator import CfgEventSpawnsValidator
                return CfgEventSpawnsValidator(version=self.version)
            
            # Ajouter les autres validateurs JSON au fur et à mesure...
            
        except ImportError as e:
            print(f"⚠️ Validateur JSON '{file_type}' non disponible: {e}")
            return None
        
        return None
    
    def get_supported_files(self) -> Dict[str, List[str]]:
        """
        Retourne la liste de tous les types de fichiers supportés
        
        Returns:
            dict: {'xml': [...], 'json': [...]}
        """
        return self.detector.get_supported_files()
    
    def get_file_info(self, file_type: str) -> Optional[Dict]:
        """
        Retourne les informations sur un type de fichier
        
        Args:
            file_type: Type de fichier (ex: 'types', 'cfggameplay')
        
        Returns:
            dict: Informations sur le fichier ou None
        """
        return self.detector.get_file_info(file_type)
    
    def clear_cache(self):
        """Vide le cache des validateurs"""
        self._validators_cache.clear()


# ========================================
# INSTANCE GLOBALE POUR FACILITER L'IMPORT
# ========================================
# Usage simple:
#   from modules.validator import validator
#   result = validator.validate(content, filename)

validator = DayZValidator()
