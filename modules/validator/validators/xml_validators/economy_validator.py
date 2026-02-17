"""
economy_validator.py
Validateur pour economy.xml (cfgEconomyCore.xml)

Source: DayZ Wiki - Central Economy Configuration
"""

import xml.etree.ElementTree as ET
from typing import List
from ...base_validator import BaseValidator, ValidationError


class EconomyValidator(BaseValidator):
    """
    Validateur pour economy.xml (cfgEconomyCore.xml)
    Basé sur la documentation officielle Bohemia Interactive
    """
    
    # Rootclasses valides (doc officielle)
    VALID_ROOTCLASSES = {
        'DefaultWeapon': {'act': None},
        'DefaultMagazine': {'act': None},
        'HouseNoDestruct': {'act': None, 'reportMemoryLOD': 'no'},
        'Inventory_Base': {'act': None},
        'SurvivorBase': {'act': 'character'},
        'DZ_LightAI': {'act': 'character'},
        'Car_DZ': {'act': 'car'},
    }
    
    # Defaults valides (doc officielle)
    VALID_DEFAULTS = {
        'world_segments': (int, 1, 100, 12, "World segments count"),
        'backup_period': (int, 15, 3600, 60, "Backup period (minutes)"),
        'backup_count': (int, 1, 100, 12, "Backups to keep"),
        'backup_startup': (bool, None, None, False, "Backup on startup"),
        'dyn_radius': (float, 1.0, 1000.0, 20.0, "Dynamic zone radius (m)"),
        'dyn_smin': (float, 0.0, 100.0, 0.0, "Dynamic zone min static"),
        'dyn_smax': (float, 0.0, 100.0, 0.0, "Dynamic zone max static"),
        'dyn_dmin': (float, 0.0, 100.0, 0.0, "Dynamic zone min dynamic"),
        'dyn_dmax': (float, 0.0, 100.0, 5.0, "Dynamic zone max dynamic"),
        'save_events_startup': (bool, None, None, True, "Save events on startup"),
        'save_types_startup': (bool, None, None, True, "Save types on startup"),
        'log_hivewarning': (bool, None, None, True, "Log hive warnings"),
        'log_storageinfo': (bool, None, None, False, "Log storage info"),
        'log_missionfilewarning': (bool, None, None, True, "Log mission file warnings"),
        'log_celoop': (bool, None, None, False, "Log CE loop"),
        'log_ce_dynamicevent': (bool, None, None, False, "Log dynamic events"),
        'log_ce_vehicle': (bool, None, None, False, "Log vehicle CE"),
        'log_ce_lootspawn': (bool, None, None, False, "Log loot spawn"),
        'log_ce_lootcleanup': (bool, None, None, False, "Log cleanup"),
        'log_ce_lootrespawn': (bool, None, None, False, "Log loot respawn"),
        'log_ce_statistics': (bool, None, None, False, "Log statistics"),
        'log_ce_zombie': (bool, None, None, False, "Log infected"),
        'log_ce_animal': (bool, None, None, False, "Log animal"),
    }
    
    def __init__(self, version: str = '1.28'):
        super().__init__('economy', version)
    
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
        """Valide la structure de economy.xml"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            # Vérifier balise racine
            if root.tag != 'economycore':
                errors.append(ValidationError(
                    severity='error',
                    message=f"Balise racine invalide : '{root.tag}'. Attendu : 'economycore'",
                    line=1,
                    suggestion="La balise racine doit être <economycore>"
                ))
                return errors
            
            # Vérifier section <classes>
            classes_elem = root.find('classes')
            if classes_elem is None:
                errors.append(ValidationError(
                    severity='warning',
                    message="Section <classes> manquante",
                    suggestion="Ajoutez <classes>...</classes> avec les rootclasses",
                    context="Optionnel mais recommandé pour définir les entités CE"
                ))
            else:
                errors.extend(self._validate_classes(classes_elem))
            
            # Vérifier section <defaults>
            defaults_elem = root.find('defaults')
            if defaults_elem is None:
                errors.append(ValidationError(
                    severity='info',
                    message="Section <defaults> manquante",
                    suggestion="Ajoutez <defaults>...</defaults> pour personnaliser les valeurs",
                    context="Optionnel, valeurs par défaut seront utilisées"
                ))
            else:
                errors.extend(self._validate_defaults(defaults_elem))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def validate_business_rules(self, content: str) -> List[ValidationError]:
        """Valide les règles métier"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            defaults_elem = root.find('defaults')
            if defaults_elem is not None:
                # Vérifier backup_period ≥ 15 (doc: "Minimum value 15")
                for default in defaults_elem.findall('default'):
                    name = default.get('name')
                    value = default.get('value')
                    
                    if name == 'backup_period':
                        try:
                            period = int(value)
                            if period < 15:
                                errors.append(ValidationError(
                                    severity='error',
                                    message=f"backup_period ({period}) doit être ≥ 15 minutes",
                                    field='backup_period',
                                    suggestion="Valeur minimale: 15",
                                    context="Doc: Minimum value '15'"
                                ))
                        except ValueError:
                            pass
                    
                    # Vérifier world_segments > 0
                    if name == 'world_segments':
                        try:
                            segments = int(value)
                            if segments <= 0:
                                errors.append(ValidationError(
                                    severity='error',
                                    message=f"world_segments ({segments}) doit être > 0",
                                    field='world_segments',
                                    suggestion="Valeur vanilla (Chernarus): 12"
                                ))
                        except ValueError:
                            pass
        
        except ET.ParseError:
            pass
        
        return errors
    
    def _validate_classes(self, classes_elem) -> List[ValidationError]:
        """Valide la section <classes>"""
        errors = []
        
        for idx, rootclass in enumerate(classes_elem.findall('rootclass'), start=1):
            name = rootclass.get('name')
            act = rootclass.get('act')
            report_lod = rootclass.get('reportMemoryLOD')
            
            # Attribut 'name' requis
            if not name:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Rootclass #{idx} : attribut 'name' manquant",
                    suggestion="Format: <rootclass name='ClassName'/>"
                ))
                continue
            
            # Vérifier 'act' si présent
            if act and act not in ['character', 'car', 'none']:
                errors.append(ValidationError(
                    severity='warning',
                    message=f"Rootclass '{name}' : act='{act}' inhabituel",
                    suggestion="Valeurs standards: 'character', 'car' (ou omis pour loot)",
                    context="Doc: act types: none/character/car"
                ))
            
            # Warning si rootclass non standard
            if name not in self.VALID_ROOTCLASSES:
                errors.append(ValidationError(
                    severity='info',
                    message=f"Rootclass '{name}' personnalisée (non vanilla)",
                    context="OK si c'est un mod, sinon vérifiez l'orthographe"
                ))
        
        return errors
    
    def _validate_defaults(self, defaults_elem) -> List[ValidationError]:
        """Valide la section <defaults>"""
        errors = []
        
        for idx, default in enumerate(defaults_elem.findall('default'), start=1):
            name = default.get('name')
            value = default.get('value')
            
            # Attributs requis
            if not name:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Default #{idx} : attribut 'name' manquant",
                    suggestion="Format: <default name='variable' value='valeur'/>"
                ))
                continue
            
            if not value:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Default '{name}' : attribut 'value' manquant",
                    suggestion=f"Ajoutez value='...' (voir doc pour {name})"
                ))
                continue
            
            # Vérifier variables connues
            if name in self.VALID_DEFAULTS:
                expected_type, min_val, max_val, default_val, description = self.VALID_DEFAULTS[name]
                
                # Validation selon le type
                if expected_type == int:
                    try:
                        val = int(value)
                        if min_val is not None and max_val is not None:
                            if val < min_val or val > max_val:
                                errors.append(ValidationError(
                                    severity='error',
                                    message=f"Default '{name}' : valeur {val} hors range [{min_val}-{max_val}]",
                                    field=name,
                                    suggestion=f"Valeur vanilla: {default_val}",
                                    context=description
                                ))
                    except ValueError:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"Default '{name}' : '{value}' n'est pas un entier",
                            field=name,
                            suggestion="Type attendu: integer"
                        ))
                
                elif expected_type == float:
                    try:
                        val = float(value)
                        if min_val is not None and max_val is not None:
                            if val < min_val or val > max_val:
                                errors.append(ValidationError(
                                    severity='error',
                                    message=f"Default '{name}' : valeur {val} hors range [{min_val}-{max_val}]",
                                    field=name,
                                    suggestion=f"Valeur vanilla: {default_val}",
                                    context=description
                                ))
                    except ValueError:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"Default '{name}' : '{value}' n'est pas un nombre",
                            field=name,
                            suggestion="Type attendu: float"
                        ))
                
                elif expected_type == bool:
                    if value.lower() not in ['true', 'false', 'on', 'off', '0', '1']:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"Default '{name}' : '{value}' n'est pas un booléen valide",
                            field=name,
                            suggestion="Valeurs valides: true/false, on/off, 0/1"
                        ))
            
            else:
                errors.append(ValidationError(
                    severity='info',
                    message=f"Default '{name}' non documenté",
                    context="Variable custom ou version plus récente"
                ))
        
        return errors
