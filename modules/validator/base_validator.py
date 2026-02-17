"""
base_validator.py
Classe de base abstraite pour tous les validateurs DayZ
Définit l'interface commune et les méthodes utilitaires
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import json
import os


class ValidationError:
    """Représente une erreur de validation"""
    
    def __init__(self, severity: str, message: str, line: Optional[int] = None, 
                 column: Optional[int] = None, field: Optional[str] = None,
                 suggestion: Optional[str] = None, context: Optional[str] = None):
        self.severity = severity  # 'error', 'warning', 'info'
        self.message = message
        self.line = line
        self.column = column
        self.field = field
        self.suggestion = suggestion
        self.context = context
    
    def to_dict(self) -> Dict:
        """Convertit en dictionnaire"""
        return {
            'severity': self.severity,
            'message': self.message,
            'line': self.line,
            'column': self.column,
            'field': self.field,
            'suggestion': self.suggestion,
            'context': self.context
        }
    
    def __repr__(self):
        location = f"L{self.line}" if self.line else "?"
        return f"[{self.severity.upper()}] {location}: {self.message}"


class BaseValidator(ABC):
    """Classe de base abstraite pour tous les validateurs DayZ"""
    
    def __init__(self, file_type: str, version: str = '1.28'):
        """
        Initialise le validateur
        
        Args:
            file_type: Type de fichier (ex: 'types', 'events', 'globals')
            version: Version DayZ (ex: '1.28')
        """
        self.file_type = file_type
        self.version = version
        self.schema = self.load_schema()
        self.errors: List[ValidationError] = []
    
    def load_schema(self) -> Optional[Dict]:
        """
        Charge le schéma de validation JSON pour ce type de fichier
        
        Returns:
            dict: Schéma de validation ou None si non trouvé
        """
        # Chemin vers le schéma
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        schema_path = os.path.join(base_path, f"schemas/dayz_{self.version}/{self.file_type}.json")
        
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Schéma non disponible, continuer sans
            return None
        except json.JSONDecodeError as e:
            print(f"⚠️ Erreur lecture schéma {schema_path}: {e}")
            return None
    
    def validate(self, content: str) -> List[ValidationError]:
        """
        Validation complète du fichier
        
        Args:
            content: Contenu du fichier à valider
        
        Returns:
            list: Liste d'erreurs de validation
        """
        self.errors = []
        
        # 1. Validation syntaxe (XML ou JSON)
        self.errors.extend(self.validate_syntax(content))
        
        # Si erreur de syntaxe, arrêter (impossible de valider la structure)
        if any(e.severity == 'error' for e in self.errors):
            return self.errors
        
        # 2. Validation structure
        self.errors.extend(self.validate_structure(content))
        
        # 3. Validation business rules
        self.errors.extend(self.validate_business_rules(content))
        
        # 4. Validation custom (sous-classes peuvent override)
        self.errors.extend(self.validate_custom(content))
        
        return self.errors
    
    @abstractmethod
    def validate_syntax(self, content: str) -> List[ValidationError]:
        """
        Valide la syntaxe du fichier (XML ou JSON)
        DOIT être implémenté par les sous-classes
        
        Args:
            content: Contenu du fichier
        
        Returns:
            list: Erreurs de syntaxe
        """
        pass
    
    @abstractmethod
    def validate_structure(self, content: str) -> List[ValidationError]:
        """
        Valide la structure du fichier (éléments requis, types, etc.)
        DOIT être implémenté par les sous-classes
        
        Args:
            content: Contenu du fichier
        
        Returns:
            list: Erreurs de structure
        """
        pass
    
    @abstractmethod
    def validate_business_rules(self, content: str) -> List[ValidationError]:
        """
        Valide les règles métier DayZ (min ≤ nominal, etc.)
        DOIT être implémenté par les sous-classes
        
        Args:
            content: Contenu du fichier
        
        Returns:
            list: Erreurs de règles métier
        """
        pass
    
    def validate_custom(self, content: str) -> List[ValidationError]:
        """
        Validation custom optionnelle (override si nécessaire)
        
        Args:
            content: Contenu du fichier
        
        Returns:
            list: Erreurs custom
        """
        return []
    
    def add_error(self, severity: str, message: str, **kwargs):
        """Ajoute une erreur à la liste"""
        error = ValidationError(severity, message, **kwargs)
        self.errors.append(error)
    
    def get_errors(self, severity: Optional[str] = None) -> List[ValidationError]:
        """
        Retourne les erreurs, optionnellement filtrées par sévérité
        
        Args:
            severity: 'error', 'warning', 'info' ou None pour toutes
        
        Returns:
            list: Erreurs filtrées
        """
        if severity:
            return [e for e in self.errors if e.severity == severity]
        return self.errors
    
    def has_errors(self) -> bool:
        """Retourne True s'il y a au moins une erreur (severity='error')"""
        return any(e.severity == 'error' for e in self.errors)
    
    def get_summary(self) -> Dict:
        """
        Retourne un résumé de la validation
        
        Returns:
            dict: {
                'valid': bool,
                'num_errors': int,
                'num_warnings': int,
                'num_info': int,
                'errors': list
            }
        """
        return {
            'valid': not self.has_errors(),
            'num_errors': len([e for e in self.errors if e.severity == 'error']),
            'num_warnings': len([e for e in self.errors if e.severity == 'warning']),
            'num_info': len([e for e in self.errors if e.severity == 'info']),
            'errors': [e.to_dict() for e in self.errors]
        }
    
    # ==============================
    # MÉTHODES UTILITAIRES
    # ==============================
    
    def safe_int(self, value: str, default: int = 0) -> int:
        """Convertit une string en int de manière sûre"""
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    def safe_float(self, value: str, default: float = 0.0) -> float:
        """Convertit une string en float de manière sûre"""
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def is_in_range(self, value: int, min_val: int, max_val: int) -> bool:
        """Vérifie si une valeur est dans un range"""
        return min_val <= value <= max_val
    
    def validate_enum(self, value: str, allowed_values: List[str]) -> bool:
        """Vérifie si une valeur fait partie d'une énumération"""
        return value in allowed_values
