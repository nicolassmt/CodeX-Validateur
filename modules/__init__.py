"""
Wrapper de compatibilité
Permet d'utiliser l'ancien code SANS modification
"""

from .validator.core import validator as new_validator


def validate(content, filetype=None):
    """
    Ancienne interface - COMPATIBILITÉ TOTALE
    
    Args:
        content: Contenu du fichier
        filetype: Type (ignoré, détection auto maintenant)
    
    Returns:
        dict: Résultat au format ancien
    """
    # Utiliser le nouveau validateur
    result = new_validator.validate(content)
    
    # Convertir au format ancien
    return {
        'valid': result.valid,
        'file_type': result.file_type,
        'errors': result.errors,
        'warnings': result.warnings,
        'num_errors': len(result.errors),
        'num_warnings': len(result.warnings)
    }


# Export pour compatibilité
__all__ = ['validate']
