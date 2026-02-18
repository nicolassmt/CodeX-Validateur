"""
mapgrouppos_validator.py
Validateur pour mapgrouppos.xml - Positions des groupes de loot

NOTE: Validation syntaxique stricte (pas de doc officielle disponible)
"""

import xml.etree.ElementTree as ET
from typing import List
from ...base_validator import BaseValidator, ValidationError


class MapGroupPosValidator(BaseValidator):
    """
    Validateur pour mapgrouppos.xml
    
    Structure déduite du fichier vanilla:
    <map>
        <group name="..." pos="x y z" rpy="..." a="..." />
    </map>
    """
    
    def __init__(self, version: str = '1.28'):
        super().__init__('mapgrouppos', version)
    
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
        """Valide la structure de mapgrouppos.xml"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            # Vérifier balise racine
            if root.tag != 'map':
                errors.append(ValidationError(
                    severity='error',
                    message=f"Balise racine invalide : '{root.tag}'. Attendu : 'map'",
                    line=1,
                    suggestion="La balise racine doit être <map>"
                ))
                return errors
            
            # Vérifier chaque group
            for idx, group_elem in enumerate(root.findall('group'), start=1):
                group_name = group_elem.get('name')
                
                # Attribut 'name' requis
                if not group_name:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Group #{idx} : attribut 'name' manquant",
                        line=idx,
                        suggestion="Format: <group name='BuildingName' pos='...' rpy='...' a='...'/>"
                    ))
                    group_name = f"Group #{idx}"
                
                # Vérifier attributs requis
                errors.extend(self._validate_group_attributes(group_elem, group_name, idx))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def validate_business_rules(self, content: str) -> List[ValidationError]:
        """Valide les règles métier (limitées faute de doc)"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            for idx, group_elem in enumerate(root.findall('group'), start=1):
                group_name = group_elem.get('name', f'Group #{idx}')
                pos = group_elem.get('pos')
                rpy = group_elem.get('rpy')
                a = group_elem.get('a')
                
                # Vérifier format pos (3 floats séparés par espaces)
                if pos:
                    parts = pos.split()
                    if len(parts) != 3:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"Group '{group_name}' : pos doit avoir 3 valeurs (x y z), trouvé {len(parts)}",
                            line=idx,
                            field='pos',
                            suggestion="Format: pos='x y z' (ex: '123.45 67.89 1011.12')"
                        ))
                    else:
                        # Vérifier que ce sont des nombres
                        for i, part in enumerate(parts):
                            try:
                                float(part)
                            except ValueError:
                                errors.append(ValidationError(
                                    severity='error',
                                    message=f"Group '{group_name}' : pos[{i}]='{part}' n'est pas un nombre",
                                    line=idx,
                                    field='pos'
                                ))
                
                # Vérifier format rpy (3 floats)
                if rpy:
                    parts = rpy.split()
                    if len(parts) != 3:
                        errors.append(ValidationError(
                            severity='warning',
                            message=f"Group '{group_name}' : rpy doit avoir 3 valeurs (roll pitch yaw), trouvé {len(parts)}",
                            line=idx,
                            field='rpy'
                        ))
                    else:
                        for i, part in enumerate(parts):
                            try:
                                float(part)
                            except ValueError:
                                errors.append(ValidationError(
                                    severity='error',
                                    message=f"Group '{group_name}' : rpy[{i}]='{part}' n'est pas un nombre",
                                    line=idx,
                                    field='rpy'
                                ))
                
                # Vérifier a (angle)
                if a:
                    try:
                        a_val = float(a)
                        # Warning si hors range typique -360 à 360
                        if a_val < -360 or a_val > 360:
                            errors.append(ValidationError(
                                severity='warning',
                                message=f"Group '{group_name}' : a={a_val} hors range typique [-360, 360]",
                                line=idx,
                                field='a',
                                suggestion="Angle généralement entre -360 et 360 degrés"
                            ))
                    except ValueError:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"Group '{group_name}' : a='{a}' n'est pas un nombre",
                            line=idx,
                            field='a'
                        ))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def _validate_group_attributes(self, group_elem, group_name: str, line: int) -> List[ValidationError]:
        """Valide les attributs d'un group"""
        errors = []
        
        required_attrs = ['pos', 'rpy', 'a']
        
        for attr in required_attrs:
            if group_elem.get(attr) is None:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Group '{group_name}' : attribut '{attr}' manquant",
                    line=line,
                    field=attr,
                    suggestion=f"Ajoutez {attr}='...' (voir fichier vanilla pour exemples)"
                ))
        
        return errors
