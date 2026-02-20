"""
core.py - VERSION FUSIONNÉE ULTIME
Combine la puissance du nouveau système avec la pédagogie de l'ancien
Point d'entrée UNIQUE pour la validation de TOUS les fichiers DayZ
"""

from typing import Dict, Optional, List
from .detector import DayZFileDetector
import xml.etree.ElementTree as ET
import json


class ValidationResult:
    """Résultat de validation unifié - VERSION AMÉLIORÉE"""
    
    def __init__(self):
        self.valid = True
        self.file_type = None
        self.format = None
        self.confidence = 0.0
        self.errors = []
        self.warnings = []
        self.info = []
        self.metadata = {}
        
        # ✨ NOUVEAU : Support ancien système
        self.formatted_content = None
        self.corrected_content = None
        self.applied_corrections = []
        self.real_error_line = None
        self.pedagogy = None  # Messages pédagogiques de errors_matcher
    
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
            'metadata': self.metadata,
            'formatted': self.formatted_content,
            'corrected': self.corrected_content,
            'applied_corrections': self.applied_corrections,
            'pedagogy': self.pedagogy
        }
    
    def get_summary(self) -> str:
        """Résumé textuel"""
        if self.valid:
            return f"✅ Fichier {self.file_type} valide ({len(self.warnings)} avertissements)"
        else:
            return f"❌ {len(self.errors)} erreur(s) dans {self.file_type}"


