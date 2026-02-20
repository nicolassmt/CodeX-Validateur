"""
Module Validator - Point d'entrée
Validation automatique de TOUS les fichiers DayZ
"""

from .core import DayZValidator, ValidationResult, validator
from .detector import DayZFileDetector

# Export pour faciliter les imports
__all__ = [
    'DayZValidator',
    'ValidationResult', 
    'validator',
    'DayZFileDetector'
]

# Fonction validate pour compatibilité avec l'ancienne API
def validate(content: str, filename: str = None):
    """
    Fonction de validation simple (compatible ancienne API)
    
    Args:
        content: Contenu du fichier
        filename: Nom du fichier (optionnel)
    
    Returns:
        ValidationResult: Résultat de validation
    """
    return validator.validate(content, filename)
