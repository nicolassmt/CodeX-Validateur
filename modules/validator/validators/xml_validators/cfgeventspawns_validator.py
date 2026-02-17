"""
cfgeventspawns_validator.py
Validateur pour cfgEventSpawns.xml - Positions spawn events

Source: DayZ Wiki - cfgEventSpawns.xml Configuration
"""

import xml.etree.ElementTree as ET
from typing import List
from ...base_validator import BaseValidator, ValidationError


class CfgEventSpawnsValidator(BaseValidator):
    """
    Validateur pour cfgEventSpawns.xml
    Basé sur la documentation officielle DayZ
    """
    
    # Limites coordonnées par carte
    MAP_BOUNDS = {
        'Chernarus': {'x': (0, 15360), 'z': (0, 15360)},
        'Livonia': {'x': (0, 12800), 'z': (0, 12800)},
        'Sakhal': {'x': (0, 12800), 'z': (0, 12800)},
        'Default': {'x': (0, 16000), 'z': (0, 16000)}  # Sécurité
    }
    
    def __init__(self, version: str = '1.28', map_name: str = 'Default'):
        super().__init__('cfgeventspawns', version)
        self.map_name = map_name
        self.bounds = self.MAP_BOUNDS.get(map_name, self.MAP_BOUNDS['Default'])
    
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
        """Valide la structure de cfgEventSpawns.xml"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            # Vérifier balise racine
            if root.tag != 'eventposdef':
                errors.append(ValidationError(
                    severity='error',
                    message=f"Balise racine invalide : '{root.tag}'. Attendu : 'eventposdef'",
                    line=1,
                    suggestion="La balise racine doit être <eventposdef>"
                ))
                return errors
            
            # Vérifier chaque event
            for idx, event_elem in enumerate(root.findall('event'), start=1):
                event_name = event_elem.get('name')
                
                # Attribut 'name' requis
                if not event_name:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Event #{idx} : attribut 'name' manquant",
                        line=idx,
                        suggestion="Format: <event name='StaticHeliCrash'>",
                        context="Doc: Must exactly match an event name defined in events.xml"
                    ))
                    event_name = f"Event #{idx}"
                
                # Vérifier positions
                positions = event_elem.findall('pos')
                
                if len(positions) == 0:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Event '{event_name}' : aucune position définie",
                        line=idx,
                        suggestion="Ajoutez au moins une <pos x='...' z='...' a='0.0'/>",
                        context="Sans positions, l'event ne pourra pas spawn"
                    ))
                
                # Valider chaque position
                for pos_idx, pos_elem in enumerate(positions, start=1):
                    errors.extend(self._validate_position(pos_elem, event_name, pos_idx))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def validate_business_rules(self, content: str) -> List[ValidationError]:
        """Valide les règles métier"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            for event_elem in root.findall('event'):
                event_name = event_elem.get('name', 'Unknown')
                positions = event_elem.findall('pos')
                
                # WARNING: Trop peu de positions
                if len(positions) < 3:
                    errors.append(ValidationError(
                        severity='info',
                        message=f"Event '{event_name}' : seulement {len(positions)} position(s)",
                        field='pos',
                        suggestion="Recommandé: ajoutez plus de positions pour la variété",
                        context="Doc: Add more spawn points than max simultaneous events for variety"
                    ))
                
                # Vérifier coordonnées hors limites
                for pos_idx, pos_elem in enumerate(positions, start=1):
                    x = pos_elem.get('x')
                    z = pos_elem.get('z')
                    
                    if x and z:
                        try:
                            x_val = float(x)
                            z_val = float(z)
                            
                            # Vérifier dans les limites de la carte
                            x_min, x_max = self.bounds['x']
                            z_min, z_max = self.bounds['z']
                            
                            if x_val < x_min or x_val > x_max:
                                errors.append(ValidationError(
                                    severity='error',
                                    message=f"Event '{event_name}' pos #{pos_idx} : x={x_val} hors limites [{x_min}-{x_max}]",
                                    field='x',
                                    suggestion=f"Coordonnées valides pour {self.map_name}: x=[{x_min}-{x_max}]",
                                    context="Doc: Using coordinates outside the map boundaries"
                                ))
                            
                            if z_val < z_min or z_val > z_max:
                                errors.append(ValidationError(
                                    severity='error',
                                    message=f"Event '{event_name}' pos #{pos_idx} : z={z_val} hors limites [{z_min}-{z_max}]",
                                    field='z',
                                    suggestion=f"Coordonnées valides pour {self.map_name}: z=[{z_min}-{z_max}]",
                                    context="Doc: Using coordinates outside the map boundaries"
                                ))
                        
                        except ValueError:
                            pass  # Déjà géré dans validate_structure
        
        except ET.ParseError:
            pass
        
        return errors
    
    def _validate_position(self, pos_elem, event_name: str, pos_idx: int) -> List[ValidationError]:
        """Valide une position individuelle"""
        errors = []
        
        x = pos_elem.get('x')
        z = pos_elem.get('z')
        a = pos_elem.get('a')
        
        # Attribut x requis
        if not x:
            errors.append(ValidationError(
                severity='error',
                message=f"Event '{event_name}' pos #{pos_idx} : attribut 'x' manquant",
                field='x',
                suggestion="Format: <pos x='4540.4' z='8312.6' a='0.0'/>"
            ))
        else:
            # Vérifier que x est un nombre
            try:
                float(x)
            except ValueError:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Event '{event_name}' pos #{pos_idx} : x='{x}' n'est pas un nombre valide",
                    field='x'
                ))
        
        # Attribut z requis
        if not z:
            errors.append(ValidationError(
                severity='error',
                message=f"Event '{event_name}' pos #{pos_idx} : attribut 'z' manquant",
                field='z',
                suggestion="Format: <pos x='4540.4' z='8312.6' a='0.0'/>"
            ))
        else:
            # Vérifier que z est un nombre
            try:
                float(z)
            except ValueError:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Event '{event_name}' pos #{pos_idx} : z='{z}' n'est pas un nombre valide",
                    field='z'
                ))
        
        # Attribut a optionnel mais recommandé
        if not a:
            errors.append(ValidationError(
                severity='info',
                message=f"Event '{event_name}' pos #{pos_idx} : attribut 'a' manquant (rotation)",
                field='a',
                suggestion="Ajoutez a='0.0' (rotation par défaut) ou randomisez"
            ))
        else:
            # Vérifier que a est un nombre
            try:
                a_val = float(a)
                # Vérifier range 0-360
                if a_val < 0 or a_val > 360:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Event '{event_name}' pos #{pos_idx} : a={a_val} hors range [0-360]",
                        field='a',
                        suggestion="Angle en degrés: 0-360",
                        context="Doc: rotation angle in degrees (0-360)"
                    ))
            except ValueError:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Event '{event_name}' pos #{pos_idx} : a='{a}' n'est pas un nombre valide",
                    field='a'
                ))
        
        return errors
