"""
  APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés
  
  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : ui_message.py
  License : MIT License

  Ce module gère l’affichage temporaire des messages dans l’interface utilisateur.
  Il permet d’afficher un message pendant une durée définieet de le supprimer automatiquement après expiration du délai.
"""
import time

def set_message(self, message_text: str, seconds: float = 3.0) -> None:
    """_
    Définit un message temporaire à afficher dans l’interface

    Args:
        msg (str): Texte du message à afficher.
        seconds (float, optional): Durée d’affichage en secondes.. Defaults to 3.0.
    """
    self.context.message = message_text
    self.context.message_until = time.time() + seconds

def tick_messages(self) -> None:
    """
     Vérifie si le message temporaire a expiré.
     Si le temps courant dépasse message_until,le message est effacé.
    """
    if self.context.message and time.time() > self.context.message_until:
        self.context.message = ""
