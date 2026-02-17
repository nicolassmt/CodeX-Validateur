"""
messages_validator.py
Validateur pour messages.xml - Messages serveur

Source: DayZ Wiki - Messages.xml Configuration
"""

import xml.etree.ElementTree as ET
from typing import List
from ...base_validator import BaseValidator, ValidationError


class MessagesValidator(BaseValidator):
    """
    Validateur pour messages.xml
    Basé sur la documentation officielle DayZ
    """
    
    # Types de messages valides
    VALID_TYPES = ['welcome', 'periodic', 'event']
    
    def __init__(self, version: str = '1.28'):
        super().__init__('messages', version)
    
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
        """Valide la structure de messages.xml"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            # Vérifier balise racine
            if root.tag != 'messages':
                errors.append(ValidationError(
                    severity='error',
                    message=f"Balise racine invalide : '{root.tag}'. Attendu : 'messages'",
                    line=1,
                    suggestion="La balise racine doit être <messages>"
                ))
                return errors
            
            # Vérifier chaque message
            for idx, msg_elem in enumerate(root.findall('message'), start=1):
                msg_type = msg_elem.get('type')
                
                # Attribut 'type' requis
                if not msg_type:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Message #{idx} : attribut 'type' manquant",
                        line=idx,
                        suggestion="Format: <message type='welcome'> ou 'periodic' ou 'event'"
                    ))
                else:
                    # Vérifier type valide
                    if msg_type not in self.VALID_TYPES:
                        errors.append(ValidationError(
                            severity='error',
                            message=f"Message #{idx} : type '{msg_type}' invalide",
                            line=idx,
                            field='type',
                            suggestion=f"Types valides: {', '.join(self.VALID_TYPES)}",
                            context="Doc: 'welcome', 'periodic', ou 'event'"
                        ))
                
                # Vérifier <text> requis
                text_elem = msg_elem.find('text')
                if text_elem is None:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Message #{idx} ({msg_type}) : balise <text> manquante",
                        line=idx,
                        field='text',
                        suggestion="Ajoutez <text>Votre message</text>"
                    ))
                else:
                    # Vérifier longueur texte
                    text = text_elem.text or ''
                    if len(text) > 200:
                        errors.append(ValidationError(
                            severity='warning',
                            message=f"Message #{idx} ({msg_type}) : texte très long ({len(text)} caractères)",
                            line=idx,
                            field='text',
                            suggestion="Max recommandé: 200 caractères pour lisibilité",
                            context="Doc: Maximum recommended length is around 200 characters"
                        ))
                    
                    if len(text) == 0:
                        errors.append(ValidationError(
                            severity='warning',
                            message=f"Message #{idx} ({msg_type}) : texte vide",
                            line=idx,
                            field='text',
                            suggestion="Ajoutez du contenu au message"
                        ))
                
                # Vérifier paramètres selon type
                if msg_type == 'welcome':
                    errors.extend(self._validate_welcome(msg_elem, idx))
                elif msg_type == 'periodic':
                    errors.extend(self._validate_periodic(msg_elem, idx))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def validate_business_rules(self, content: str) -> List[ValidationError]:
        """Valide les règles métier"""
        errors = []
        
        try:
            root = ET.fromstring(content)
            
            for idx, msg_elem in enumerate(root.findall('message'), start=1):
                msg_type = msg_elem.get('type', 'unknown')
                
                # RÈGLE: delay pour welcome (doc: "Recommended values are 3-10 seconds")
                if msg_type == 'welcome':
                    delay_elem = msg_elem.find('delay')
                    if delay_elem is not None:
                        delay = self.safe_int(delay_elem.text, 0)
                        
                        if delay == 0:
                            errors.append(ValidationError(
                                severity='warning',
                                message=f"Message #{idx} (welcome) : delay=0 peut s'afficher avant le chargement",
                                line=idx,
                                field='delay',
                                suggestion="Recommandé: 3-10 secondes",
                                context="Doc: Setting delay to 0 (message may appear before player loads)"
                            ))
                        elif delay > 30:
                            errors.append(ValidationError(
                                severity='warning',
                                message=f"Message #{idx} (welcome) : delay={delay}s très long",
                                line=idx,
                                field='delay',
                                suggestion="Recommandé: 3-10 secondes pour que le joueur soit prêt"
                            ))
                
                # RÈGLE: interval pour periodic (doc: "Avoid intervals shorter than 10 minutes")
                if msg_type == 'periodic':
                    interval_elem = msg_elem.find('interval')
                    if interval_elem is not None:
                        interval = self.safe_int(interval_elem.text, 0)
                        
                        if interval < 600:  # 10 minutes
                            errors.append(ValidationError(
                                severity='warning',
                                message=f"Message #{idx} (periodic) : interval={interval}s trop court (< 10 min)",
                                line=idx,
                                field='interval',
                                suggestion="Recommandé: >= 1800s (30 min) pour éviter le spam",
                                context="Doc: Avoid intervals shorter than 10 minutes to prevent message spam"
                            ))
                        elif interval > 7200:  # 2 heures
                            errors.append(ValidationError(
                                severity='info',
                                message=f"Message #{idx} (periodic) : interval={interval}s très long (> 2h)",
                                line=idx,
                                field='interval',
                                context="Messages rares = moins de visibilité"
                            ))
        
        except ET.ParseError:
            pass
        
        return errors
    
    def _validate_welcome(self, msg_elem, idx: int) -> List[ValidationError]:
        """Valide un message de type welcome"""
        errors = []
        
        # Vérifier <delay>
        delay_elem = msg_elem.find('delay')
        if delay_elem is None:
            errors.append(ValidationError(
                severity='info',
                message=f"Message #{idx} (welcome) : <delay> manquant (optionnel)",
                field='delay',
                suggestion="Ajoutez <delay>5</delay> pour attendre que le joueur charge"
            ))
        else:
            # Vérifier que c'est un nombre
            try:
                delay = int(delay_elem.text or '0')
                if delay < 0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Message #{idx} (welcome) : delay={delay} ne peut pas être négatif",
                        field='delay'
                    ))
            except ValueError:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Message #{idx} (welcome) : delay '{delay_elem.text}' n'est pas un entier",
                    field='delay',
                    suggestion="Utilisez un nombre en secondes (ex: 5)"
                ))
        
        return errors
    
    def _validate_periodic(self, msg_elem, idx: int) -> List[ValidationError]:
        """Valide un message de type periodic"""
        errors = []
        
        # Vérifier <interval> REQUIS pour periodic
        interval_elem = msg_elem.find('interval')
        if interval_elem is None:
            errors.append(ValidationError(
                severity='error',
                message=f"Message #{idx} (periodic) : <interval> manquant (REQUIS)",
                field='interval',
                suggestion="Ajoutez <interval>1800</interval> (30 min recommandé)",
                context="Doc: Time in seconds between periodic message broadcasts"
            ))
        else:
            # Vérifier que c'est un nombre
            try:
                interval = int(interval_elem.text or '0')
                if interval <= 0:
                    errors.append(ValidationError(
                        severity='error',
                        message=f"Message #{idx} (periodic) : interval={interval} doit être > 0",
                        field='interval',
                        suggestion="Valeurs courantes: 900 (15min), 1800 (30min), 3600 (1h)"
                    ))
            except ValueError:
                errors.append(ValidationError(
                    severity='error',
                    message=f"Message #{idx} (periodic) : interval '{interval_elem.text}' n'est pas un entier",
                    field='interval',
                    suggestion="Utilisez un nombre en secondes"
                ))
        
        return errors
