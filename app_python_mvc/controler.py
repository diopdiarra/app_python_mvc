"""
  APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés
  
  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : controler.py
  License : MIT License

  Ce module implémente le contrôleur principal de l'application selon l'architecture MVC (Model - View - Controller).

Rôle du contrôleur :
    - Assurer la communication entre le modèle et la vue.
    - Traiter les commandes saisies par l'utilisateur.
    -l'envoi des commandes vers le microcontrôleur et la réception des données UART via le modèle
    - l'affichage des traces via la vue
"""
import queue
import curses
import logging

from app_python_mvc.models.model import AppModel
from app_python_mvc.views.view import AppView
from app_python_mvc.setting import save_settings,load_settings
from app_python_mvc.models.frame_builder import build_frame
from app_python_mvc.logger import dump_log_to_file, log_buffer
from app_python_mvc.views.ui_messages import set_message, tick_messages
from app_python_mvc.process_commands import start_cmd, stop_cmd, set_cmd
from app_python_mvc.constants import ( CMD_STOP,CMD_PING,
START, STOP, LOG, SET,
)

logger = logging.getLogger(__name__)

class AppControler:
    def __init__(self, model: AppModel, view: AppView, ):
        """_Initialise le contrôleur.

        Connecte la vue au contrôleur afin que les commandes
        utilisateur soient traitées par la méthode

        Args:
            model (AppModel):  Instance du modèle gérant la communication série.
            view (AppView): Instance de la vue gérant l'interface utilisateur.
        """
        self._model = model
        self._view = view
        self._view.on_submit.connect(self.process_user_command)
    
    def check_device(self) -> bool:
        """ Vérifie que le périphérique connecté correspond bien à l'espion UART.

        Returns:
            bool:  - True  : la carte a répondu correctement au PING.
                   - False : aucune réponse reçue ou périphérique incorrect.
        """

        self._model.send_frame(build_frame(CMD_PING))

        ok = self._model.wait_response(CMD_PING, timeout=1)

        if not ok:
            print("Device incorrect ou non répondu")
            return False

        return True


    def sync_uart_configuration(self)-> None:
        """Synchronise la configuration UART entre l'application PC et la carte espion.
        """

        settings = load_settings()
        uart = settings["uart"]

        baud = uart["baud"]
        bits = uart["bits"]
        parity = uart["parity"]
        stopbits = uart["stopbits"]
        frame_end_uart0 = uart["frame_end_uart0"]
        frame_end_uart1 = uart["frame_end_uart1"]


        cmd = f"set {baud} {bits} {parity} {stopbits} {frame_end_uart0} {frame_end_uart1}"

        set_cmd(self, cmd)

    def run(self)->None:
        """ Lance l'application.

         Démarre le thread d'écoute série.
        Lance la boucle principale de l'interface utilisateur.
        À la fermeture de l'application :
            - envoie la commande STOP au microcontrôleur
            - sauvegarde la configuration UART
            - arrête le thread d'écoute.
        """
        self._model.start_listener()
        if self.check_device():
            self.sync_uart_configuration()
       
        try:
            curses.wrapper(self._ui_loop)
        finally:
            self._model.send_frame(build_frame(CMD_STOP))
            parts = (self._view.context.config or "").split()
            if len(parts) == 5:
                baud, bits, parity, stopbits, frame_end_uart0, frame_end_uart1, = parts
            else:
                baud, bits, parity, stopbits , frame_end_uart0, frame_end_uart1= "115200", "8", "N", "1", "CRLF","CRLF"

            settings_dict = {
                "baud": baud,
                "bits": bits,
                "parity": parity,
                "stopbits": stopbits,
                "frame_end_uart0": frame_end_uart0,
                "frame_end_uart1" : frame_end_uart1
            }
            save_settings(self._view.context.filter, self._view.context.display_mode, settings_dict)
            self._model.stop_listener()
            

    def _ui_loop(self, stdscr):
        """  Boucle principale de l'interface utilisateur.

        Cette boucle :
            - récupère les commandes saisies par l'utilisateur
            - traite les données capturées dans le buffer
            - met à jour les messages d'information
            - rafraîchit l'affichage de l'interface.

        Args:
            stdscr:Fenêtre principale fournie par curses.
        """
        self._view.init(stdscr)
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        curses.mouseinterval(250)


        while not self._model._stop_evt.is_set():

            self._view.get_user_command(stdscr)
            self.process_trace_buffer()
            tick_messages(self._view)
            self._view.step(stdscr)
    

    def process_trace_buffer(self)-> None:
        """ Traite les données de capture provenant du modèle.

            Les trames décodées sont extraites du `trace_buffer`,
            converties selon le mode d'affichage (HEX ou ASCII),
            puis ajoutées à l'historique des traces affichées
            dans l'interface utilisateur.

            Les données sont également ajoutées au buffer
            d'enregistrement pour permettre leur sauvegarde.
        """
        try:
            data = self._model.trace_buffer.get_nowait()

            if data is None:
                return

            direction = data.get("direction", "?")
            payload = data.get("payload", b"")
            if self._view.context.display_mode == "hex":
                payload_str = " ".join(f"{b:02X}" for b in payload)
                
            else:
                payload_str = "".join(chr(b) if 32 <= b <= 126 else "." for b in payload)
            line = f"{direction} | {payload_str}"
            
            self._view.context.trace.append(line)
            self._view.context.buffer_size = len(self._view.context.trace)
            log_buffer.append(line)

        except queue.Empty:
            pass
   
    def process_user_command(self, user_command: str) -> None:
        """ Traite une commande saisie par l'utilisateur.

        Args:
            user_command (str): Commande saisie par l'utilisateur dans l'interface.

        Returns:
            None
        """

        logger.info(f"commande recupéré ")

        command = user_command.strip()
            
        if command == START:
            logger.info(f"commande = {command}")
            return start_cmd(self)
        
        elif command == STOP:
            logger.info(f"commande = {user_command}")
            return stop_cmd(self)
    
        elif command.startswith(SET): 
            return set_cmd(self,command)           
               
        elif command == LOG:
            dump_log_to_file(lambda msg, seconds=3.0: set_message(self._view, msg, seconds))

        elif command == "help":
            set_message(self._view, "commandes disponibles: start, stop et set {usage : set 'baud' 'nombre_de_bit' 'parité' 'bit_de_stop'}", seconds=15)

        elif command in ("exit", "quit"):
            self._model.send_frame(build_frame(CMD_STOP))
            self._model.stop_listener()

        else:
            set_message(self._view, "ERREUR: Commande inconnue", seconds=3.0)