class DayZValidator:
    """
    Validateur universel FUSIONNÉ pour TOUS les fichiers DayZ
    Combine détection smart + validation sémantique + pédagogie
    """
    
    def __init__(self, version: str = '1.28'):
        self.version = version
        self.detector = DayZFileDetector()
        self._validators_cache = {}
        
        # ✨ Charger les modules de l'ancien système
        self._load_legacy_modules()
    
    def _load_legacy_modules(self):
        """Charge les modules pédagogiques de l'ancien système"""
        try:
            # Import relatif depuis le dossier parent
            import sys
            from pathlib import Path
            parent_path = Path(__file__).parent.parent
            if str(parent_path) not in sys.path:
                sys.path.insert(0, str(parent_path))
            
            from modules import errors_matcher, corrector, locator
            self.errors_matcher = errors_matcher
            self.corrector = corrector
            self.locator = locator
        except ImportError as e:
            print(f"⚠️ Modules pédagogiques non disponibles: {e}")
            self.errors_matcher = None
            self.corrector = None
            self.locator = None
    
    def validate(self, content: str, filename: Optional[str] = None) -> ValidationResult:
        """
        Valide n'importe quel fichier DayZ - VERSION FUSIONNÉE
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
        
        # ========================================
        # ÉTAPE 2 : VALIDATION SYNTAXIQUE
        # ========================================
        if detection['format'] == 'xml':
            self._validate_xml_syntax(content, result)
        elif detection['format'] == 'json':
            self._validate_json_syntax(content, result)
        else:
            result.valid = False
            result.errors.append({
                'severity': 'error',
                'message': 'Format de fichier non supporté',
                'suggestion': 'Seuls XML et JSON sont supportés'
            })
            return result
        
        # Si erreur de syntaxe, on s'arrête là
        if not result.valid:
            return result
        
        # ========================================
        # ÉTAPE 3 : FORMATAGE
        # ========================================
        if detection['format'] == 'xml':
            result.formatted_content = self._format_xml(content)
        elif detection['format'] == 'json':
            try:
                data = json.loads(content)
                result.formatted_content = json.dumps(data, indent=2, ensure_ascii=False)
            except:
                result.formatted_content = content
        
        # ========================================
        # ÉTAPE 4 : VALIDATION SÉMANTIQUE (nouveau système)
        # ========================================
        if detection['file_type']:
            validator = self._get_validator(detection['file_type'], detection['format'])
            
            if validator:
                semantic_errors = validator.validate(content)
                
                for error in semantic_errors:
                    error_dict = error.to_dict()
                    
                    if error.severity == 'error':
                        result.errors.append(error_dict)
                        result.valid = False
                    elif error.severity == 'warning':
                        result.warnings.append(error_dict)
                    elif error.severity == 'info':
                        result.info.append(error_dict)
                
                result.metadata['validator'] = validator.__class__.__name__
        
        result.metadata['version'] = self.version
        
        return result
    
    def _validate_xml_syntax(self, content: str, result: ValidationResult):
        """Valide la syntaxe XML avec pédagogie"""
        try:
            ET.fromstring(content)
            result.valid = True
        except ET.ParseError as e:
            result.valid = False
            line, col = e.position
            
            # ✨ PÉDAGOGIE : Matcher l'erreur
            matched_error = None
            if self.errors_matcher:
                matched_error = self.errors_matcher.match_error(content, e, "xml")
            
            # ✨ LOCALISATION : Trouver la vraie ligne
            real_line = line
            if self.locator:
                location = self.locator.locate_real_error(content, line)
                real_line = location['real_line']
                result.real_error_line = location
            
            # Construire l'erreur enrichie
            error_dict = {
                'severity': 'error',
                'line': real_line,
                'column': col,
                'message': str(e)
            }
            
            if matched_error:
                error_dict['pedagogy'] = {
                    'title': matched_error.get('title', ''),
                    'explanation': matched_error.get('message_novice', ''),
                    'solution': matched_error.get('solution', ''),
                    'example_before': matched_error.get('example_before', ''),
                    'example_after': matched_error.get('example_after', '')
                }
                result.pedagogy = matched_error
                
                # ✨ AUTO-CORRECTION si possible
                if self.corrector and self.corrector.can_auto_correct(matched_error):
                    correction = self.corrector.auto_correct(content, "xml")
                    if correction['has_changes']:
                        result.corrected_content = correction['corrected']
                        result.applied_corrections = correction['applied_corrections']
            
            result.errors.append(error_dict)
    
    def _validate_json_syntax(self, content: str, result: ValidationResult):
        """Valide la syntaxe JSON avec pédagogie"""
        try:
            json.loads(content)
            result.valid = True
        except json.JSONDecodeError as e:
            result.valid = False
            
            # ✨ PÉDAGOGIE : Matcher l'erreur
            matched_error = None
            if self.errors_matcher:
                matched_error = self.errors_matcher.match_error(content, e, "json")
            
            # Construire l'erreur enrichie
            error_dict = {
                'severity': 'error',
                'line': e.lineno,
                'column': e.colno,
                'message': e.msg
            }
            
            if matched_error:
                error_dict['pedagogy'] = {
                    'title': matched_error.get('title', ''),
                    'explanation': matched_error.get('message_novice', ''),
                    'solution': matched_error.get('solution', ''),
                    'example_before': matched_error.get('example_before', ''),
                    'example_after': matched_error.get('example_after', '')
                }
                result.pedagogy = matched_error
                
                # ✨ AUTO-CORRECTION si possible
                if self.corrector and self.corrector.can_auto_correct(matched_error):
                    correction = self.corrector.auto_correct(content, "json")
                    if correction['has_changes']:
                        result.corrected_content = correction['corrected']
                        result.applied_corrections = correction['applied_corrections']
            
            result.errors.append(error_dict)
    
    def _get_validator(self, file_type: str, format: str):
        """Charge le validateur approprié"""
        cache_key = f"{format}_{file_type}"
        
        if cache_key in self._validators_cache:
            return self._validators_cache[cache_key]
        
        validator = None
        
        if format == 'xml':
            validator = self._load_xml_validator(file_type)
        elif format == 'json':
            validator = self._load_json_validator(file_type)
        
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
            
        except ImportError as e:
            print(f"⚠️ Validateur JSON '{file_type}' non disponible: {e}")
            return None
        
        return None
    
    def _format_xml(self, content: str) -> str:
        """Formate du XML avec indentation propre"""
        try:
            from xml.dom import minidom
            pretty = minidom.parseString(content).toprettyxml(indent="    ")
            lines = [line for line in pretty.split("\n") if line.strip()]
            return "\n".join(lines)
        except:
            return content
    
    def get_supported_files(self) -> Dict[str, List[str]]:
        """Retourne la liste de tous les types de fichiers supportés"""
        return self.detector.get_supported_files()
    
    def get_file_info(self, file_type: str) -> Optional[Dict]:
        """Retourne les informations sur un type de fichier"""
        return self.detector.get_file_info(file_type)
    
    def clear_cache(self):
        """Vide le cache des validateurs"""
        self._validators_cache.clear()


# ========================================
# INSTANCE GLOBALE POUR FACILITER L'IMPORT
# ========================================
validator = DayZValidator()
