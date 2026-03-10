"""
  APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés
  
  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : filter.py
  License : MIT License

  Ce module gère les paramètres d'affichage des traces capturées.

  Il fournit deux fonctionnalités principales :
    - le changement du filtre de direction des trames (ALL, TX, RX)
    - le changement du mode d'affichage des données (HEX ou ASCII)
"""
from app_python_mvc.constants import TX , RX, ALL, HEX, ASCII

FILTER_ORDER = [ALL, TX, RX]

def cycle_filter(current_filter: str) -> str:
    cf = (current_filter or "all").lower()
    try:
        i = FILTER_ORDER.index(cf)
    except ValueError:
        return "all"
    return FILTER_ORDER[(i + 1) % len(FILTER_ORDER)]


def toggle_display_mode(mode: str) -> str:
    return ASCII if (mode or "").lower() == "hex" else HEX
