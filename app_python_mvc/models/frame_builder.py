"""
 APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés
 
  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : frame_builder.py
  License : MIT License

  Ce module gère la construction des trames de commande envoyées au microcontrôleur via la liaison série.
"""

def build_frame(command: bytes, params: bytes = b"") -> bytes:
  """
   Construit une trame de commande avec le format:
        b'#' + command + params + b'\\r\\n'
  Args:
      command (bytes): Code de la commande
      params (bytes, optional):  Paramètres associés à la commande, Par défaut : aucun paramètre.
  Returns:
      bytes:Trame complète prête à être envoyée sur le port série.
  """
  command_frame= b"#" + command + params + b"\r\n"
  return command_frame