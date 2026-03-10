"""
  APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés
  
  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : logger.py
  License : MIT License

  Ce module gère l'enregistrement des traces UART capturées.
"""
import os
from collections import deque
from datetime import datetime


LOG_MAX_LINES = 50000
log_buffer = deque(maxlen=LOG_MAX_LINES)

def dump_log_to_file(notify=None)->None:
    """sert à creer un fichier et enregistrer tous les données du buffer

    Args:
        notify (str, optional): un message d'information. Defaults to None.
    """

    folder = "logs"
    
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    filename = f"uart_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    filepath = os.path.join(folder, filename)

    try:
        with open(filepath, "w") as f:
            for line in log_buffer:
                f.write(line + "\n")
        
        if notify:
           notify(f"fichier enregistré dans \logs", seconds=3.0)
            
    except Exception as e:
        if notify:
            notify(f"Erreur dossier log: {e}", seconds=4.0)