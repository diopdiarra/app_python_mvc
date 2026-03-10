
"""
  APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés
  
  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : process_commands.py
  License : MIT License

 Ce module implémente les fonctions de traitement des commandes saisies par l'utilisateur dans l'interface.
"""
import logging

from app_python_mvc.models.frame_builder import build_frame
from app_python_mvc.models.config_uart import SpyDeviceConfigUART
from app_python_mvc.views.ui_messages import set_message
from app_python_mvc.constants import CMD_START, CMD_STOP, CMD_SET

logger = logging.getLogger(__name__)

def start_cmd(self)-> None:
    """ Active la capture des données UART.

    Cette fonction :
        - construit la trame START
        - l'envoie au microcontrôleur
        - attend la réponse de l'espion UART
        - active l'état de capture si la commande réussit.
    """
    frame = build_frame(CMD_START)

    logger.info("trame START envoyée : %s", frame)

    self._model.send_frame(frame)

    result = self._model.wait_response(CMD_START)

    if result is True:
        self._model._capture_evt.set()
        self._view.context.capture_active = True
        set_message(self._view, "Capture activée", seconds=2.0)

    elif result is False:
        set_message(self._view, "Capture déjà active", seconds=2.0)

    else:
        set_message(self._view, "Connexion perdue. Veuillez relancer l'application.<Exit> pour quitter.", seconds=5.0)

def stop_cmd(self)-> None:
    """ Désactive la capture des données UART.

    Cette fonction :
        - construit la trame STOP
        - l'envoie au microcontrôleur
        - attend la réponse de l'espion UART
        - désactive l'état de capture si la commande réussit.

    """
    frame = build_frame(CMD_STOP)

    logger.info("trame STOP envoyée : %s", frame)

    self._model.send_frame(frame)

    result = self._model.wait_response(CMD_STOP)

    if result is True:

        self._model._capture_evt.clear()
        self._view.context.capture_active = False

        set_message(self._view, "Capture arrêtée", seconds=2.0)

    elif result is False:

        set_message(self._view, "Capture déjà arrêtée", seconds=2.0)

    else:

        set_message(self._view, "Connexion perdue. Veuillez relancer l'application.<Exit> pour quitter", seconds=5.0)

def set_cmd(self, command:str)->None:
    """ Configure les paramètres UART de l'espion.

    Étapes :
        vérifie que la capture est arrêtée
        parse les paramètres saisis par l'utilisateur
        crée un objet de configuration UART
        envoie la trame au microcontrôleur
        attend la réponse de l'espion
        met à jour la configuration affichée.
    Args:
        command (str): Commande utilisateur complète.
    """
    parts = command.split()

    if self._model._capture_evt.is_set():
        set_message(self._view, "STOP CAPTURE !!!", seconds=3.0)
        return

    if len(parts) < 2:
        set_message(
            self._view,
            "Usage: set <baud> [bits] [stop] [parité] [fin de trame]",
            seconds=3.0
        )
        return

    try:
        config_uart = SpyDeviceConfigUART(*parts[1:])
    except ValueError as e:
        logger.warning("Mauvais parametre de config uart saisi: %s", str(e))
        set_message(self._view, str(e), seconds=3.0)
        return

    frame = config_uart.build_set_command_frame()

    logger.info("trame SET envoyée : %s", frame)

    self._model.send_set_frame(frame)

    result = self._model.wait_response(CMD_SET, timeout=0.8)

    if result is True:

        set_message(self._view, "Paramètres appliqués", seconds=2.0)

        self._view.context.config = str(config_uart)

    elif result is False:

        set_message(self._view, "Paramètres non configurés", seconds=2.0)

    else:

        set_message(self._view, "Connexion perdue. Veuillez relancer l'application.<Exit> pour quitter", seconds=5.0)