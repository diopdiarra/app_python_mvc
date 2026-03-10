"""
  APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés

  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : model.py
  License : MIT License

  Ce module implémente la couche "Model" (MVC).
 Il gère :
    - La liaison série (envoi de trames vers le microcontrôleur).
    - Le lancement/arrêt du thread d’écoute (listener_thread).
    - Les buffers thread-safe (queues) contenant :
        * les données capturées (trace_buffer)
        * les réponses aux commandes (response_buffer)
"""
import threading
import queue
import logging
import time

from serial import Serial

from app_python_mvc.models.listener import listener_thread
from app_python_mvc.views.ui_messages import set_message

logger = logging.getLogger(__name__)

class AppModel:
    def __init__(self, ser: Serial, stop_evt: threading.Event, capture_evt: threading.Event)-> None:
        """
        Initialise le modèle avec un port série et les événements de contrôle.
        Args:
            ser (Serial): Instance pyserial déjà ouverte et configurée (baudrate, timeout, etc.)
            stop_evt (threading.Event): Événement permettant de demander l’arrêt du thread listener.
            capture_evt (threading.Event):  Événement indiquant si la capture est active.
        Thread:
            _listener :Thread de réception : lit le port série et remplit les buffers

        """
        self._capture_evt = capture_evt
        self._stop_evt = stop_evt
        self._trace_buffer = queue.Queue()
        self._response_buffer = queue.Queue()
        self._ser = ser

        self._listener = threading.Thread(
            target=listener_thread,
            args=(
                self._ser,
                self._stop_evt,
                self._capture_evt,
                self._trace_buffer,
                self._response_buffer,
                
            ),
            daemon=False
        )

    def start_listener(self) :
        """ 
          Démarre le thread de réception s'il n'est pas déjà en cours d'exécution
        """
        if not self._listener.is_alive():
            self._listener.start()

    def stop_listener(self, join_timeout: float = 1.0):
        """
            Demande l'arrêt du thread de réception et attend sa fin

        Args:
            join_timeout (float, optional): Durée maximale (en secondes) d’attente du join. Defaults to 1.0.
        """
        self._stop_evt.set()

        self._ser.cancel_read()
  
        if self._listener and self._listener.is_alive():
            self._listener.join(timeout=join_timeout)
    def send_frame(self, frame: bytes) -> None:
        try:
            self._ser.write(frame)
            logger.info(f"trame envoyé :{frame}")

        except Exception as e:
            logger.warning(f"Connexion série perdue : {e}")
            set_message(self._view, "Connexion perdue. Veuillez relancer l'application.y", seconds=2.0)
            self._ser = None

    @property
    def trace_buffer(self)->queue.Queue:
        """
           Accès au buffer des données capturées décodées.

        Returns:
            queue.Queue:  file contenant des dict (ex: {"direction": str, "payload": bytes})
        """
        return self._trace_buffer

    @property
    def response_buffer(self)->queue.Queue:
        """
         Accès au buffer des réponses aux commandes.
        Returns:
            queue.Queue: file contenant des tuples (command_code: bytes, command_success: bool)
        """
        return self._response_buffer
    
    def send_set_frame(self, frame_set: bytes)-> None:
        """
          Envoie une trame de configuration (SET) vers la carte.

        Args:
            params (bytes): _description_
        """
        self.send_frame(frame_set)
    
    def wait_response(self, expected_cmd: bytes, timeout: float = 1.0)-> None:
        """
        Attend la réponse correspondant à une commande.

        Args:
            expected_cmd (bytes): code de la commande attendue
            timeout (float): temps maximum d'attente
        """

        end_time = time.monotonic() + timeout

        while time.monotonic() < end_time:

            try:
                cmd, result = self._response_buffer.get(timeout=0.1)

            except queue.Empty:
                continue

            if cmd == expected_cmd:
                return result

        return None
