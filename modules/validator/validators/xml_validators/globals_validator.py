"""
globals_validator.py
Validateur pour globals.xml - Variables serveur globales

Source: DayZ Wiki - Central Economy Configuration
"""

import xml.etree.ElementTree as ET
from typing import List
from ...base_validator import BaseValidator, ValidationError


class GlobalsValidator(BaseValidator):
    """
    Validateur pour globals.xml
    Basé sur la documentation officielle Bohemia Interactive
    """
    
    # Variables définies dans la doc officielle
    VALID_VARIABLES = {
        # Nom: (type, min, max, default, description)
        'AnimalMaxCount': (0, 0, 10000, 200, "Maximal limit of spawned animals"),
        'CleanupAvoidance': (0, 0, 1000, 100, "Distance from player for item deletion (m)"),
        'CleanupLifetimeDeadAnimal': (0, 0, 86400, 1200, "Lifetime for dead animals (sec)"),
        'CleanupLifetimeDeadInfected': (0, 0, 86400, 330, "Lifetime for dead infected (sec)"),
        'CleanupLifetimeDeadPlayer': (0, 0, 86400, 3600, "Lifetime for dead player (sec)"),
        'CleanupLifetimeDefault': (0, 0, 86400, 45, "Default lifetime for damaged entities (sec)"),
        'CleanupLifetimeLimit': (0, 1, 1000, 50, "Max items deleted at once"),
        'CleanupLifetimeRuined': (0, 0, 86400, 330, "Lifetime for ruined loot (sec)"),
        'FlagRefreshFrequency': (0, 0, 999999, 432000, "Items refresh frequency (sec)"),
        'FlagRefreshMaxDuration': (0, 0, 9999999, 3456000, "Flag refresh duration (sec)"),
        'IdleModeCountdown': (0, 0, 3600, 60, "Idle mode activation time (sec)"),
        'IdleModeStartup': (0, 0, 1, 1, "Enable idle mode on startup (0/1)"),
        'InitialSpawn': (0, 0, 100, 100, "Initial loot spawn percentage (%)"),
        'LootProxyPlacement': (0, 0, 1, 1, "Allow containers to receive loot (0/1)"),
        'RespawnAttempt': (0, 1, 100, 2, "Attempts per item respawn"),
        'RespawnLimit': (0, 1, 1000, 20, "Max items of one type spawned at once"),
        'RespawnTypes': (0, 1, 100, 12, "Max different types respawned at once"),
        'RestartSpawn': (0, 0, 100, 0, "Loot respawn on restart (%)"),
        'SpawnInitial': (0, 0, 10000, 1200, "Initial spawn tests allowed"),
        'TimeHopping': (0, 0, 600, 60, "Server hopper penalty (sec)"),
        'TimeLogin': (0, 0, 65536, 15, "Login time (sec, max 65536)"),
        'TimeLogout': (0, 0, 65536, 15, "Logout time (sec, max 65536)"),
        'TimePenalty': (0, 0, 600, 20, "In-session penalty time (sec)"),
        'ZombieMaxCount': (0, 0, 10000, 1000, "Maximal spawned zombies"),
        'ZoneSpawnDist': (0, 0, 1000, 300, "Distance for infected spawn (m)"),
        'WorldWetTempUpdate': (0, 0, 1, 1, "Update wetness/temp on items (0/1)"),
        'FoodDecay': (0, 0, 1, 1, "Enable food decay (0/1)"),
        'LootDamageMin': (1, 0.0, 1.0, 0.0, "Min damage on spawned items (0-1)"),
        'LootDamageMax': (1, 0.0, 1.0, 0.0, "Max damage on spawned items (0-1)"),
        'LootSpawnAvoidance': (0, 0, 500, 50, "Distance from player for loot spawn (m)"),
    }
    
    def __init__(self, version: str = '1.28'):
        super().__init__('globals', version)
    
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
        """Valide la structure de globals.xml"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            # Vérifier balise racine
            if root.tag != 'variables':
                errors.append(ValidationError(
                    severity='error',
                    message=f"Balise racine invalide : '{root.tag}'. Attendu : 'variables'",
                    line=1,
                    suggestion="La balise racine doit être <variables>"
                ))
                return errors
            
            # Vérifier chaque variable
            for idx, var_elem in enumerate(root.findall('var'), start=1):
                var_name = var_elem.get('name')
                var_type = var_elem.get('type')
                var_value = var_elem.get('value')
                
                # Attribut 'name' requis
                if not var_name:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Variable #{idx} : attribut 'name' manquant",
                        line=idx,
                        suggestion="Format: <var name='VariableName' type='0' value='100'/>"
                    ))
                    continue
                
                # Attribut 'type' requis
                if not var_type:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Variable '{var_name}' : attribut 'type' manquant",
                        line=idx,
                        suggestion="Type: 0=integer, 1=float, 2=string"
                    ))
                
                # Attribut 'value' requis
                if not var_value:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Variable '{var_name}' : attribut 'value' manquant",
                        line=idx,
                        suggestion=f"Ajoutez value='...' (voir doc pour {var_name})"
                    ))
                
                # Vérifier type valide
                if var_type and var_type not in ['0', '1', '2']:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Variable '{var_name}' : type '{var_type}' invalide",
                        line=idx,
                        suggestion="Type valides: 0 (integer), 1 (float), 2 (string)",
                        context="Doc: 0 for integer, 1 for float, 2 for string"
                    ))
                
                # Warning si variable inconnue
                if var_name and var_name not in self.VALID_VARIABLES:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Variable '{var_name}' non documentée",
                        line=idx,
                        suggestion="Vérifiez l'orthographe ou consultez la doc DayZ"
                    ))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def validate_business_rules(self, content: str) -> List[ValidationError]:
        """Valide les règles métier selon doc Bohemia"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            for idx, var_elem in enumerate(root.findall('var'), start=1):
                var_name = var_elem.get('name')
                var_type = var_elem.get('type')
                var_value = var_elem.get('value')
                
                if not var_name or not var_type or not var_value:
                    continue
                
                # Vérifier variables connues
                if var_name in self.VALID_VARIABLES:
                    expected_type, min_val, max_val, default_val, description = self.VALID_VARIABLES[var_name]
                    
                    # RÈGLE 1: Type correct
                    if var_type != str(expected_type):
                        type_names = {0: 'integer', 1: 'float', 2: 'string'}
                        errors.append(ValidationError(
                            severity='error',
                            message=f"Variable '{var_name}' : type incorrect (trouvé {var_type}, attendu {expected_type})",
                            line=idx,
                            field=var_name,
                            suggestion=f"Type correct: {expected_type} ({type_names.get(expected_type, 'unknown')})",
                            context=description
                        ))
                        continue
                    
                    # RÈGLE 2: Valeur dans le range (integer/float)
                    if expected_type in [0, 1]:  # Integer ou Float
                        try:
                            if expected_type == 0:
                                value = int(var_value)
                            else:
                                value = float(var_value)
                            
                            if value < min_val or value > max_val:
                                errors.append(ValidationError(
                                    severity='error',
                                    message=f"Variable '{var_name}' : valeur {value} hors range [{min_val}-{max_val}]",
                                    line=idx,
                                    field=var_name,
                                    suggestion=f"Valeur vanilla: {default_val}, range valide: {min_val}-{max_val}",
                                    context=description
                                ))
                        
                        except (ValueError, TypeError):
                            errors.append(ValidationError(
                                severity='error',
                                message=f"Variable '{var_name}' : valeur '{var_value}' n'est pas un nombre valide",
                                line=idx,
                                field=var_name,
                                suggestion=f"Type attendu: {'integer' if expected_type == 0 else 'float'}"
                            ))
                    
                    # RÈGLE 3: Warning si très différent de la valeur vanilla
                    if expected_type == 0 and var_value.isdigit():
                        value = int(var_value)
                        if abs(value - default_val) > default_val * 3:  # 300% différence
                            errors.append(ValidationError(
                                severity='warning',
                                message=f"Variable '{var_name}' : valeur {value} très éloignée de vanilla ({default_val})",
                                line=idx,
                                field=var_name,
                                suggestion=f"Valeur vanilla: {default_val}",
                                context="Valeurs extrêmes peuvent causer des problèmes de performance"
                            ))
                
                # RÈGLES SPÉCIFIQUES
                
                # TimeLogin et TimeLogout : max 65536
                if var_name in ['TimeLogin', 'TimeLogout']:
                    if var_value.isdigit() and int(var_value) > 65536:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"Variable '{var_name}' : max 65536 (trouvé {var_value})",
                            line=idx,
                            field=var_name,
                            suggestion="Valeur max: 65536",
                            context="Doc: max value 65536"
                        ))
                
                # LootDamageMin ≤ LootDamageMax
                # (on vérifiera ça après avoir parcouru toutes les variables)
        
            # Vérifier LootDamageMin ≤ LootDamageMax
            damage_min = None
            damage_max = None
            
            for var_elem in root.findall('var'):
                var_name = var_elem.get('name')
                var_value = var_elem.get('value')
                
                if var_name == 'LootDamageMin':
                    try:
                        damage_min = float(var_value)
                    except:
                        pass
                
                if var_name == 'LootDamageMax':
                    try:
                        damage_max = float(var_value)
                    except:
                        pass
            
            if damage_min is not None and damage_max is not None:
                if damage_min > damage_max:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"LootDamageMin ({damage_min}) > LootDamageMax ({damage_max})",
                        field='LootDamageMin',
                        suggestion=f"LootDamageMin doit être ≤ {damage_max}",
                        context="Min ne peut pas être supérieur à Max"
                    ))
        
        except ET.ParseError:
            pass
        
        return errors
