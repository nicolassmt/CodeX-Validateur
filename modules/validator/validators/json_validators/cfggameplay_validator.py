"""
cfggameplay_validator.py
Validateur pour cfggameplay.json - BASÉ SUR DOC OFFICIELLE BOHEMIA

⚠️ CRITICITÉ MAXIMALE ⚠️
UNE SEULE ERREUR = FICHIER ENTIER IGNORÉ PAR LE JEU

Source: https://community.bistudio.com/wiki/DayZ:Crafting_Configuration
"""

import json
import re
from typing import List
from ...base_validator import BaseValidator, ValidationError


class CfgGameplayValidator(BaseValidator):
    """
    Validateur pour cfggameplay.json
    Basé sur la documentation officielle Bohemia Interactive
    """
    
    # Version supportées (doc officielle mentionne 119+)
    VERSION_MIN = 110
    VERSION_MAX = 140  # Future-proof
    
    # Sections requises (selon doc)
    REQUIRED_SECTIONS = ['version']
    
    # Sections communes (optionnelles)
    COMMON_SECTIONS = [
        'GeneralData', 'PlayerData', 'WorldsData', 'BaseBuildingData',
        'UIData', 'MapData', 'VehicleData'
    ]
    
    def __init__(self, version: str = '1.28'):
        super().__init__('cfggameplay', version)
    
    def validate_syntax(self, content: str) -> List[ValidationError]:
        """Valide la syntaxe JSON - ULTRA-STRICT"""
        errors = []
        
        try:
            data = json.loads(content)
            
            if not isinstance(data, dict):
                errors.append(ValidationError(
                    severity='error',
                    message=f"Le fichier doit être un objet JSON, pas {type(data).__name__}",
                    line=1,
                    suggestion="Le fichier doit commencer par { et finir par }",
                    context="⚠️ CRITIQUE : Une erreur JSON = fichier entier ignoré par DayZ"
                ))
        
        except json.JSONDecodeError as e:
            errors.append(ValidationError(
                severity='error',
                message=f"Erreur de syntaxe JSON : {e.msg}",
                line=e.lineno,
                column=e.colno,
                suggestion=self._get_json_error_suggestion(e.msg),
                context="⚠️ CRITIQUE : Une erreur JSON = fichier entier ignoré par DayZ"
            ))
        
        return errors
    
    def validate_structure(self, content: str) -> List[ValidationError]:
        """Valide la structure selon doc Bohemia"""
        errors = []
        
        try:
            data = json.loads(content)
            
            # VERSION (seul champ vraiment requis)
            if 'version' not in data:
                errors.append(ValidationError(
                    severity='error',
                    message="Champ 'version' manquant (REQUIS)",
                    field='version',
                    suggestion='Ajoutez: "version": 131',
                    context="La version est OBLIGATOIRE selon doc Bohemia"
                ))
            else:
                version = data['version']
                if not isinstance(version, int):
                    errors.append(ValidationError(
                        severity='error',
                        message=f"'version' doit être un entier, pas {type(version).__name__}",
                        field='version',
                        suggestion=f'Changez "version": "{version}" en "version": {version}'
                    ))
                elif version < self.VERSION_MIN:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Version {version} très ancienne (minimum recommandé: {self.VERSION_MIN})",
                        field='version',
                        suggestion="Mettez à jour vers version 131+"
                    ))
            
            # VALIDER SOUS-SECTIONS SI PRÉSENTES
            if 'PlayerData' in data and isinstance(data['PlayerData'], dict):
                errors.extend(self._validate_player_data(data['PlayerData']))
            
            if 'WorldsData' in data and isinstance(data['WorldsData'], dict):
                errors.extend(self._validate_worlds_data(data['WorldsData']))
            
            if 'GeneralData' in data and isinstance(data['GeneralData'], dict):
                errors.extend(self._validate_general_data(data['GeneralData']))
            
            if 'BaseBuildingData' in data and isinstance(data['BaseBuildingData'], dict):
                errors.extend(self._validate_basebuilding_data(data['BaseBuildingData']))
            
            if 'UIData' in data and isinstance(data['UIData'], dict):
                errors.extend(self._validate_ui_data(data['UIData']))
            
            if 'MapData' in data and isinstance(data['MapData'], dict):
                errors.extend(self._validate_map_data(data['MapData']))
        
        except json.JSONDecodeError:
            pass
        
        return errors
    
    def validate_business_rules(self, content: str) -> List[ValidationError]:
        """Valide les règles métier selon doc Bohemia"""
        errors = []
        
        try:
            data = json.loads(content)
            
            # RÈGLE : environmentTemps = EXACTEMENT 12 valeurs (doc: "12 values exactly")
            if 'WorldsData' in data:
                worlds = data['WorldsData']
                
                if 'environmentMinTemps' in worlds:
                    min_temps = worlds['environmentMinTemps']
                    if not isinstance(min_temps, list):
                        errors.append(ValidationError(
                            severity='error',
                            message="environmentMinTemps doit être un array",
                            field='WorldsData.environmentMinTemps',
                            context="Doc Bohemia: 'List of minimal temperatures (12 values exactly)'"
                        ))
                    elif len(min_temps) != 12:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"environmentMinTemps doit avoir EXACTEMENT 12 valeurs (1 par mois), trouvé {len(min_temps)}",
                            field='WorldsData.environmentMinTemps',
                            suggestion="Format: [-3, -2, 0, 4, 9, 14, 18, 17, 12, 7, 4, 0]",
                            context="Doc Bohemia: '12 values exactly'"
                        ))
                
                if 'environmentMaxTemps' in worlds:
                    max_temps = worlds['environmentMaxTemps']
                    if not isinstance(max_temps, list):
                        errors.append(ValidationError(
                            severity='error',
                            message="environmentMaxTemps doit être un array",
                            field='WorldsData.environmentMaxTemps',
                            context="Doc Bohemia: 'List of maximal temperatures (12 values exactly)'"
                        ))
                    elif len(max_temps) != 12:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"environmentMaxTemps doit avoir EXACTEMENT 12 valeurs (1 par mois), trouvé {len(max_temps)}",
                            field='WorldsData.environmentMaxTemps',
                            suggestion="Format: [3, 5, 7, 14, 19, 24, 26, 25, 21, 16, 10, 5]",
                            context="Doc Bohemia: '12 values exactly'"
                        ))
                
                # RÈGLE : wetnessWeightModifiers = EXACTEMENT 5 valeurs
                if 'wetnessWeightModifiers' in worlds:
                    wetness = worlds['wetnessWeightModifiers']
                    if not isinstance(wetness, list):
                        errors.append(ValidationError(
                            severity='error',
                            message="wetnessWeightModifiers doit être un array",
                            field='WorldsData.wetnessWeightModifiers'
                        ))
                    elif len(wetness) != 5:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"wetnessWeightModifiers doit avoir EXACTEMENT 5 valeurs [DRY, DAMP, WET, SOAKED, DRENCHED], trouvé {len(wetness)}",
                            field='WorldsData.wetnessWeightModifiers',
                            suggestion="Format: [1.0, 1.0, 1.33, 1.66, 2.0]",
                            context="Doc Bohemia: 'Values ... [DRY, DAMP, WET, SOAKED, DRENCHED]'"
                        ))
        
        except json.JSONDecodeError:
            pass
        
        return errors
    
    def _validate_player_data(self, player_data: dict) -> List[ValidationError]:
        """Valide PlayerData selon doc Bohemia"""
        errors = []
        
        # STAMINA DATA
        if 'StaminaData' in player_data and isinstance(player_data['StaminaData'], dict):
            stamina = player_data['StaminaData']
            
            # staminaMax (Doc: "setting to 0 may produce unexpected results")
            if 'staminaMax' in stamina:
                max_val = stamina['staminaMax']
                if not isinstance(max_val, (int, float)):
                    errors.append(ValidationError(
                        severity='error',
                        message=f"staminaMax doit être un nombre, pas {type(max_val).__name__}",
                        field='PlayerData.StaminaData.staminaMax'
                    ))
                elif max_val == 0:
                    errors.append(ValidationError(
                        severity='error',
                        message="staminaMax = 0 produira des résultats inattendus",
                        field='PlayerData.StaminaData.staminaMax',
                        suggestion="Valeur vanilla: 100.0",
                        context="Doc Bohemia: 'setting to 0 may produce unexpected results'"
                    ))
                elif max_val < 0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"staminaMax ({max_val}) ne peut pas être négatif",
                        field='PlayerData.StaminaData.staminaMax'
                    ))
                elif max_val > 1000:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"staminaMax ({max_val}) très élevé (vanilla: 100.0)",
                        field='PlayerData.StaminaData.staminaMax',
                        suggestion="Valeurs extrêmes peuvent causer des bugs"
                    ))
            
            # staminaMinCap (Doc: "setting to 0 may produce unexpected results")
            if 'staminaMinCap' in stamina:
                min_cap = stamina['staminaMinCap']
                if isinstance(min_cap, (int, float)) and min_cap == 0:
                    errors.append(ValidationError(
                        severity='warning',
                        message="staminaMinCap = 0 peut produire des résultats inattendus",
                        field='PlayerData.StaminaData.staminaMinCap',
                        suggestion="Valeur vanilla: 5.0",
                        context="Doc Bohemia: 'setting to 0 may produce unexpected results'"
                    ))
        
        # MOVEMENT DATA
        if 'MovementData' in player_data and isinstance(player_data['MovementData'], dict):
            movement = player_data['MovementData']
            
            # Valeurs avec min 0.01
            min_values = {
                'timeToStrafeJog': 0.01,
                'rotationSpeedJog': 0.01,
                'timeToSprint': 0.01,
                'timeToStrafeSprint': 0.01,
                'rotationSpeedSprint': 0.01
            }
            
            for field, min_val in min_values.items():
                if field in movement:
                    value = movement[field]
                    if isinstance(value, (int, float)) and value < min_val:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"{field} ({value}) doit être >= {min_val}",
                            field=f'PlayerData.MovementData.{field}',
                            suggestion=f"Valeur minimale: {min_val}",
                            context=f"Doc Bohemia: 'min possible value {min_val}'"
                        ))
        
        return errors
    
    def _validate_worlds_data(self, worlds_data: dict) -> List[ValidationError]:
        """Valide WorldsData selon doc Bohemia"""
        errors = []
        
        # lightingConfig (Doc: "0 = bright, 1 = dark")
        if 'lightingConfig' in worlds_data:
            lighting = worlds_data['lightingConfig']
            if not isinstance(lighting, int):
                errors.append(ValidationError(
                    severity='error',
                    message=f"lightingConfig doit être un entier (0 ou 1), pas {type(lighting).__name__}",
                    field='WorldsData.lightingConfig',
                    context="Doc Bohemia: '0 = bright, 1 = dark'"
                ))
            elif lighting not in [0, 1]:
                errors.append(ValidationError(
                    severity='warning',
                    message=f"lightingConfig={lighting} inhabituel (valeurs documentées: 0=bright, 1=dark)",
                    field='WorldsData.lightingConfig'
                ))
        
        return errors
    
    def _validate_general_data(self, general_data: dict) -> List[ValidationError]:
        """Valide GeneralData - Accepte bool ET int"""
        errors = []
        
        # Flags booléens (Doc: accepte "0/false" et "1/true")
        bool_fields = [
            'disableBaseDamage', 'disableContainerDamage', 
            'disableRespawnDialog', 'disableRespawnInUnconsciousness',
            'disablePersonalLight'
        ]
        
        for field in bool_fields:
            if field in general_data:
                value = general_data[field]
                # Accepter bool OU int (0/1)
                if not isinstance(value, (bool, int)):
                    errors.append(ValidationError(
                        severity='error',
                        message=f"{field} doit être bool (true/false) ou int (0/1), pas {type(value).__name__}",
                        field=f'GeneralData.{field}',
                        suggestion="Utilisez true/false ou 0/1"
                    ))
                elif isinstance(value, int) and value not in [0, 1]:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"{field}={value} inhabituel (valeurs normales: 0/1 ou true/false)",
                        field=f'GeneralData.{field}'
                    ))
        
        return errors
    
    def _validate_basebuilding_data(self, basebuilding_data: dict) -> List[ValidationError]:
        """Valide BaseBuildingData"""
        errors = []
        
        if 'HologramData' in basebuilding_data:
            hologram = basebuilding_data['HologramData']
            
            # disallowedTypesInUnderground (Doc: array de strings)
            if 'disallowedTypesInUnderground' in hologram:
                disallowed = hologram['disallowedTypesInUnderground']
                if not isinstance(disallowed, list):
                    errors.append(ValidationError(
                        severity='error',
                        message="disallowedTypesInUnderground doit être un array",
                        field='BaseBuildingData.HologramData.disallowedTypesInUnderground',
                        suggestion='Format: ["FenceKit","TerritoryFlagKit","WatchtowerKit"]'
                    ))
        
        return errors
    
    def _validate_ui_data(self, ui_data: dict) -> List[ValidationError]:
        """Valide UIData"""
        errors = []
        
        if 'HitIndicationData' in ui_data:
            hit_data = ui_data['HitIndicationData']
            
            # hitDirectionBehaviour (Doc: "0 == Disabled, 1 == Static, 2 == Dynamic")
            if 'hitDirectionBehaviour' in hit_data:
                value = hit_data['hitDirectionBehaviour']
                if not isinstance(value, int):
                    errors.append(ValidationError(
                        severity='error',
                        message=f"hitDirectionBehaviour doit être un int (0, 1, ou 2), pas {type(value).__name__}",
                        field='UIData.HitIndicationData.hitDirectionBehaviour'
                    ))
                elif value not in [0, 1, 2]:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"hitDirectionBehaviour={value} invalide (0=Disabled, 1=Static, 2=Dynamic)",
                        field='UIData.HitIndicationData.hitDirectionBehaviour',
                        context="Doc Bohemia: '0 == Disabled, 1 == Static, 2 == Dynamic'"
                    ))
            
            # hitDirectionStyle (Doc: "0 == 'splash', 1 == 'spike', 2 == 'arrow'")
            if 'hitDirectionStyle' in hit_data:
                value = hit_data['hitDirectionStyle']
                if not isinstance(value, int):
                    errors.append(ValidationError(
                        severity='error',
                        message=f"hitDirectionStyle doit être un int (0, 1, ou 2), pas {type(value).__name__}",
                        field='UIData.HitIndicationData.hitDirectionStyle'
                    ))
                elif value not in [0, 1, 2]:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"hitDirectionStyle={value} invalide (0=splash, 1=spike, 2=arrow)",
                        field='UIData.HitIndicationData.hitDirectionStyle',
                        context="Doc Bohemia: \"0 == 'splash', 1 == 'spike', 2 == 'arrow'\""
                    ))
            
            # hitDirectionIndicatorColorStr (Doc: format ARGB "0xFFFF0000")
            if 'hitDirectionIndicatorColorStr' in hit_data:
                color = hit_data['hitDirectionIndicatorColorStr']
                if not isinstance(color, str):
                    errors.append(ValidationError(
                        severity='error',
                        message=f"hitDirectionIndicatorColorStr doit être une string ARGB, pas {type(color).__name__}",
                        field='UIData.HitIndicationData.hitDirectionIndicatorColorStr',
                        suggestion='Format: "0xFFFF0000" (ARGB)'
                    ))
                elif not re.match(r'^0x[0-9A-Fa-f]{8}$', color):
                    errors.append(ValidationError(
                        severity='error',
                        message=f"hitDirectionIndicatorColorStr='{color}' format ARGB invalide",
                        field='UIData.HitIndicationData.hitDirectionIndicatorColorStr',
                        suggestion='Format: "0xAARRGGBB" (ex: "0xFFFF0000" pour rouge)',
                        context="Doc Bohemia: format ARGB = 0x + AA + RR + GG + BB"
                    ))
        
        return errors
    
    def _validate_map_data(self, map_data: dict) -> List[ValidationError]:
        """Valide MapData"""
        # Tous les champs sont booléens, accepter bool ET int
        return []
    
    def _get_json_error_suggestion(self, error_msg: str) -> str:
        """Suggère une correction selon l'erreur JSON"""
        if 'Expecting property name' in error_msg:
            return "Virgule en trop ? Vérifiez qu'il n'y a pas de ',' avant '}' ou ']'"
        elif 'Expecting value' in error_msg:
            return "Valeur manquante après ':' ou virgule en trop"
        elif 'Extra data' in error_msg:
            return "Caractères après la fin du JSON (accolade/crochet en trop ?)"
        elif 'Unterminated string' in error_msg:
            return "Guillemet de fermeture manquant sur une string"
        elif 'Expecting' in error_msg and 'delimiter' in error_msg:
            return "Virgule manquante entre deux éléments ?"
        else:
            return "Vérifiez les accolades { }, crochets [ ], virgules et guillemets"
