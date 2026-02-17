"""
events_validator.py
Validateur pour events.xml - Événements dynamiques

Source: DayZ Wiki - Events.xml Configuration
"""

import xml.etree.ElementTree as ET
from typing import List
from ...base_validator import BaseValidator, ValidationError


class EventsValidator(BaseValidator):
    """
    Validateur pour events.xml
    Basé sur la documentation officielle DayZ
    """
    
    # Champs requis pour chaque event
    REQUIRED_FIELDS = ['nominal', 'min', 'max', 'lifetime', 'restock', 
                       'saferadius', 'distanceradius', 'cleanupradius']
    
    # Flags valides
    VALID_FLAGS = ['deletable', 'init_random', 'remove_damaged']
    
    # Valeurs position valides
    VALID_POSITIONS = ['fixed', 'random']
    
    # Valeurs limit valides
    VALID_LIMITS = ['child', 'parent', 'mixed']
    
    def __init__(self, version: str = '1.28'):
        super().__init__('events', version)
    
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
        """Valide la structure de events.xml"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            # Vérifier balise racine
            if root.tag != 'events':
                errors.append(ValidationError(
                    severity='error',
                    message=f"Balise racine invalide : '{root.tag}'. Attendu : 'events'",
                    line=1,
                    suggestion="La balise racine doit être <events>"
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
                        suggestion="Format: <event name='EventName'>"
                    ))
                    event_name = f"Event #{idx}"
                
                # Vérifier champs requis
                for field in self.REQUIRED_FIELDS:
                    if event_elem.find(field) is None:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"Event '{event_name}' : champ requis <{field}> manquant",
                            line=idx,
                            field=field,
                            suggestion=f"Ajoutez <{field}>valeur</{field}>"
                        ))
                
                # Vérifier flags
                errors.extend(self._validate_flags(event_elem, event_name, idx))
                
                # Vérifier position
                errors.extend(self._validate_position(event_elem, event_name, idx))
                
                # Vérifier limit
                errors.extend(self._validate_limit(event_elem, event_name, idx))
                
                # Vérifier active
                errors.extend(self._validate_active(event_elem, event_name, idx))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def validate_business_rules(self, content: str) -> List[ValidationError]:
        """Valide les règles métier selon doc"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            for idx, event_elem in enumerate(root.findall('event'), start=1):
                event_name = event_elem.get('name', f'Event #{idx}')
                
                # Récupérer valeurs
                nominal = self.safe_int(event_elem.findtext('nominal', '0'))
                min_val = self.safe_int(event_elem.findtext('min', '0'))
                max_val = self.safe_int(event_elem.findtext('max', '0'))
                lifetime = self.safe_int(event_elem.findtext('lifetime', '0'))
                restock = self.safe_int(event_elem.findtext('restock', '0'))
                saferadius = self.safe_int(event_elem.findtext('saferadius', '0'))
                distanceradius = self.safe_int(event_elem.findtext('distanceradius', '0'))
                cleanupradius = self.safe_int(event_elem.findtext('cleanupradius', '0'))
                
                # RÈGLE 1: min ≤ nominal ≤ max
                if min_val > nominal:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Event '{event_name}' : min ({min_val}) > nominal ({nominal})",
                        line=idx,
                        field='min',
                        suggestion=f"Réduisez min à {nominal} ou augmentez nominal",
                        context="Doc: The server will never spawn fewer than min"
                    ))
                
                if nominal > max_val:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Event '{event_name}' : nominal ({nominal}) > max ({max_val})",
                        line=idx,
                        field='nominal',
                        suggestion=f"Réduisez nominal à {max_val} ou augmentez max",
                        context="Doc: The server will never spawn more than max"
                    ))
                
                # RÈGLE 2: lifetime > 0
                if lifetime <= 0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Event '{event_name}' : lifetime ({lifetime}) doit être > 0",
                        line=idx,
                        field='lifetime',
                        suggestion="Valeurs courantes: 1800 (30min), 3600 (1h)",
                        context="Doc: How long in seconds the event persists"
                    ))
                
                # RÈGLE 3: restock >= 0 (0 = respawn immédiat OK)
                if restock < 0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Event '{event_name}' : restock ({restock}) ne peut pas être négatif",
                        line=idx,
                        field='restock',
                        suggestion="0 = respawn immédiat, ou valeur en secondes",
                        context="Doc: Set to 0 for immediate respawn eligibility"
                    ))
                
                # RÈGLE 4: saferadius > 0 (recommandé)
                if saferadius <= 0:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Event '{event_name}' : saferadius ({saferadius}) = 0 ou négatif",
                        line=idx,
                        field='saferadius',
                        suggestion="Recommandé: >= 200 pour éviter clustering",
                        context="Doc: Prevents events from spawning too close together"
                    ))
                
                # RÈGLE 5: cleanupradius >= 0
                if cleanupradius < 0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Event '{event_name}' : cleanupradius ({cleanupradius}) ne peut pas être négatif",
                        line=idx,
                        field='cleanupradius'
                    ))
                
                # WARNING: nominal très élevé (performance)
                if nominal > 50:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Event '{event_name}' : nominal ({nominal}) très élevé",
                        line=idx,
                        field='nominal',
                        suggestion="Valeurs élevées impactent les performances",
                        context="Doc: Setting extremely high nominal values can impact server performance"
                    ))
                
                # WARNING: saferadius très faible (clustering)
                if 0 < saferadius < 100:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Event '{event_name}' : saferadius ({saferadius}) très faible",
                        line=idx,
                        field='saferadius',
                        suggestion="Recommandé: >= 200 pour spreading correct",
                        context="Doc: Using very low saferadius values causing event clustering"
                    ))
                
                # WARNING: restock très faible (performance)
                if 0 < restock < 300:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Event '{event_name}' : restock ({restock}) très court",
                        line=idx,
                        field='restock',
                        suggestion="Valeurs trop courtes impactent les performances",
                        context="Doc: Use higher restock times to prevent server performance issues"
                    ))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def _validate_flags(self, event_elem, event_name: str, line: int) -> List[ValidationError]:
        """Valide les flags"""
        errors = []
        
        flags_elem = event_elem.find('flags')
        if flags_elem is not None:
            for flag_name in flags_elem.attrib:
                # Vérifier que le flag est connu
                if flag_name not in self.VALID_FLAGS:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Event '{event_name}' : flag '{flag_name}' inconnu",
                        line=line,
                        field='flags',
                        suggestion=f"Flags valides: {', '.join(self.VALID_FLAGS)}"
                    ))
                
                # Vérifier que la valeur est 0 ou 1
                value = flags_elem.get(flag_name)
                if value not in ['0', '1']:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Event '{event_name}' : flag '{flag_name}'='{value}' invalide",
                        line=line,
                        field='flags',
                        suggestion="Les flags doivent valoir 0 ou 1"
                    ))
        
        return errors
    
    def _validate_position(self, event_elem, event_name: str, line: int) -> List[ValidationError]:
        """Valide position"""
        errors = []
        
        position_elem = event_elem.find('position')
        if position_elem is not None:
            position = position_elem.text
            if position and position not in self.VALID_POSITIONS:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Event '{event_name}' : position '{position}' invalide",
                    line=line,
                    field='position',
                    suggestion="Valeurs valides: 'fixed' (coordonnées prédéfinies) ou 'random'",
                    context="Doc: 'fixed' uses cfgeventspawns.xml, 'random' allows spawn anywhere"
                ))
        
        return errors
    
    def _validate_limit(self, event_elem, event_name: str, line: int) -> List[ValidationError]:
        """Valide limit"""
        errors = []
        
        limit_elem = event_elem.find('limit')
        if limit_elem is not None:
            limit = limit_elem.text
            if limit and limit not in self.VALID_LIMITS:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Event '{event_name}' : limit '{limit}' invalide",
                    line=line,
                    field='limit',
                    suggestion="Valeurs valides: 'child', 'parent', 'mixed'",
                    context="Doc: Controls spawn limit behavior"
                ))
        
        return errors
    
    def _validate_active(self, event_elem, event_name: str, line: int) -> List[ValidationError]:
        """Valide active"""
        errors = []
        
        active_elem = event_elem.find('active')
        if active_elem is not None:
            active = active_elem.text
            if active and active not in ['0', '1']:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Event '{event_name}' : active '{active}' invalide",
                    line=line,
                    field='active',
                    suggestion="Valeurs valides: 0 (désactivé) ou 1 (activé)",
                    context="Doc: Master toggle for this event"
                ))
        
        return errors
