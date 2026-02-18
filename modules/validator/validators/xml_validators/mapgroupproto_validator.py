"""
mapgroupproto_validator.py
Validateur pour mapgroupproto.xml - Prototypes de groupes de loot

NOTE: Validation syntaxique stricte (pas de doc officielle disponible)
"""

import xml.etree.ElementTree as ET
from typing import List
from ...base_validator import BaseValidator, ValidationError


class MapGroupProtoValidator(BaseValidator):
    """
    Validateur pour mapgroupproto.xml
    
    Structure déduite du fichier vanilla:
    <prototype>
        <defaults>
            <default name="..." ... />
        </defaults>
        <group name="..." lootmax="...">
            <usage name="..." />
            <container name="..." lootmax="...">
                <category name="..." />
                <tag name="..." />
                <point pos="..." range="..." height="..." flags="..." />
            </container>
        </group>
    </prototype>
    """
    
    def __init__(self, version: str = '1.28'):
        super().__init__('mapgroupproto', version)
    
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
        """Valide la structure de mapgroupproto.xml"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            # Vérifier balise racine
            if root.tag != 'prototype':
                errors.append(ValidationError(
                    severity='error',
                    message=f"Balise racine invalide : '{root.tag}'. Attendu : 'prototype'",
                    line=1,
                    suggestion="La balise racine doit être <prototype>"
                ))
                return errors
            
            # Vérifier section defaults (optionnelle)
            defaults_elem = root.find('defaults')
            if defaults_elem is not None:
                errors.extend(self._validate_defaults(defaults_elem))
            
            # Vérifier chaque group
            for idx, group_elem in enumerate(root.findall('group'), start=1):
                errors.extend(self._validate_group(group_elem, idx))
        
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
                lootmax = group_elem.get('lootmax')
                
                # Vérifier lootmax est un nombre
                if lootmax:
                    try:
                        lootmax_val = int(lootmax)
                        if lootmax_val < 0:
                            errors.append(ValidationError(
                                severity='error',
                                message=f"Group '{group_name}' : lootmax ({lootmax_val}) ne peut pas être négatif",
                                field='lootmax'
                            ))
                        elif lootmax_val == 0:
                            errors.append(ValidationError(
                                severity='warning',
                                message=f"Group '{group_name}' : lootmax=0 (aucun loot ne spawne)",
                                field='lootmax'
                            ))
                    except ValueError:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"Group '{group_name}' : lootmax='{lootmax}' n'est pas un entier",
                            field='lootmax'
                        ))
                
                # Vérifier containers
                for container_elem in group_elem.findall('container'):
                    errors.extend(self._validate_container_business(container_elem, group_name))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def _validate_defaults(self, defaults_elem) -> List[ValidationError]:
        """Valide la section defaults"""
        errors = []
        
        for default_elem in defaults_elem.findall('default'):
            name = default_elem.get('name')
            
            if not name:
                errors.append(ValidationError(
                    severity='error',
                    message="Default : attribut 'name' manquant",
                    field='default.name'
                ))
        
        return errors
    
    def _validate_group(self, group_elem, idx: int) -> List[ValidationError]:
        """Valide un group"""
        errors = []
        
        group_name = group_elem.get('name')
        
        # Attribut name requis
        if not group_name:
            errors.append(ValidationError(
                severity='error',
                message=f"Group #{idx} : attribut 'name' manquant",
                line=idx,
                suggestion="Format: <group name='BuildingName' lootmax='...'>"
            ))
            group_name = f"Group #{idx}"
        
        # Attribut lootmax optionnel mais recommandé
        if group_elem.get('lootmax') is None:
            errors.append(ValidationError(
                severity='info',
                message=f"Group '{group_name}' : attribut 'lootmax' absent (utilisera default)",
                field='lootmax'
            ))
        
        # Vérifier usage tags
        usages = group_elem.findall('usage')
        if len(usages) == 0:
            errors.append(ValidationError(
                severity='warning',
                message=f"Group '{group_name}' : aucun <usage> défini",
                suggestion="Ajoutez au moins un <usage name='...'/> (ex: Industrial, Town)"
            ))
        
        # Vérifier containers
        containers = group_elem.findall('container')
        if len(containers) == 0:
            errors.append(ValidationError(
                severity='warning',
                message=f"Group '{group_name}' : aucun <container> défini",
                suggestion="Sans container, aucun point de spawn de loot"
            ))
        
        for container_elem in containers:
            errors.extend(self._validate_container(container_elem, group_name))
        
        return errors
    
    def _validate_container(self, container_elem, group_name: str) -> List[ValidationError]:
        """Valide un container"""
        errors = []
        
        container_name = container_elem.get('name')
        
        # Attribut name requis
        if not container_name:
            errors.append(ValidationError(
                severity='error',
                message=f"Group '{group_name}' : container sans attribut 'name'",
                field='container.name',
                suggestion="Format: <container name='lootFloor' lootmax='...'>"
            ))
            container_name = 'Unnamed'
        
        # Vérifier points de spawn
        points = container_elem.findall('point')
        if len(points) == 0:
            errors.append(ValidationError(
                severity='warning',
                message=f"Group '{group_name}' container '{container_name}' : aucun <point> défini",
                suggestion="Sans points, pas de spawn de loot"
            ))
        
        # Vérifier chaque point
        for point_idx, point_elem in enumerate(points, start=1):
            errors.extend(self._validate_point(point_elem, group_name, container_name, point_idx))
        
        return errors
    
    def _validate_point(self, point_elem, group_name: str, container_name: str, point_idx: int) -> List[ValidationError]:
        """Valide un point de spawn"""
        errors = []
        
        pos = point_elem.get('pos')
        range_val = point_elem.get('range')
        height = point_elem.get('height')
        flags = point_elem.get('flags')
        
        # Attributs requis
        required = {'pos': pos, 'range': range_val, 'height': height, 'flags': flags}
        
        for attr_name, attr_value in required.items():
            if attr_value is None:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Group '{group_name}' container '{container_name}' point #{point_idx} : attribut '{attr_name}' manquant",
                    field=f'point.{attr_name}'
                ))
        
        # Vérifier format pos (3 floats)
        if pos:
            parts = pos.split()
            if len(parts) != 3:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Group '{group_name}' point #{point_idx} : pos doit avoir 3 valeurs (x y z), trouvé {len(parts)}",
                    field='point.pos',
                    suggestion="Format: pos='x y z'"
                ))
            else:
                for i, part in enumerate(parts):
                    try:
                        float(part)
                    except ValueError:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"Group '{group_name}' point #{point_idx} : pos[{i}]='{part}' n'est pas un nombre",
                            field='point.pos'
                        ))
        
        # Vérifier que range, height, flags sont des nombres
        if range_val:
            try:
                float(range_val)
            except ValueError:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Group '{group_name}' point #{point_idx} : range='{range_val}' n'est pas un nombre",
                    field='point.range'
                ))
        
        if height:
            try:
                float(height)
            except ValueError:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Group '{group_name}' point #{point_idx} : height='{height}' n'est pas un nombre",
                    field='point.height'
                ))
        
        if flags:
            try:
                int(flags)
            except ValueError:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Group '{group_name}' point #{point_idx} : flags='{flags}' n'est pas un entier",
                    field='point.flags'
                ))
        
        return errors
    
    def _validate_container_business(self, container_elem, group_name: str) -> List[ValidationError]:
        """Valide les règles métier d'un container"""
        errors = []
        
        container_name = container_elem.get('name', 'Unnamed')
        lootmax = container_elem.get('lootmax')
        
        if lootmax:
            try:
                lootmax_val = int(lootmax)
                if lootmax_val < 0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Container '{container_name}' : lootmax ({lootmax_val}) ne peut pas être négatif",
                        field='container.lootmax'
                    ))
            except ValueError:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Container '{container_name}' : lootmax='{lootmax}' n'est pas un entier",
                    field='container.lootmax'
                ))
        
        return errors
