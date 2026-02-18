"""
cfgeventgroups_validator.py
Validateur pour cfgeventgroups.xml - Groupes d'objets pour events

NOTE: Validation syntaxique stricte (pas de doc officielle complète)
Structure déduite du fichier vanilla
"""

import xml.etree.ElementTree as ET
from typing import List
from ...base_validator import BaseValidator, ValidationError


class CfgEventGroupsValidator(BaseValidator):
    """
    Validateur pour cfgeventgroups.xml
    
    Structure déduite:
    <eventgroupdef>
        <group name="...">
            <child type="..." deloot="0/1" lootmax="..." lootmin="..." 
                   x="..." z="..." a="..." y="..." spawnsecondary="true/false" />
        </group>
    </eventgroupdef>
    """
    
    def __init__(self, version: str = '1.28'):
        super().__init__('cfgeventgroups', version)
    
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
        """Valide la structure de cfgeventgroups.xml"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            # Vérifier balise racine
            if root.tag != 'eventgroupdef':
                errors.append(ValidationError(
                    severity='error',
                    message=f"Balise racine invalide : '{root.tag}'. Attendu : 'eventgroupdef'",
                    line=1,
                    suggestion="La balise racine doit être <eventgroupdef>"
                ))
                return errors
            
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
                
                # Vérifier chaque child
                for child_idx, child_elem in enumerate(group_elem.findall('child'), start=1):
                    errors.extend(self._validate_child_business(child_elem, group_name, child_idx))
        
        except ET.ParseError:
            pass
        
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
                suggestion="Format: <group name='GroupName'>"
            ))
            group_name = f"Group #{idx}"
        
        # Vérifier children
        children = group_elem.findall('child')
        if len(children) == 0:
            errors.append(ValidationError(
                severity='warning',
                message=f"Group '{group_name}' : aucun <child> défini",
                suggestion="Sans enfants, le groupe ne spawnera rien"
            ))
        
        # Vérifier chaque child
        for child_idx, child_elem in enumerate(children, start=1):
            errors.extend(self._validate_child(child_elem, group_name, child_idx))
        
        return errors
    
    def _validate_child(self, child_elem, group_name: str, child_idx: int) -> List[ValidationError]:
        """Valide un child"""
        errors = []
        
        # Attribut type requis
        child_type = child_elem.get('type')
        if not child_type:
            errors.append(ValidationError(
                severity='error',
                message=f"Group '{group_name}' child #{child_idx} : attribut 'type' manquant",
                field='child.type',
                suggestion="Format: <child type='ObjectClassName' ...>"
            ))
            child_type = 'Unknown'
        
        # Attributs requis selon le type d'objet
        # Si deloot présent, lootmax et lootmin requis
        deloot = child_elem.get('deloot')
        if deloot is not None:
            if child_elem.get('lootmax') is None:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Group '{group_name}' child '{child_type}' : 'lootmax' manquant (requis avec deloot)",
                    field='child.lootmax',
                    suggestion="Format: lootmax='3'"
                ))
            
            if child_elem.get('lootmin') is None:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Group '{group_name}' child '{child_type}' : 'lootmin' manquant (requis avec deloot)",
                    field='child.lootmin',
                    suggestion="Format: lootmin='1'"
                ))
        
        # Attributs position
        required_pos = ['x', 'z', 'a']
        for attr in required_pos:
            if child_elem.get(attr) is None:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Group '{group_name}' child '{child_type}' : attribut '{attr}' manquant",
                    field=f'child.{attr}',
                    suggestion=f"Ajoutez {attr}='...' (position/angle requis)"
                ))
        
        # y est optionnel mais recommandé
        if child_elem.get('y') is None:
            errors.append(ValidationError(
                severity='info',
                message=f"Group '{group_name}' child '{child_type}' : attribut 'y' absent (hauteur)",
                field='child.y'
            ))
        
        return errors
    
    def _validate_child_business(self, child_elem, group_name: str, child_idx: int) -> List[ValidationError]:
        """Valide les règles métier d'un child"""
        errors = []
        
        child_type = child_elem.get('type', 'Unknown')
        
        # Vérifier deloot (0 ou 1)
        deloot = child_elem.get('deloot')
        if deloot and deloot not in ['0', '1']:
            errors.append(ValidationError(
                severity='error',
                message=f"Group '{group_name}' child '{child_type}' : deloot '{deloot}' invalide (doit être 0 ou 1)",
                field='child.deloot'
            ))
        
        # Vérifier lootmax/lootmin
        lootmax = child_elem.get('lootmax')
        lootmin = child_elem.get('lootmin')
        
        if lootmax and lootmin:
            try:
                max_val = int(lootmax)
                min_val = int(lootmin)
                
                if min_val > max_val:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Group '{group_name}' child '{child_type}' : lootmin ({min_val}) > lootmax ({max_val})",
                        field='child.lootmin',
                        suggestion=f"lootmin doit être ≤ {max_val}"
                    ))
                
                if min_val < 0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Group '{group_name}' child '{child_type}' : lootmin ({min_val}) ne peut pas être négatif",
                        field='child.lootmin'
                    ))
                
                if max_val < 0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Group '{group_name}' child '{child_type}' : lootmax ({max_val}) ne peut pas être négatif",
                        field='child.lootmax'
                    ))
            
            except ValueError:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Group '{group_name}' child '{child_type}' : lootmax ou lootmin n'est pas un entier valide",
                    field='child.lootmax'
                ))
        
        # Vérifier spawnsecondary (true/false)
        spawnsecondary = child_elem.get('spawnsecondary')
        if spawnsecondary and spawnsecondary.lower() not in ['true', 'false']:
            errors.append(ValidationError(
                severity='error',
                message=f"Group '{group_name}' child '{child_type}' : spawnsecondary '{spawnsecondary}' invalide",
                field='child.spawnsecondary',
                suggestion="Valeurs valides: 'true' ou 'false'"
            ))
        
        # Vérifier coordonnées sont des nombres
        for coord in ['x', 'z', 'a', 'y']:
            value = child_elem.get(coord)
            if value:
                try:
                    float(value)
                except ValueError:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Group '{group_name}' child '{child_type}' : {coord}='{value}' n'est pas un nombre",
                        field=f'child.{coord}'
                    ))
        
        return errors
