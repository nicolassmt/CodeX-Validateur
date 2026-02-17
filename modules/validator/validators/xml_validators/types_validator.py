"""
types_validator.py
Validateur pour types.xml - Configuration économie loot

Source: DayZ Wiki - Types.xml Configuration
"""

import xml.etree.ElementTree as ET
from typing import List
from ...base_validator import BaseValidator, ValidationError


class TypesValidator(BaseValidator):
    """
    Validateur pour types.xml
    Basé sur la documentation officielle DayZ
    """
    
    # Champs requis
    REQUIRED_FIELDS = ['nominal', 'lifetime', 'restock', 'min']
    
    # Champs optionnels courants
    OPTIONAL_FIELDS = ['quantmin', 'quantmax', 'cost']
    
    # Flags valides
    VALID_FLAGS = ['count_in_cargo', 'count_in_hoarder', 'count_in_map', 
                   'count_in_player', 'crafted', 'deloot']
    
    # Catégories valides (doc officielle)
    VALID_CATEGORIES = ['weapons', 'food', 'tools', 'clothes', 'containers', 'vehiclesparts']
    
    # Usage valides (doc)
    VALID_USAGES = ['Military', 'Town', 'Farm', 'Industrial', 'Medic', 'Firefighter',
                    'Police', 'Hunting', 'Village', 'Coast', 'School', 'Office']
    
    # Tiers valides (doc)
    VALID_TIERS = ['Tier1', 'Tier2', 'Tier3', 'Tier4']
    
    # Valeurs lifetime courantes (doc)
    COMMON_LIFETIMES = {
        3600: '1 hour (common items)',
        7200: '2 hours',
        14400: '4 hours (standard items)',
        604800: '7 days (base building)'
    }
    
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
                suggestion="Vérifiez que toutes les balises sont correctement fermées"
            ))
        
        return errors
    
    def validate_structure(self, content: str) -> List[ValidationError]:
        """Valide la structure de types.xml"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            # Vérifier balise racine
            if root.tag != 'types':
                errors.append(ValidationError(
                    severity='error',
                    message=f"Balise racine invalide : '{root.tag}'. Attendu : 'types'",
                    line=1,
                    suggestion="La balise racine doit être <types>"
                ))
                return errors
            
            # Vérifier chaque type
            for idx, type_elem in enumerate(root.findall('type'), start=1):
                item_name = type_elem.get('name')
                
                # Attribut 'name' requis
                if not item_name:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Type #{idx} : attribut 'name' manquant",
                        line=idx,
                        suggestion="Format: <type name='ItemClassName'>"
                    ))
                    item_name = f"Item #{idx}"
                
                # Vérifier champs requis
                for field in self.REQUIRED_FIELDS:
                    if type_elem.find(field) is None:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"Item '{item_name}' : champ requis <{field}> manquant",
                            line=idx,
                            field=field,
                            suggestion=f"Ajoutez <{field}>valeur</{field}>"
                        ))
                
                # Vérifier types de données
                errors.extend(self._validate_field_types(type_elem, item_name, idx))
                
                # Vérifier flags
                errors.extend(self._validate_flags(type_elem, item_name, idx))
                
                # Vérifier catégorie
                errors.extend(self._validate_category(type_elem, item_name, idx))
                
                # Vérifier usage (max 4)
                errors.extend(self._validate_usage(type_elem, item_name, idx))
                
                # Vérifier value (tiers)
                errors.extend(self._validate_value(type_elem, item_name, idx))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def validate_business_rules(self, content: str) -> List[ValidationError]:
        """Valide les règles métier selon doc"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            for idx, type_elem in enumerate(root.findall('type'), start=1):
                item_name = type_elem.get('name', f'Item #{idx}')
                
                # Récupérer valeurs
                nominal = self.safe_int(type_elem.findtext('nominal', '0'))
                min_val = self.safe_int(type_elem.findtext('min', '0'))
                quantmin = self.safe_int(type_elem.findtext('quantmin', '-1'))
                quantmax = self.safe_int(type_elem.findtext('quantmax', '-1'))
                lifetime = self.safe_int(type_elem.findtext('lifetime', '0'))
                restock = self.safe_int(type_elem.findtext('restock', '0'))
                cost = self.safe_int(type_elem.findtext('cost', '100'))
                
                # RÈGLE 1: min ≤ nominal (doc: "Typically set to 50-80% of the nominal value")
                if min_val > nominal:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Item '{item_name}' : min ({min_val}) > nominal ({nominal})",
                        line=idx,
                        field='min',
                        suggestion=f"Réduisez min à {int(nominal * 0.8)} (80% de nominal)",
                        context="Doc: min should typically be 50-80% of nominal"
                    ))
                
                # RÈGLE 2: quantmin ≤ quantmax (si les deux != -1)
                if quantmin != -1 and quantmax != -1 and quantmin > quantmax:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Item '{item_name}' : quantmin ({quantmin}) > quantmax ({quantmax})",
                        line=idx,
                        field='quantmin',
                        suggestion=f"Réduisez quantmin à {quantmax} ou augmentez quantmax",
                        context="Doc: quantmin and quantmax create a random range"
                    ))
                
                # RÈGLE 3: quantmin/quantmax entre 0-100 (si != -1)
                if quantmin != -1 and (quantmin < 0 or quantmin > 100):
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Item '{item_name}' : quantmin ({quantmin}) hors range [0-100]",
                        line=idx,
                        field='quantmin',
                        suggestion="Valeurs valides: -1 (non applicable) ou 0-100 (%)",
                        context="Doc: percentage (0-100) of capacity"
                    ))
                
                if quantmax != -1 and (quantmax < 0 or quantmax > 100):
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Item '{item_name}' : quantmax ({quantmax}) hors range [0-100]",
                        line=idx,
                        field='quantmax',
                        suggestion="Valeurs valides: -1 (non applicable) ou 0-100 (%)",
                        context="Doc: percentage (0-100) of capacity"
                    ))
                
                # RÈGLE 4: lifetime > 0
                if lifetime <= 0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Item '{item_name}' : lifetime ({lifetime}) doit être > 0",
                        line=idx,
                        field='lifetime',
                        suggestion="Valeurs courantes: 3600 (1h), 14400 (4h), 604800 (7j)",
                        context="Doc: How long in seconds an item will persist"
                    ))
                
                # RÈGLE 5: restock >= 0 (0 = OK pour respawn immédiat)
                if restock < 0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Item '{item_name}' : restock ({restock}) ne peut pas être négatif",
                        line=idx,
                        field='restock',
                        suggestion="0 = respawn immédiat, 1800-3600 = scarcity",
                        context="Doc: Set to 0 for immediate respawn eligibility"
                    ))
                
                # WARNING: nominal = 0 mais min > 0
                if nominal == 0 and min_val > 0:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Item '{item_name}' : nominal=0 (désactivé) mais min={min_val}",
                        line=idx,
                        field='min',
                        suggestion="Mettez min=0 car l'item est désactivé"
                    ))
                
                # WARNING: Pas de <usage> pour item avec nominal > 0
                usages = type_elem.findall('usage')
                if nominal > 0 and len(usages) == 0:
                    flags = type_elem.find('flags')
                    crafted = flags.get('crafted', '0') if flags is not None else '0'
                    deloot = flags.get('deloot', '0') if flags is not None else '0'
                    
                    if crafted == '0' and deloot == '0':
                        errors.append(ValidationError(
                            severity='warning',
                            message=f"Item '{item_name}' : nominal={nominal} mais aucun <usage> défini",
                            line=idx,
                            field='usage',
                            suggestion="Ajoutez <usage name='Town'/> ou autre zone de spawn",
                            context="Sans usage, l'item ne spawnera pas naturellement"
                        ))
                
                # WARNING: Plus de 4 usage (doc: "Max 4 per item")
                if len(usages) > 4:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Item '{item_name}' : {len(usages)} <usage> définis (max recommandé: 4)",
                        line=idx,
                        field='usage',
                        context="Doc: Max 4 per item"
                    ))
                
                # WARNING: count_in_player=1 sur item commun
                flags = type_elem.find('flags')
                if flags is not None and flags.get('count_in_player') == '1':
                    if nominal > 10:
                        errors.append(ValidationError(
                            severity='warning',
                            message=f"Item '{item_name}' : count_in_player=1 sur item commun (nominal={nominal})",
                            line=idx,
                            field='flags',
                            suggestion="Réservez count_in_player=1 aux items très rares (nominal < 10)",
                            context="Doc: Enable for extremely rare items"
                        ))
                
                # WARNING: count_in_map=0 (presque jamais voulu)
                if flags is not None and flags.get('count_in_map') == '0':
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Item '{item_name}' : count_in_map=0 causerait spawn infini",
                        line=idx,
                        field='flags',
                        suggestion="Mettez count_in_map=1 (obligatoire pour économie)",
                        context="Doc: This should almost always be enabled (1)"
                    ))
                
                # WARNING: nominal très élevé (performance)
                if nominal > 500:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Item '{item_name}' : nominal ({nominal}) très élevé",
                        line=idx,
                        field='nominal',
                        suggestion="Valeurs élevées impactent les performances serveur",
                        context="Doc: be careful not to set this too high"
                    ))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def _validate_field_types(self, type_elem, item_name: str, line: int) -> List[ValidationError]:
        """Valide les types de données"""
        errors = []
        
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
                # Vérifier flag connu
                if flag_name not in self.VALID_FLAGS:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Item '{item_name}' : flag '{flag_name}' inconnu",
                        line=line,
                        field='flags',
                        suggestion=f"Flags valides: {', '.join(self.VALID_FLAGS)}"
                    ))
                
                # Vérifier valeur 0 ou 1
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
        
        categories = type_elem.findall('category')
        
        # Doc: "Each item should have exactly one category"
        if len(categories) == 0:
            errors.append(ValidationError(
                severity='warning',
                message=f"Item '{item_name}' : aucune <category> définie",
                line=line,
                field='category',
                suggestion="Ajoutez <category name='weapons'/> ou autre",
                context="Doc: Each item should have exactly one category"
            ))
        elif len(categories) > 1:
            errors.append(ValidationError(
                severity='warning',
                message=f"Item '{item_name}' : {len(categories)} catégories définies (recommandé: 1)",
                line=line,
                field='category',
                context="Doc: Each item should have exactly one category"
            ))
        
        # Vérifier catégories valides
        for cat_elem in categories:
            cat_name = cat_elem.get('name')
            if cat_name and cat_name not in self.VALID_CATEGORIES:
                errors.append(ValidationError(
                    severity='info',
                    message=f"Item '{item_name}' : catégorie '{cat_name}' non standard",
                    line=line,
                    field='category',
                    suggestion=f"Catégories standards: {', '.join(self.VALID_CATEGORIES)}",
                    context="Catégories custom OK si définies dans cfglimitsdefinition.xml"
                ))
        
        return errors
    
    def _validate_usage(self, type_elem, item_name: str, line: int) -> List[ValidationError]:
        """Valide les usage"""
        errors = []
        
        usages = type_elem.findall('usage')
        
        for usage_elem in usages:
            usage_name = usage_elem.get('name')
            if usage_name and usage_name not in self.VALID_USAGES:
                errors.append(ValidationError(
                    severity='info',
                    message=f"Item '{item_name}' : usage '{usage_name}' non standard",
                    line=line,
                    field='usage',
                    suggestion=f"Usages standards: {', '.join(self.VALID_USAGES[:6])}...",
                    context="Usages custom OK si définis dans cfglimitsdefinition.xml"
                ))
        
        return errors
    
    def _validate_value(self, type_elem, item_name: str, line: int) -> List[ValidationError]:
        """Valide les value (tiers)"""
        errors = []
        
        values = type_elem.findall('value')
        
        for value_elem in values:
            value_name = value_elem.get('name')
            if value_name and value_name not in self.VALID_TIERS:
                errors.append(ValidationError(
                    severity='info',
                    message=f"Item '{item_name}' : value '{value_name}' non standard",
                    line=line,
                    field='value',
                    suggestion=f"Tiers standards: {', '.join(self.VALID_TIERS)}",
                    context="Doc: Tier1 is coastal, Tier4 is high-value inland military"
                ))
        
        return errors
