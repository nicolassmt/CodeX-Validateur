"""
cfgspawnabletypes_validator.py
Validateur pour cfgspawnabletypes.xml - Attachements et cargo

Source: DayZ Wiki - cfgspawnabletypes.xml Configuration
"""

import xml.etree.ElementTree as ET
from typing import List
from ...base_validator import BaseValidator, ValidationError


class CfgSpawnableTypesValidator(BaseValidator):
    """
    Validateur pour cfgspawnabletypes.xml
    Basé sur la documentation officielle DayZ
    """
    
    def __init__(self, version: str = '1.28'):
        super().__init__('cfgspawnabletypes', version)
    
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
        """Valide la structure de cfgspawnabletypes.xml"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            # Vérifier balise racine
            if root.tag != 'spawnabletypes':
                errors.append(ValidationError(
                    severity='error',
                    message=f"Balise racine invalide : '{root.tag}'. Attendu : 'spawnabletypes'",
                    line=1,
                    suggestion="La balise racine doit être <spawnabletypes>"
                ))
                return errors
            
            # Vérifier chaque type
            for idx, type_elem in enumerate(root.findall('type'), start=1):
                type_name = type_elem.get('name')
                
                # Attribut 'name' requis
                if not type_name:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Type #{idx} : attribut 'name' manquant",
                        line=idx,
                        suggestion="Format: <type name='ItemClassName'>",
                        context="Doc: Must exactly match a classname defined in types.xml"
                    ))
                    type_name = f"Type #{idx}"
                
                # Vérifier attachments
                for attach_idx, attach_elem in enumerate(type_elem.findall('attachments'), start=1):
                    errors.extend(self._validate_attachments(attach_elem, type_name, attach_idx))
                
                # Vérifier cargo
                for cargo_idx, cargo_elem in enumerate(type_elem.findall('cargo'), start=1):
                    errors.extend(self._validate_cargo(cargo_elem, type_name, cargo_idx))
                
                # Info si pas d'attachments ni cargo
                if len(type_elem.findall('attachments')) == 0 and len(type_elem.findall('cargo')) == 0:
                    errors.append(ValidationError(
                        severity='info',
                        message=f"Type '{type_name}' : ni attachments ni cargo définis",
                        line=idx,
                        context="L'item spawnera toujours vide"
                    ))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def validate_business_rules(self, content: str) -> List[ValidationError]:
        """Valide les règles métier selon doc"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            for idx, type_elem in enumerate(root.findall('type'), start=1):
                type_name = type_elem.get('name', f'Type #{idx}')
                
                # Vérifier attachments
                for attach_idx, attach_elem in enumerate(type_elem.findall('attachments'), start=1):
                    chance = attach_elem.get('chance')
                    
                    if chance:
                        try:
                            chance_val = float(chance)
                            
                            # RÈGLE: chance entre 0.0 et 1.0
                            if chance_val < 0.0 or chance_val > 1.0:
                                errors.append(ValidationError(
                                    severity='error',
                                    message=f"Type '{type_name}' attachments #{attach_idx} : chance ({chance_val}) hors range [0.0-1.0]",
                                    field='attachments.chance',
                                    suggestion="Probabilité entre 0.0 (jamais) et 1.0 (toujours)",
                                    context="Doc: The probability (0.0 to 1.0)"
                                ))
                            
                            # WARNING: chance très élevée
                            elif chance_val > 0.35:
                                errors.append(ValidationError(
                                    severity='warning',
                                    message=f"Type '{type_name}' attachments #{attach_idx} : chance ({chance_val}) très élevée",
                                    field='attachments.chance',
                                    suggestion="Recommandé: 0.15-0.35 pour maintenir rareté",
                                    context="Doc: Keep slot chances relatively low (0.15-0.35)"
                                ))
                        
                        except ValueError:
                            pass  # Déjà géré dans validate_structure
                    
                    # Vérifier items dans attachments
                    items = attach_elem.findall('item')
                    if len(items) == 0:
                        errors.append(ValidationError(
                            severity='warning',
                            message=f"Type '{type_name}' attachments #{attach_idx} : aucun <item> défini",
                            suggestion="Ajoutez au moins un <item name='...' chance='...'/>"
                        ))
                    
                    # Vérifier somme des chances items
                    total_chance = 0.0
                    for item_elem in items:
                        item_chance = item_elem.get('chance')
                        if item_chance:
                            try:
                                total_chance += float(item_chance)
                            except ValueError:
                                pass
                    
                    # Info si total très différent de 1.0
                    if len(items) > 0 and total_chance > 0:
                        if abs(total_chance - 1.0) > 0.1:
                            errors.append(ValidationError(
                                severity='info',
                                message=f"Type '{type_name}' attachments #{attach_idx} : somme des chances items = {total_chance:.2f}",
                                field='attachments.item.chance',
                                context="Les chances sont relatives, pas besoin qu'elles totalisent 1.0"
                            ))
                
                # Vérifier cargo
                for cargo_idx, cargo_elem in enumerate(type_elem.findall('cargo'), start=1):
                    chance = cargo_elem.get('chance')
                    
                    if chance:
                        try:
                            chance_val = float(chance)
                            
                            # RÈGLE: chance entre 0.0 et 1.0
                            if chance_val < 0.0 or chance_val > 1.0:
                                errors.append(ValidationError(
                                    severity='error',
                                    message=f"Type '{type_name}' cargo #{cargo_idx} : chance ({chance_val}) hors range [0.0-1.0]",
                                    field='cargo.chance',
                                    suggestion="Probabilité entre 0.0 (jamais) et 1.0 (toujours)"
                                ))
                        
                        except ValueError:
                            pass
                    
                    # Vérifier items dans cargo
                    items = cargo_elem.findall('item')
                    if len(items) == 0:
                        errors.append(ValidationError(
                            severity='warning',
                            message=f"Type '{type_name}' cargo #{cargo_idx} : aucun <item> défini",
                            suggestion="Ajoutez au moins un <item name='...' chance='...'/>"
                        ))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def _validate_attachments(self, attach_elem, type_name: str, attach_idx: int) -> List[ValidationError]:
        """Valide un groupe attachments"""
        errors = []
        
        # Attribut 'chance' requis
        chance = attach_elem.get('chance')
        if not chance:
            errors.append(ValidationError(
                severity='error',
                message=f"Type '{type_name}' attachments #{attach_idx} : attribut 'chance' manquant",
                field='attachments.chance',
                suggestion="Format: <attachments chance='0.25'>",
                context="Doc: The probability (0.0 to 1.0) that this attachment slot will have an item"
            ))
        else:
            # Vérifier que c'est un nombre
            try:
                chance_val = float(chance)
                if chance_val < 0.0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Type '{type_name}' attachments #{attach_idx} : chance ({chance_val}) ne peut pas être négative",
                        field='attachments.chance'
                    ))
            except ValueError:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Type '{type_name}' attachments #{attach_idx} : chance '{chance}' n'est pas un nombre",
                    field='attachments.chance'
                ))
        
        # Vérifier items
        for item_idx, item_elem in enumerate(attach_elem.findall('item'), start=1):
            errors.extend(self._validate_item(item_elem, type_name, f"attachments #{attach_idx}", item_idx))
        
        return errors
    
    def _validate_cargo(self, cargo_elem, type_name: str, cargo_idx: int) -> List[ValidationError]:
        """Valide un groupe cargo"""
        errors = []
        
        # Attribut 'chance' requis
        chance = cargo_elem.get('chance')
        if not chance:
            errors.append(ValidationError(
                severity='error',
                message=f"Type '{type_name}' cargo #{cargo_idx} : attribut 'chance' manquant",
                field='cargo.chance',
                suggestion="Format: <cargo chance='0.20'>",
                context="Doc: The probability (0.0 to 1.0) that this cargo slot will contain an item"
            ))
        else:
            # Vérifier que c'est un nombre
            try:
                chance_val = float(chance)
                if chance_val < 0.0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Type '{type_name}' cargo #{cargo_idx} : chance ({chance_val}) ne peut pas être négative",
                        field='cargo.chance'
                    ))
            except ValueError:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Type '{type_name}' cargo #{cargo_idx} : chance '{chance}' n'est pas un nombre",
                    field='cargo.chance'
                ))
        
        # Vérifier items
        for item_idx, item_elem in enumerate(cargo_elem.findall('item'), start=1):
            errors.extend(self._validate_item(item_elem, type_name, f"cargo #{cargo_idx}", item_idx))
        
        return errors
    
    def _validate_item(self, item_elem, type_name: str, group_type: str, item_idx: int) -> List[ValidationError]:
        """Valide un item"""
        errors = []
        
        # Attribut 'name' requis
        item_name = item_elem.get('name')
        if not item_name:
            errors.append(ValidationError(
                severity='error',
                message=f"Type '{type_name}' {group_type} item #{item_idx} : attribut 'name' manquant",
                field='item.name',
                suggestion="Format: <item name='ItemClassName' chance='0.50'/>"
            ))
        
        # Attribut 'chance' requis
        chance = item_elem.get('chance')
        if not chance:
            errors.append(ValidationError(
                severity='error',
                message=f"Type '{type_name}' {group_type} item #{item_idx} : attribut 'chance' manquant",
                field='item.chance',
                suggestion="Format: <item name='...' chance='0.50'/>",
                context="Doc: The relative weight for selecting this item"
            ))
        else:
            # Vérifier que c'est un nombre
            try:
                chance_val = float(chance)
                if chance_val < 0.0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Type '{type_name}' {group_type} item '{item_name}' : chance ({chance_val}) ne peut pas être négative",
                        field='item.chance'
                    ))
                elif chance_val == 0.0:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Type '{type_name}' {group_type} item '{item_name}' : chance=0 (item ne spawnera jamais)",
                        field='item.chance'
                    ))
            except ValueError:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Type '{type_name}' {group_type} item '{item_name}' : chance '{chance}' n'est pas un nombre",
                    field='item.chance'
                ))
        
        return errors
