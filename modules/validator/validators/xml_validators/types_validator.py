"""
types_validator.py
Validateur spécifique pour types.xml
Gère la validation du système de loot spawns DayZ
"""

import xml.etree.ElementTree as ET
from typing import List
from ..base_validator import BaseValidator, ValidationError


class TypesValidator(BaseValidator):
    """Validateur pour types.xml - Configuration des spawns de loot"""
    
    # Champs requis dans chaque <type>
    REQUIRED_FIELDS = ['nominal', 'lifetime', 'restock', 'min']
    
    # Champs optionnels
    OPTIONAL_FIELDS = ['quantmin', 'quantmax', 'cost', 'flags', 'category', 'usage', 'value']
    
    # Flags valides
    VALID_FLAGS = ['count_in_cargo', 'count_in_hoarder', 'count_in_map', 'count_in_player', 'crafted', 'deloot']
    
    # Catégories valides
    VALID_CATEGORIES = ['weapons', 'clothes', 'food', 'tools', 'containers', 'vehiclesparts']
    
    def __init__(self, version: str = '1.28'):
        super().__init__('types', version)
    
    def validate_syntax(self, content: str) -> List[ValidationError]:
        """Valide la syntaxe XML"""
        errors = []
        
        try:
            ET.fromstring(content)
        except ET.ParseError as e:
            errors.append(ValidationError(
                severity='error',
                message=f"Erreur de syntaxe XML : {str(e)}",
                line=e.position[0] if hasattr(e, 'position') else None,
                column=e.position[1] if hasattr(e, 'position') else None,
                suggestion="Vérifiez que toutes les balises sont correctement fermées"
            ))
        
        return errors
    
    def validate_structure(self, content: str) -> List[ValidationError]:
        """Valide la structure de types.xml"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            # Vérifier la balise racine
            if root.tag != 'types':
                errors.append(ValidationError(
                    severity='error',
                    message=f"Balise racine invalide : '{root.tag}'. Attendu : 'types'",
                    line=1,
                    suggestion="La balise racine doit être <types>"
                ))
                return errors  # Impossible de continuer
            
            # Vérifier chaque <type>
            for idx, type_elem in enumerate(root.findall('type'), start=1):
                item_name = type_elem.get('name')
                
                # Attribut 'name' requis
                if not item_name:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Élément <type> #{idx} : attribut 'name' manquant",
                        line=idx,
                        field='name',
                        suggestion="Ajoutez l'attribut name='ItemClassName'"
                    ))
                    item_name = f"Item #{idx}"
                
                # Vérifier les champs requis
                for field in self.REQUIRED_FIELDS:
                    if type_elem.find(field) is None:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"Item '{item_name}' : champ requis <{field}> manquant",
                            line=idx,
                            field=field,
                            suggestion=f"Ajoutez <{field}>valeur</{field}>"
                        ))
                
                # Vérifier les types de données
                errors.extend(self._validate_field_types(type_elem, item_name, idx))
                
                # Vérifier les flags
                errors.extend(self._validate_flags(type_elem, item_name, idx))
                
                # Vérifier la catégorie
                errors.extend(self._validate_category(type_elem, item_name, idx))
        
        except ET.ParseError:
            # Déjà géré dans validate_syntax
            pass
        
        return errors
    
    def validate_business_rules(self, content: str) -> List[ValidationError]:
        """Valide les règles métier de types.xml"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            for idx, type_elem in enumerate(root.findall('type'), start=1):
                item_name = type_elem.get('name', f'Item #{idx}')
                
                # Récupérer les valeurs de manière sûre
                nominal = self.safe_int(type_elem.findtext('nominal', '0'))
                min_val = self.safe_int(type_elem.findtext('min', '0'))
                quantmin = self.safe_int(type_elem.findtext('quantmin', '-1'))
                quantmax = self.safe_int(type_elem.findtext('quantmax', '-1'))
                lifetime = self.safe_int(type_elem.findtext('lifetime', '0'))
                restock = self.safe_int(type_elem.findtext('restock', '0'))
                
                # RÈGLE 1: min ≤ nominal
                if min_val > nominal:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Item '{item_name}' : min ({min_val}) > nominal ({nominal})",
                        line=idx,
                        field='min',
                        suggestion=f"Réduisez min à {nominal} ou augmentez nominal à {min_val}",
                        context="Le minimum ne peut pas être supérieur au nominal"
                    ))
                
                # RÈGLE 2: quantmin ≤ quantmax (si les deux sont définis)
                if quantmin != -1 and quantmax != -1 and quantmin > quantmax:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Item '{item_name}' : quantmin ({quantmin}) > quantmax ({quantmax})",
                        line=idx,
                        field='quantmin',
                        suggestion=f"Réduisez quantmin à {quantmax} ou augmentez quantmax à {quantmin}",
                        context="La quantité minimum ne peut pas être supérieure au maximum"
                    ))
                
                # RÈGLE 3: lifetime > 0
                if lifetime <= 0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Item '{item_name}' : lifetime ({lifetime}) doit être > 0",
                        line=idx,
                        field='lifetime',
                        suggestion="Définissez un lifetime positif (ex: 3600 pour 1 heure)",
                        context="Les items doivent avoir une durée de vie"
                    ))
                
                # RÈGLE 4: restock > 0
                if restock <= 0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Item '{item_name}' : restock ({restock}) doit être > 0",
                        line=idx,
                        field='restock',
                        suggestion="Définissez un restock positif (ex: 1800 pour 30 min)",
                        context="Les items doivent avoir un intervalle de respawn"
                    ))
                
                # RÈGLE 5: Item désactivé mais min > 0
                if nominal == 0 and min_val > 0:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Item '{item_name}' : nominal=0 (désactivé) mais min={min_val}",
                        line=idx,
                        field='min',
                        suggestion="Mettez min=0 car l'item est désactivé",
                        context="Un item désactivé ne devrait pas avoir de minimum"
                    ))
                
                # RÈGLE 6: Pas de <usage> = pas de spawn naturel
                usages = type_elem.findall('usage')
                if nominal > 0 and len(usages) == 0:
                    flags = type_elem.find('flags')
                    crafted = flags.get('crafted', '0') if flags is not None else '0'
                    if crafted == '0':
                        errors.append(ValidationError(
                            severity='warning',
                            message=f"Item '{item_name}' : nominal={nominal} mais aucun <usage> défini",
                            line=idx,
                            field='usage',
                            suggestion="Ajoutez au moins un <usage> (ex: <usage name='Military'/>)",
                            context="Cet item ne spawnera pas naturellement sans usage"
                        ))
                
                # RÈGLE 7: count_in_player=1 sur item commun (mauvaise pratique)
                flags = type_elem.find('flags')
                if flags is not None and flags.get('count_in_player') == '1':
                    if nominal > 10:  # Item "commun"
                        errors.append(ValidationError(
                            severity='warning',
                            message=f"Item '{item_name}' : count_in_player=1 sur item commun (nominal={nominal})",
                            line=idx,
                            field='flags',
                            suggestion="Réservez count_in_player=1 aux items très rares (nominal < 10)",
                            context="Impact performance : chaque inventaire joueur est vérifié"
                        ))
        
        except ET.ParseError:
            # Déjà géré
            pass
        
        return errors
    
    def _validate_field_types(self, type_elem, item_name: str, line: int) -> List[ValidationError]:
        """Valide les types de données des champs"""
        errors = []
        
        # Champs qui doivent être des entiers
        int_fields = ['nominal', 'min', 'lifetime', 'restock', 'quantmin', 'quantmax', 'cost']
        
        for field in int_fields:
            field_elem = type_elem.find(field)
            if field_elem is not None and field_elem.text:
                try:
                    int(field_elem.text)
                except ValueError:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Item '{item_name}' : {field}='{field_elem.text}' n'est pas un entier valide",
                        line=line,
                        field=field,
                        suggestion=f"Utilisez un nombre entier pour {field}"
                    ))
        
        return errors
    
    def _validate_flags(self, type_elem, item_name: str, line: int) -> List[ValidationError]:
        """Valide les flags"""
        errors = []
        
        flags_elem = type_elem.find('flags')
        if flags_elem is not None:
            for flag_name, flag_value in flags_elem.attrib.items():
                # Vérifier que le flag est connu
                if flag_name not in self.VALID_FLAGS:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Item '{item_name}' : flag '{flag_name}' inconnu",
                        line=line,
                        field='flags',
                        suggestion=f"Flags valides : {', '.join(self.VALID_FLAGS)}"
                    ))
                
                # Vérifier que la valeur est 0 ou 1
                if flag_value not in ['0', '1']:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Item '{item_name}' : flag '{flag_name}'='{flag_value}' invalide",
                        line=line,
                        field='flags',
                        suggestion="Les flags doivent valoir 0 ou 1"
                    ))
        
        return errors
    
    def _validate_category(self, type_elem, item_name: str, line: int) -> List[ValidationError]:
        """Valide la catégorie"""
        errors = []
        
        category_elem = type_elem.find('category')
        if category_elem is not None:
            category_name = category_elem.get('name')
            if category_name and category_name not in self.VALID_CATEGORIES:
                errors.append(ValidationError(
                    severity='warning',
                    message=f"Item '{item_name}' : catégorie '{category_name}' non standard",
                    line=line,
                    field='category',
                    suggestion=f"Catégories standards : {', '.join(self.VALID_CATEGORIES)}",
                    context="Les catégories custom fonctionnent mais ne sont pas documentées"
                ))
        
        return errors
