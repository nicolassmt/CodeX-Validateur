"""
cfggameplay_validator.py
Validateur pour cfggameplay.json

⚠️ CRITICITÉ MAXIMALE ⚠️
UNE SEULE ERREUR = FICHIER ENTIER IGNORÉ PAR LE JEU
Tous les changements (stamina, mappings, etc.) sont perdus
"""

import json
from typing import List
from ...base_validator import BaseValidator, ValidationError


class CfgGameplayValidator(BaseValidator):
    """
    Validateur pour cfggameplay.json
    
    ATTENTION CRITIQUE :
    Ce fichier est le PLUS sensible de DayZ.
    Une seule erreur de syntaxe = TOUT le fichier est ignoré.
    
    Impact : Stamina, mappings, spawns, météo, TOUT est perdu.
    """
    
    # Version supportées
    VERSION_MIN = 110
    VERSION_MAX = 135  # Future-proof
    
    # Sections requises
    REQUIRED_SECTIONS = [
        'version',
        'GeneralData',
        'PlayerData',
        'WorldsData'
    ]
    
    # Sections optionnelles mais courantes
    OPTIONAL_SECTIONS = [
        'BaseBuildingData',
        'UIData',
        'MapData',
        'TerritoryData',
        'PlayerSpawnGearPresetData',
        'SpawnGearPresetsData'
    ]
    
    def __init__(self, version: str = '1.28'):
        super().__init__('cfggameplay', version)
    
    def validate_syntax(self, content: str) -> List[ValidationError]:
        """Valide la syntaxe JSON - ULTRA-STRICT"""
        errors = []
        
        try:
            data = json.loads(content)
            
            # Vérifier que c'est un objet (pas array, string, etc.)
            if not isinstance(data, dict):
                errors.append(ValidationError(
                    severity='error',
                    message=f"Le fichier doit être un objet JSON, pas {type(data).__name__}",
                    line=1,
                    suggestion="Le fichier doit commencer par { et finir par }"
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
        """Valide la structure du cfggameplay.json"""
        errors = []
        
        try:
            data = json.loads(content)
            
            # VÉRIFIER VERSION (CRITIQUE)
            if 'version' not in data:
                errors.append(ValidationError(
                    severity='error',
                    message="Champ 'version' manquant",
                    field='version',
                    suggestion="Ajoutez: \"version\": 131",
                    context="La version est OBLIGATOIRE"
                ))
            else:
                version = data['version']
                if not isinstance(version, int):
                    errors.append(ValidationError(
                        severity='error',
                        message=f"'version' doit être un entier, pas {type(version).__name__}",
                        field='version',
                        suggestion=f"Changez \"version\": \"{version}\" en \"version\": {version}"
                    ))
                elif not (self.VERSION_MIN <= version <= self.VERSION_MAX):
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Version {version} inhabituelle (range normal: {self.VERSION_MIN}-{self.VERSION_MAX})",
                        field='version',
                        suggestion=f"Versions courantes: 131 (1.26+)"
                    ))
            
            # VÉRIFIER SECTIONS REQUISES
            for section in self.REQUIRED_SECTIONS:
                if section == 'version':  # Déjà vérifié
                    continue
                
                if section not in data:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Section requise '{section}' manquante",
                        field=section,
                        suggestion=f"Ajoutez la section {section} (voir vanilla cfggameplay.json)",
                        context=f"{section} est nécessaire pour le bon fonctionnement"
                    ))
                elif not isinstance(data[section], dict):
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Section '{section}' doit être un objet, pas {type(data[section]).__name__}",
                        field=section
                    ))
            
            # VALIDER SOUS-SECTIONS
            if 'PlayerData' in data and isinstance(data['PlayerData'], dict):
                errors.extend(self._validate_player_data(data['PlayerData']))
            
            if 'WorldsData' in data and isinstance(data['WorldsData'], dict):
                errors.extend(self._validate_worlds_data(data['WorldsData']))
            
            if 'GeneralData' in data and isinstance(data['GeneralData'], dict):
                errors.extend(self._validate_general_data(data['GeneralData']))
        
        except json.JSONDecodeError:
            # Déjà géré dans validate_syntax
            pass
        
        return errors
    
    def validate_business_rules(self, content: str) -> List[ValidationError]:
        """Valide les règles métier DayZ pour cfggameplay.json"""
        errors = []
        
        try:
            data = json.loads(content)
            
            # RÈGLE : environmentTemps doit avoir 12 valeurs (1 par mois)
            if 'WorldsData' in data:
                worlds = data['WorldsData']
                
                if 'environmentMinTemps' in worlds:
                    min_temps = worlds['environmentMinTemps']
                    if not isinstance(min_temps, list):
                        errors.append(ValidationError(
                            severity='error',
                            message="environmentMinTemps doit être un array",
                            field='WorldsData.environmentMinTemps'
                        ))
                    elif len(min_temps) != 12:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"environmentMinTemps doit avoir 12 valeurs (1 par mois), trouvé {len(min_temps)}",
                            field='WorldsData.environmentMinTemps',
                            suggestion="Format: [-3, -2, 0, 4, 9, 14, 18, 17, 12, 7, 4, 0]"
                        ))
                
                if 'environmentMaxTemps' in worlds:
                    max_temps = worlds['environmentMaxTemps']
                    if not isinstance(max_temps, list):
                        errors.append(ValidationError(
                            severity='error',
                            message="environmentMaxTemps doit être un array",
                            field='WorldsData.environmentMaxTemps'
                        ))
                    elif len(max_temps) != 12:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"environmentMaxTemps doit avoir 12 valeurs (1 par mois), trouvé {len(max_temps)}",
                            field='WorldsData.environmentMaxTemps',
                            suggestion="Format: [3, 5, 7, 14, 19, 24, 26, 25, 21, 16, 10, 5]"
                        ))
                
                # RÈGLE : minTemps ≤ maxTemps pour chaque mois
                if ('environmentMinTemps' in worlds and 'environmentMaxTemps' in worlds and
                    isinstance(worlds['environmentMinTemps'], list) and isinstance(worlds['environmentMaxTemps'], list) and
                    len(worlds['environmentMinTemps']) == 12 and len(worlds['environmentMaxTemps']) == 12):
                    
                    for month in range(12):
                        min_temp = worlds['environmentMinTemps'][month]
                        max_temp = worlds['environmentMaxTemps'][month]
                        
                        if min_temp > max_temp:
                            month_names = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 
                                          'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
                            errors.append(ValidationError(
                                severity='error',
                                message=f"{month_names[month]} : minTemp ({min_temp}°C) > maxTemp ({max_temp}°C)",
                                field=f'WorldsData.environmentTemps[{month}]',
                                suggestion=f"Corrigez : minTemp doit être ≤ {max_temp} ou maxTemp ≥ {min_temp}"
                            ))
                
                # RÈGLE : wetnessWeightModifiers doit avoir 5 valeurs
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
                            message=f"wetnessWeightModifiers doit avoir 5 valeurs, trouvé {len(wetness)}",
                            field='WorldsData.wetnessWeightModifiers',
                            suggestion="Format: [1.0, 1.0, 1.33, 1.66, 2.0]"
                        ))
        
        except json.JSONDecodeError:
            # Déjà géré
            pass
        
        return errors
    
    def _validate_player_data(self, player_data: dict) -> List[ValidationError]:
        """Valide la section PlayerData"""
        errors = []
        
        # StaminaData
        if 'StaminaData' in player_data and isinstance(player_data['StaminaData'], dict):
            stamina = player_data['StaminaData']
            
            # staminaMax CRITIQUE (souvent modifié, souvent cassé)
            if 'staminaMax' in stamina:
                max_val = stamina['staminaMax']
                if not isinstance(max_val, (int, float)):
                    errors.append(ValidationError(
                        severity='error',
                        message=f"staminaMax doit être un nombre, pas {type(max_val).__name__}",
                        field='PlayerData.StaminaData.staminaMax'
                    ))
                elif max_val > 100:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"staminaMax ({max_val}) ne peut pas dépasser 100",
                        field='PlayerData.StaminaData.staminaMax',
                        suggestion="Valeur max: 100.0 (c'est un pourcentage)",
                        context="Valeurs > 100 causent des bugs in-game"
                    ))
                elif max_val <= 0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"staminaMax ({max_val}) doit être > 0",
                        field='PlayerData.StaminaData.staminaMax',
                        suggestion="Valeur vanilla: 100.0"
                    ))
        
        return errors
    
    def _validate_worlds_data(self, worlds_data: dict) -> List[ValidationError]:
        """Valide la section WorldsData"""
        errors = []
        
        # lightingConfig
        if 'lightingConfig' in worlds_data:
            lighting = worlds_data['lightingConfig']
            if not isinstance(lighting, int):
                errors.append(ValidationError(
                    severity='error',
                    message=f"lightingConfig doit être un entier (0, 1, ou 2), pas {type(lighting).__name__}",
                    field='WorldsData.lightingConfig'
                ))
            elif lighting not in [0, 1, 2]:
                errors.append(ValidationError(
                    severity='warning',
                    message=f"lightingConfig={lighting} inhabituel (valeurs normales: 0, 1, ou 2)",
                    field='WorldsData.lightingConfig'
                ))
        
        return errors
    
    def _validate_general_data(self, general_data: dict) -> List[ValidationError]:
        """Valide la section GeneralData"""
        errors = []
        
        # Flags booléens (doivent être 0 ou 1, pas true/false)
        bool_fields = ['disableBaseDamage', 'disableContainerDamage', 'disableRespawnDialog']
        
        for field in bool_fields:
            if field in general_data:
                value = general_data[field]
                if not isinstance(value, int):
                    errors.append(ValidationError(
                        severity='error',
                        message=f"{field} doit être 0 ou 1 (int), pas {type(value).__name__}",
                        field=f'GeneralData.{field}',
                        suggestion=f"Changez \"true\"/\"false\" en 1/0"
                    ))
                elif value not in [0, 1]:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"{field}={value} inhabituel (valeurs normales: 0 ou 1)",
                        field=f'GeneralData.{field}'
                    ))
        
        return errors
    
    def _get_json_error_suggestion(self, error_msg: str) -> str:
        """Suggère une correction selon l'erreur JSON"""
        if 'Expecting property name' in error_msg:
            return "Virgule en trop ? Vérifiez qu'il n'y a pas de ',' avant '}'  ou ']'"
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
