"""
detector.py - VERSION CORRIGÉE
Détection automatique du format et type de fichier DayZ
Supporte 17+ types de fichiers XML et JSON
"""

import json
import xml.etree.ElementTree as ET
from typing import Dict, Optional


class DayZFileDetector:
    """Détecte automatiquement le format et le type de fichier DayZ"""
    
    # Signatures XML - Détection par balise racine + enfants
    SIGNATURES_XML = {
        'types.xml': {
            'root': 'types',
            'child': 'type',
            'child_attribute': 'name',
            'description': 'Loot spawn configuration'
        },
        'events.xml': {
            'root': 'events',
            'child': 'event',
            'child_attribute': 'name',
            'description': 'Dynamic events configuration'
        },
        'economy.xml': {
            'root': 'economycore',
            'child': 'ce',
            'description': 'Economic zones and probabilities'
        },
        'globals.xml': {
            'root': 'variables',
            'child': 'var',
            'child_attribute': 'name',
            'description': 'Server global variables'
        },
        'messages.xml': {
            'root': 'messages',
            'child': 'message',
            'description': 'Server messages configuration'
        },
        'spawnable_types.xml': {
            'root': 'spawnabletypes',
            'child': 'type',
            'child_attribute': 'name',
            'description': 'Loot container definitions'
        },
        'cfgspawnabletypes.xml': {
            'root': 'spawnabletypes',
            'child': 'type',  # ✅ CORRIGÉ : était 'damage'
            'child_attribute': 'name',
            'description': 'Spawnable types configuration (attachments & cargo)'
        },
        'mapgrouppos.xml': {
            'root': 'map',
            'child': 'group',
            'description': 'Map-specific spawn positions'
        },
        'mapgroupproto.xml': {
            'root': 'map',
            'child': 'group',
            'child_attribute': 'name',
            'description': 'Map group prototypes'
        },
        'zombie_territories.xml': {
            'root': 'territory-type',
            'child': 'territory',
            'child_attribute': 'color',
            'description': 'Zombie spawn zones'
        },
        'cfgignorelist.xml': {
            'root': 'list',
            'child': 'type',
            'description': 'Ignored types list'
        },
        'cfgenvironment.xml': {
            'root': 'env',
            'child': 'territory',
            'description': 'Environment configuration'
        },
        'cfglimitsdefinition.xml': {
            'root': 'lists',
            'child': 'list',
            'description': 'Category limits definition'
        },
        'cfgrandompresets.xml': {
            'root': 'randompresets',
            'child': 'cargo',
            'description': 'Random presets configuration'
        }
    }
    
    # Signatures JSON - Détection par clés racine
    SIGNATURES_JSON = {
        'cfgeffectarea.json': {
            'root_keys': ['ContaminatedArea', 'ContaminatedStatic'],
            'required_fields': ['AreaName', 'Pos', 'Radius'],
            'description': 'Gas/contamination zones'
        },
        'cfgeventspawns.json': {
            'root_keys': ['EventSpawn'],
            'required_fields': ['event', 'pos', 'min', 'max'],
            'description': 'Event spawn positions'
        },
        'cfgplayerspawnpoints.json': {
            'root_keys': ['SpawnPoints'],
            'required_fields': ['generator_posbubbles', 'generator_posboxes'],
            'description': 'Player spawn points'
        },
        'cfgweather.json': {
            'root_keys': ['weather'],
            'required_fields': ['enable', 'startWeather'],
            'description': 'Weather configuration'
        },
        'cfggameplay.json': {
            'root_keys': ['GeneralData', 'PlayerData', 'StaminaData'],
            'required_fields': [],
            'description': 'Gameplay configuration'
        }
    }
    
    def detect(self, content: str, filename: Optional[str] = None) -> Dict:
        """
        Détecte le format et le type du fichier DayZ
        
        Args:
            content: Contenu du fichier
            filename: Nom du fichier (optionnel, aide à la détection)
        
        Returns:
            dict: {
                'format': 'xml' | 'json' | 'unknown',
                'file_type': 'types' | 'events' | ... | None,
                'confidence': float (0-1),
                'description': str,
                'metadata': dict
            }
        """
        # Tentative de détection XML
        xml_result = self._detect_xml(content, filename)
        if xml_result['confidence'] > 0.8:
            return xml_result
        
        # Tentative de détection JSON
        json_result = self._detect_json(content, filename)
        if json_result['confidence'] > 0.8:
            return json_result
        
        # Si aucune détection claire, retourner le meilleur score
        if xml_result['confidence'] > json_result['confidence']:
            return xml_result
        else:
            return json_result
    
    def _detect_xml(self, content: str, filename: Optional[str] = None) -> Dict:
        """Détecte les fichiers XML DayZ"""
        try:
            root = ET.fromstring(content)
            root_tag = root.tag
            
            # Chercher une correspondance exacte
            for file_type, signature in self.SIGNATURES_XML.items():
                if root_tag == signature['root']:
                    # Vérifier l'enfant si spécifié
                    confidence = 0.9
                    
                    if 'child' in signature:
                        children = root.findall(signature['child'])
                        if len(children) > 0:
                            confidence = 0.95
                            
                            # Vérifier l'attribut enfant si spécifié
                            if 'child_attribute' in signature:
                                first_child = children[0]
                                if first_child.get(signature['child_attribute']) is not None:
                                    confidence = 1.0
                    
                    # Bonus si le filename correspond
                    if filename and file_type.replace('.xml', '') in filename.lower():
                        confidence = min(1.0, confidence + 0.05)
                    
                    return {
                        'format': 'xml',
                        'file_type': file_type.replace('.xml', ''),
                        'confidence': confidence,
                        'description': signature['description'],
                        'metadata': {
                            'root_tag': root_tag,
                            'num_children': len(list(root)),
                            'has_attributes': len(root.attrib) > 0
                        }
                    }
            
            # Aucune signature trouvée mais XML valide
            return {
                'format': 'xml',
                'file_type': None,
                'confidence': 0.5,
                'description': 'Valid XML but unknown DayZ type',
                'metadata': {
                    'root_tag': root_tag,
                    'num_children': len(list(root))
                }
            }
            
        except ET.ParseError:
            # Pas du XML valide
            return {
                'format': 'unknown',
                'file_type': None,
                'confidence': 0.0,
                'description': 'Invalid XML',
                'metadata': {}
            }
    
    def _detect_json(self, content: str, filename: Optional[str] = None) -> Dict:
        """Détecte les fichiers JSON DayZ"""
        try:
            data = json.loads(content)
            
            if not isinstance(data, dict):
                return {
                    'format': 'json',
                    'file_type': None,
                    'confidence': 0.3,
                    'description': 'Valid JSON but not an object',
                    'metadata': {'type': type(data).__name__}
                }
            
            # Chercher une correspondance
            for file_type, signature in self.SIGNATURES_JSON.items():
                confidence = 0.0
                
                # Vérifier les clés racine
                for root_key in signature['root_keys']:
                    if root_key in data:
                        confidence = 0.8
                        
                        # Vérifier les champs requis si c'est un objet/liste
                        root_data = data[root_key]
                        if isinstance(root_data, dict):
                            required_fields = signature.get('required_fields', [])
                            if required_fields:
                                matching_fields = sum(1 for field in required_fields if field in root_data)
                                if matching_fields == len(required_fields):
                                    confidence = 1.0
                                elif matching_fields > 0:
                                    confidence = 0.85
                        elif isinstance(root_data, list) and len(root_data) > 0:
                            # Vérifier le premier élément
                            first_item = root_data[0]
                            if isinstance(first_item, dict):
                                required_fields = signature.get('required_fields', [])
                                if required_fields:
                                    matching_fields = sum(1 for field in required_fields if field in first_item)
                                    if matching_fields == len(required_fields):
                                        confidence = 1.0
                                    elif matching_fields > 0:
                                        confidence = 0.85
                        
                        # Bonus si le filename correspond
                        if filename and file_type.replace('.json', '') in filename.lower():
                            confidence = min(1.0, confidence + 0.05)
                        
                        if confidence > 0.8:
                            return {
                                'format': 'json',
                                'file_type': file_type.replace('.json', ''),
                                'confidence': confidence,
                                'description': signature['description'],
                                'metadata': {
                                    'root_key': root_key,
                                    'num_keys': len(data.keys()),
                                    'has_arrays': any(isinstance(v, list) for v in data.values())
                                }
                            }
            
            # JSON valide mais type inconnu
            return {
                'format': 'json',
                'file_type': None,
                'confidence': 0.5,
                'description': 'Valid JSON but unknown DayZ type',
                'metadata': {
                    'num_keys': len(data.keys()),
                    'top_level_keys': list(data.keys())[:5]
                }
            }
            
        except json.JSONDecodeError:
            # Pas du JSON valide
            return {
                'format': 'unknown',
                'file_type': None,
                'confidence': 0.0,
                'description': 'Invalid JSON',
                'metadata': {}
            }
    
    def get_supported_files(self) -> Dict[str, list]:
        """Retourne la liste de tous les fichiers supportés"""
        return {
            'xml': list(self.SIGNATURES_XML.keys()),
            'json': list(self.SIGNATURES_JSON.keys())
        }
    
    def get_file_info(self, file_type: str) -> Optional[Dict]:
        """Retourne les infos sur un type de fichier spécifique"""
        # Chercher dans XML
        if file_type + '.xml' in self.SIGNATURES_XML:
            return self.SIGNATURES_XML[file_type + '.xml']
        
        # Chercher dans JSON
        if file_type + '.json' in self.SIGNATURES_JSON:
            return self.SIGNATURES_JSON[file_type + '.json']
        
        # Chercher sans extension
        for ext_type, signatures in [('.xml', self.SIGNATURES_XML), ('.json', self.SIGNATURES_JSON)]:
            full_type = file_type + ext_type
            if full_type in signatures:
                return signatures[full_type]
        
        return None


# Instance globale pour faciliter l'import
detector = DayZFileDetector()
