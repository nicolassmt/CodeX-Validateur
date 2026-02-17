"""
cfgeffectarea_validator.py
Validateur pour cfgEffectArea.json - Zones contaminées

Source: DayZ Wiki - Contaminated Areas Configuration
"""

import json
from typing import List
from ...base_validator import BaseValidator, ValidationError


class CfgEffectAreaValidator(BaseValidator):
    """
    Validateur pour cfgEffectArea.json
    Basé sur la documentation officielle Bohemia Interactive
    
    Supporte:
    - Format v1.28+ (nouveau: FillWithParticles)
    - Format pré-1.28 (ancien: PlaceParticles)
    """
    
    # Types valides
    VALID_TYPES = [
        'ContaminatedArea_Static',
        'ContaminatedArea_Dynamic'
    ]
    
    VALID_TRIGGER_TYPES = [
        'ContaminatedTrigger',
        ''  # Vide = pas de trigger
    ]
    
    # Particules valides (doc)
    VALID_PARTICLES = [
        'graphics/particles/contaminated_area_gas_bigass',
        'graphics/particles/contaminated_area_gas_bigass_debug',
        'contaminated_area_gas_bigass',  # Ancien format
        'graphics/particles/contaminated_area_gas_around',
        'contaminated_area_gas_around',
        'graphics/particles/contaminated_area_gas_around_tiny',
        'contaminated_area_gas_around_tiny'
    ]
    
    # PPE valides
    VALID_PPE = [
        'PPERequester_ContaminatedAreaTint'
    ]
    
    def __init__(self, version: str = '1.28'):
        super().__init__('cfgeffectarea', version)
    
    def validate_syntax(self, content: str) -> List[ValidationError]:
        """Valide la syntaxe JSON"""
        errors = []
        
        try:
            data = json.loads(content)
            
            if not isinstance(data, dict):
                errors.append(ValidationError(
                    severity='error',
                    message=f"Le fichier doit être un objet JSON, pas {type(data).__name__}",
                    line=1,
                    suggestion="Format: { } ou { \"Areas\": [...] }",
                    context="Un JSON vide { } désactive les zones contaminées"
                ))
        
        except json.JSONDecodeError as e:
            errors.append(ValidationError(
                severity='error',
                message=f"Erreur de syntaxe JSON : {e.msg}",
                line=e.lineno,
                column=e.colno,
                suggestion=self._get_json_error_suggestion(e.msg),
                context="⚠️ JSON ne supporte PAS les commentaires (//, /* */)"
            ))
        
        return errors
    
    def validate_structure(self, content: str) -> List[ValidationError]:
        """Valide la structure selon doc Bohemia"""
        errors = []
        
        try:
            data = json.loads(content)
            
            # Fichier vide = OK (désactive les zones)
            if len(data) == 0:
                return []
            
            # Vérifier clé "Areas"
            if 'Areas' not in data:
                errors.append(ValidationError(
                    severity='warning',
                    message="Clé 'Areas' manquante",
                    suggestion='Ajoutez "Areas": [] ou laissez le fichier vide { }',
                    context="Fichier vide = zones contaminées désactivées"
                ))
                return errors
            
            areas = data['Areas']
            
            if not isinstance(areas, list):
                errors.append(ValidationError(
                    severity='error',
                    message=f"'Areas' doit être un array, pas {type(areas).__name__}",
                    suggestion='"Areas": []'
                ))
                return errors
            
            # Vérifier chaque zone
            for idx, area in enumerate(areas):
                errors.extend(self._validate_area(area, idx))
        
        except json.JSONDecodeError:
            pass
        
        return errors
    
    def validate_business_rules(self, content: str) -> List[ValidationError]:
        """Valide les règles métier"""
        errors = []
        
        try:
            data = json.loads(content)
            
            if 'Areas' not in data or not isinstance(data['Areas'], list):
                return []
            
            # RÈGLE: Max 1000 emitters per zone (doc v1.28)
            for idx, area in enumerate(data['Areas']):
                area_name = area.get('AreaName', f'Zone #{idx+1}')
                
                # Format v1.28+
                if 'Data' in area and isinstance(area['Data'], dict):
                    data_section = area['Data']
                    
                    # Vérifier Radius > 0
                    if 'Radius' in data_section:
                        radius = data_section['Radius']
                        if isinstance(radius, (int, float)) and radius <= 0:
                            errors.append(ValidationError(
                                severity='error',
                                message=f"Zone '{area_name}' : Radius ({radius}) doit être > 0",
                                field='Data.Radius',
                                suggestion="Rayon en mètres (ex: 150)"
                            ))
                    
                    # Vérifier Pos = [x, y, z]
                    if 'Pos' in data_section:
                        pos = data_section['Pos']
                        if not isinstance(pos, list):
                            errors.append(ValidationError(
                                severity='error',
                                message=f"Zone '{area_name}' : Pos doit être un array [x, y, z]",
                                field='Data.Pos',
                                suggestion='Format: "Pos": [7347, 0, 6410]'
                            ))
                        elif len(pos) != 3:
                            errors.append(ValidationError(
                                severity='error',
                                message=f"Zone '{area_name}' : Pos doit avoir EXACTEMENT 3 coordonnées [x, y, z], trouvé {len(pos)}",
                                field='Data.Pos',
                                suggestion='Format: "Pos": [x, y, z]'
                            ))
                    
                    # Warning sur performance (format ancien)
                    if 'InnerRingCount' in data_section or 'OuterPartDist' in data_section:
                        # Format pré-1.28 - estimer le nombre d'emitters
                        inner_count = data_section.get('InnerRingCount', 0)
                        if isinstance(inner_count, int) and inner_count > 10:
                            errors.append(ValidationError(
                                severity='warning',
                                message=f"Zone '{area_name}' : InnerRingCount ({inner_count}) très élevé",
                                field='Data.InnerRingCount',
                                suggestion="Plus de rings = plus d'emitters = impact performance",
                                context="Doc: max 1000 emitters par zone (v1.28+)"
                            ))
        
        except json.JSONDecodeError:
            pass
        
        return errors
    
    def _validate_area(self, area: dict, idx: int) -> List[ValidationError]:
        """Valide une zone individuelle"""
        errors = []
        
        area_name = area.get('AreaName', f'Zone #{idx+1}')
        
        # CHAMPS REQUIS
        required_fields = ['AreaName', 'Type', 'Data', 'PlayerData']
        
        for field in required_fields:
            if field not in area:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Zone #{idx+1} : champ requis '{field}' manquant",
                    field=field,
                    suggestion=f"Ajoutez \"{field}\": ... (voir doc)"
                ))
        
        # TYPE
        if 'Type' in area:
            area_type = area['Type']
            if area_type not in self.VALID_TYPES:
                errors.append(ValidationError(
                    severity='warning',
                    message=f"Zone '{area_name}' : Type '{area_type}' non standard",
                    field='Type',
                    suggestion=f"Types standards: {', '.join(self.VALID_TYPES)}"
                ))
        
        # TRIGGER TYPE
        if 'TriggerType' in area:
            trigger = area['TriggerType']
            if trigger not in self.VALID_TRIGGER_TYPES:
                errors.append(ValidationError(
                    severity='info',
                    message=f"Zone '{area_name}' : TriggerType '{trigger}' custom",
                    field='TriggerType',
                    context="Standard: 'ContaminatedTrigger' ou vide"
                ))
        
        # DATA SECTION
        if 'Data' in area and isinstance(area['Data'], dict):
            errors.extend(self._validate_data_section(area['Data'], area_name))
        
        # PLAYERDATA SECTION
        if 'PlayerData' in area and isinstance(area['PlayerData'], dict):
            errors.extend(self._validate_playerdata_section(area['PlayerData'], area_name))
        
        return errors
    
    def _validate_data_section(self, data: dict, area_name: str) -> List[ValidationError]:
        """Valide la section Data"""
        errors = []
        
        # DÉTECTION FORMAT (v1.28+ ou pré-1.28)
        is_new_format = 'InnerPartDist' in data and 'InnerRingCount' not in data
        
        if is_new_format:
            # FORMAT v1.28+ (FillWithParticles)
            required = ['Pos', 'Radius', 'InnerPartDist']
            recommended = ['PosHeight', 'NegHeight', 'OuterOffset', 'ParticleName']
        else:
            # FORMAT PRÉ-1.28 (PlaceParticles)
            required = ['Pos', 'Radius']
            recommended = ['InnerRingCount', 'InnerPartDist', 'OuterPartDist', 'ParticleName']
        
        # Champs requis
        for field in required:
            if field not in data:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Zone '{area_name}' : Data.{field} manquant",
                    field=f'Data.{field}',
                    suggestion=f"Champ requis pour {'v1.28+' if is_new_format else 'pré-1.28'}"
                ))
        
        # Champs recommandés
        for field in recommended:
            if field not in data:
                errors.append(ValidationError(
                    severity='info',
                    message=f"Zone '{area_name}' : Data.{field} absent (optionnel)",
                    field=f'Data.{field}'
                ))
        
        # Validation types
        if 'Pos' in data and isinstance(data['Pos'], list) and len(data['Pos']) == 3:
            # Vérifier que ce sont des nombres
            for i, coord in enumerate(data['Pos']):
                if not isinstance(coord, (int, float)):
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Zone '{area_name}' : Pos[{i}] doit être un nombre, pas {type(coord).__name__}",
                        field='Data.Pos'
                    ))
        
        # ParticleName
        if 'ParticleName' in data:
            particle = data['ParticleName']
            if particle not in self.VALID_PARTICLES:
                errors.append(ValidationError(
                    severity='info',
                    message=f"Zone '{area_name}' : ParticleName '{particle}' custom",
                    field='Data.ParticleName',
                    context="OK si particule custom, sinon vérifiez l'orthographe"
                ))
        
        return errors
    
    def _validate_playerdata_section(self, playerdata: dict, area_name: str) -> List[ValidationError]:
        """Valide la section PlayerData"""
        errors = []
        
        # Champs recommandés
        recommended = ['AroundPartName', 'TinyPartName', 'PPERequesterType']
        
        for field in recommended:
            if field not in playerdata:
                errors.append(ValidationError(
                    severity='info',
                    message=f"Zone '{area_name}' : PlayerData.{field} absent (optionnel)",
                    field=f'PlayerData.{field}'
                ))
        
        # PPERequesterType
        if 'PPERequesterType' in playerdata:
            ppe = playerdata['PPERequesterType']
            if ppe not in self.VALID_PPE:
                errors.append(ValidationError(
                    severity='info',
                    message=f"Zone '{area_name}' : PPERequesterType '{ppe}' custom",
                    field='PlayerData.PPERequesterType',
                    context="Standard: PPERequester_ContaminatedAreaTint"
                ))
        
        return errors
    
    def _get_json_error_suggestion(self, error_msg: str) -> str:
        """Suggère une correction selon l'erreur JSON"""
        if 'comment' in error_msg.lower():
            return "⚠️ JSON ne supporte PAS les commentaires - supprimez //, /* */"
        elif 'Expecting property name' in error_msg:
            return "Virgule en trop avant } ou ] ?"
        elif 'Expecting value' in error_msg:
            return "Valeur manquante après ':' ?"
        elif 'Extra data' in error_msg:
            return "Caractères en trop après la fin du JSON"
        else:
            return "Vérifiez les accolades { }, crochets [ ], virgules et guillemets"
