"""
  APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés
  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : interfacecontexte.py
  License : MIT License

  Ce module définit une structure de données utilisée pour stocker l'état de l'interface utilisateur
"""
from dataclasses import dataclass

@dataclass
class InterfaceContentsDTO:
    trace: list
    filter: str
    buffer_size: int
    max_buffer_size: int
    config: str
    capture_active: bool
    message: str
    message_until: float 
    input_buffer: str
    display_mode: str
    frame_end_uart0 : str
    frame_end_uart1 : str