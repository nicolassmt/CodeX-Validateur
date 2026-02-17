"""
cfgweather_validator.py
Validateur pour cfgweather.xml - Configuration météo

Source: DayZ Wiki - cfgweather.xml Configuration
"""

import xml.etree.ElementTree as ET
from typing import List
from ...base_validator import BaseValidator, ValidationError


class CfgWeatherValidator(BaseValidator):
    """
    Validateur pour cfgweather.xml
    Basé sur la documentation officielle DayZ
    
    NOTE: Ce fichier contrôle la météo dynamique du serveur
    """
    
    # Éléments météo requis
    WEATHER_ELEMENTS = ['overcast', 'fog', 'rain', 'windMagnitude', 'windDirection', 'snowfall']
    
    # Sous-éléments requis pour chaque élément météo
    REQUIRED_SUBELEMENTS = ['current', 'limits', 'timelimits', 'changelimits']
    
    # Ranges valides pour chaque élément
    ELEMENT_RANGES = {
        'overcast': (0.0, 1.0),
        'fog': (0.0, 1.0),
        'rain': (0.0, 1.0),
        'windMagnitude': (0.0, 20.0),
        'windDirection': (-3.14, 3.14),
        'snowfall': (0.0, 1.0)
    }
    
    def __init__(self, version: str = '1.28'):
        super().__init__('cfgweather', version)
    
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
        """Valide la structure de cfgweather.xml"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            # Vérifier balise racine
            if root.tag != 'weather':
                errors.append(ValidationError(
                    severity='error',
                    message=f"Balise racine invalide : '{root.tag}'. Attendu : 'weather'",
                    line=1,
                    suggestion="La balise racine doit être <weather>"
                ))
                return errors
            
            # Vérifier attributs racine
            reset = root.get('reset')
            enable = root.get('enable')
            
            if reset not in ['0', '1']:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Attribut 'reset'='{reset}' invalide (doit être 0 ou 1)",
                    field='reset',
                    suggestion="0 = use config on restart, 1 = load saved state",
                    context="Doc: Set to 0 for consistent weather, 1 for persistent evolving patterns"
                ))
            
            if enable not in ['0', '1']:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Attribut 'enable'='{enable}' invalide (doit être 0 ou 1)",
                    field='enable',
                    suggestion="1 = weather ON, 0 = weather OFF (non recommandé)",
                    context="Doc: Disabling weather removes atmospheric immersion"
                ))
            
            # Vérifier éléments météo
            for element in self.WEATHER_ELEMENTS:
                elem = root.find(element)
                
                if elem is None:
                    errors.append(ValidationError(
                        severity='warning',
                        message=f"Élément météo <{element}> manquant",
                        field=element,
                        suggestion=f"Ajoutez la configuration complète pour {element}"
                    ))
                else:
                    errors.extend(self._validate_weather_element(elem, element))
            
            # Vérifier storm (optionnel mais recommandé)
            storm_elem = root.find('storm')
            if storm_elem is not None:
                errors.extend(self._validate_storm(storm_elem))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def validate_business_rules(self, content: str) -> List[ValidationError]:
        """Valide les règles métier"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            # RÈGLE: snowfall sur Chernarus = BAD
            snowfall_elem = root.find('snowfall')
            if snowfall_elem is not None:
                limits_elem = snowfall_elem.find('limits')
                if limits_elem is not None:
                    max_snow = self.safe_float(limits_elem.get('max', '0'), 0.0)
                    
                    if max_snow > 0.1:
                        errors.append(ValidationError(
                            severity='warning',
                            message=f"Snowfall max={max_snow} activé",
                            field='snowfall',
                            suggestion="Snowfall doit être 0.0 sur Chernarus et cartes tempérées",
                            context="Doc: Use snowfall only on winter or arctic maps"
                        ))
            
            # RÈGLE: fog trop élevé = unplayable
            fog_elem = root.find('fog')
            if fog_elem is not None:
                limits_elem = fog_elem.find('limits')
                if limits_elem is not None:
                    max_fog = self.safe_float(limits_elem.get('max', '0'), 0.0)
                    
                    if max_fog > 0.9:
                        errors.append(ValidationError(
                            severity='warning',
                            message=f"Fog max={max_fog} très élevé",
                            field='fog',
                            suggestion="Max recommandé: 0.8 pour éviter gameplay frustrant",
                            context="Doc: Excessive fog can frustrate players"
                        ))
            
            # RÈGLE: rain threshold avec overcast
            rain_elem = root.find('rain')
            if rain_elem is not None:
                thresholds_elem = rain_elem.find('thresholds')
                if thresholds_elem is not None:
                    rain_min_thresh = self.safe_float(thresholds_elem.get('min', '0'), 0.0)
                    
                    # Vérifier avec overcast max
                    overcast_elem = root.find('overcast')
                    if overcast_elem is not None:
                        overcast_limits = overcast_elem.find('limits')
                        if overcast_limits is not None:
                            overcast_max = self.safe_float(overcast_limits.get('max', '0'), 0.0)
                            
                            if rain_min_thresh > overcast_max:
                                errors.append(ValidationError(
                                    severity='error',
                                    message=f"Rain threshold min ({rain_min_thresh}) > overcast max ({overcast_max})",
                                    field='rain.thresholds',
                                    suggestion=f"Rain threshold doit être ≤ overcast max ({overcast_max})",
                                    context="Doc: Coordinate rain thresholds with overcast limits"
                                ))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def _validate_weather_element(self, elem, element_name: str) -> List[ValidationError]:
        """Valide un élément météo (overcast, fog, rain, etc.)"""
        errors = []
        
        # Vérifier sous-éléments requis
        for subelement in self.REQUIRED_SUBELEMENTS:
            if elem.find(subelement) is None:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Élément <{element_name}> : sous-élément <{subelement}> manquant",
                    field=f'{element_name}.{subelement}',
                    suggestion=f"Ajoutez <{subelement} .../>"
                ))
        
        # Valider <current>
        current_elem = elem.find('current')
        if current_elem is not None:
            for attr in ['actual', 'time', 'duration']:
                if current_elem.get(attr) is None:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"<{element_name}><current> : attribut '{attr}' manquant",
                        field=f'{element_name}.current.{attr}'
                    ))
        
        # Valider <limits>
        limits_elem = elem.find('limits')
        if limits_elem is not None:
            min_val = limits_elem.get('min')
            max_val = limits_elem.get('max')
            
            if min_val is None or max_val is None:
                errors.append(ValidationError(
                    severity='error',
                    message=f"<{element_name}><limits> : attributs 'min' et 'max' requis",
                    field=f'{element_name}.limits'
                ))
            else:
                try:
                    min_f = float(min_val)
                    max_f = float(max_val)
                    
                    # Vérifier min ≤ max
                    if min_f > max_f:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"<{element_name}><limits> : min ({min_f}) > max ({max_f})",
                            field=f'{element_name}.limits'
                        ))
                    
                    # Vérifier range valide pour l'élément
                    if element_name in self.ELEMENT_RANGES:
                        valid_min, valid_max = self.ELEMENT_RANGES[element_name]
                        
                        if min_f < valid_min or max_f > valid_max:
                            errors.append(ValidationError(
                                severity='warning',
                                message=f"<{element_name}><limits> : range [{min_f}-{max_f}] hors limites recommandées [{valid_min}-{valid_max}]",
                                field=f'{element_name}.limits',
                                suggestion=f"Range recommandé: [{valid_min}-{valid_max}]"
                            ))
                
                except ValueError:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"<{element_name}><limits> : valeurs non numériques",
                        field=f'{element_name}.limits'
                    ))
        
        # Valider <timelimits>
        timelimits_elem = elem.find('timelimits')
        if timelimits_elem is not None:
            min_time = timelimits_elem.get('min')
            max_time = timelimits_elem.get('max')
            
            if min_time and max_time:
                try:
                    min_t = float(min_time)
                    max_t = float(max_time)
                    
                    if min_t > max_t:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"<{element_name}><timelimits> : min ({min_t}) > max ({max_t})",
                            field=f'{element_name}.timelimits'
                        ))
                    
                    # Warning si transitions trop rapides
                    if max_t < 30:
                        errors.append(ValidationError(
                            severity='warning',
                            message=f"<{element_name}><timelimits> : max={max_t}s très court",
                            field=f'{element_name}.timelimits',
                            suggestion="Transitions trop rapides = changements météo brusques",
                            context="Doc: Use smooth transitions for natural weather changes"
                        ))
                
                except ValueError:
                    pass
        
        return errors
    
    def _validate_storm(self, storm_elem) -> List[ValidationError]:
        """Valide la configuration storm"""
        errors = []
        
        density = storm_elem.get('density')
        threshold = storm_elem.get('threshold')
        timeout = storm_elem.get('timeout')
        
        # Vérifier attributs
        if density is None:
            errors.append(ValidationError(
                severity='error',
                message="<storm> : attribut 'density' manquant",
                field='storm.density',
                suggestion="Format: density='1.0' (0.0-1.0)"
            ))
        else:
            try:
                dens = float(density)
                if dens < 0 or dens > 1.0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"<storm> density={dens} hors range [0.0-1.0]",
                        field='storm.density',
                        context="Doc: Lightning frequency from 0.0 to 1.0"
                    ))
            except ValueError:
                errors.append(ValidationError(
                    severity='error',
                    message=f"<storm> density='{density}' n'est pas un nombre",
                    field='storm.density'
                ))
        
        if threshold is None:
            errors.append(ValidationError(
                severity='error',
                message="<storm> : attribut 'threshold' manquant",
                field='storm.threshold',
                suggestion="Format: threshold='0.9' (0.0-1.0)"
            ))
        else:
            try:
                thresh = float(threshold)
                if thresh < 0 or thresh > 1.0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"<storm> threshold={thresh} hors range [0.0-1.0]",
                        field='storm.threshold',
                        context="Doc: Overcast level required for storms"
                    ))
            except ValueError:
                pass
        
        if timeout is None:
            errors.append(ValidationError(
                severity='warning',
                message="<storm> : attribut 'timeout' manquant",
                field='storm.timeout',
                suggestion="Format: timeout='45' (secondes entre éclairs)"
            ))
        
        return errors
