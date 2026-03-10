"""
  APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés
  
  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : setting.py
  License : MIT License

  Ce module gère le chargement et la sauvegarde des paramètres de configuration de l'application.
  Les paramètres sont stockés dans un fichier JSON et incluent :
    - le filtre d'affichage des trames (ALL, TX, RX)
    - le mode d'affichage des données (HEX ou ASCII)
    - la configuration UART utilisée par l'espion.
"""
import json

from app_python_mvc.constants import SETTINGS_PATH

DEFAULTS = {
    "filter": "all",
    "display_mode": "ascii",
    "uart": {
        "baud": "115200",
        "bits": "8",
        "parity": "N",
        "stopbits": "1",
        "frame_end_uart0": "CRLF",  
        "frame_end_uart1": "CRLF",
    },
}

def load_settings() -> dict:
    """Charge les paramètres de configuration de l'application depuis le fichier JSON.
 
    Returns:
        dict: Dictionnaire contenant la configuration de l'application
    """
    try:
        settings_dict= json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        if not isinstance(settings_dict, dict):
            return DEFAULTS.copy()
    except FileNotFoundError:
        return DEFAULTS.copy()
    except json.JSONDecodeError:
        return DEFAULTS.copy()

    uart = settings_dict.get("uart") if isinstance(settings_dict.get("uart"), dict) else {}
    merged = DEFAULTS.copy()
    merged["filter"] = settings_dict.get("filter", DEFAULTS["filter"])
    merged["display_mode"] = settings_dict.get("display_mode", DEFAULTS["display_mode"])
    merged["uart"] = {**DEFAULTS["uart"], **uart}

    return merged

def save_settings(filter_value: str, display_mode: str, uart: dict) -> None:
    """Sauvegarde la configuration de l'application dans un fichier JSON.
    Args:
        filter_value (str):  Filtre actuellement appliqué aux traces.
        display_mode (str): Mode d'affichage des données (HEX ou ASCII).
        uart (dict): Dictionnaire contenant les paramètres UART
    """
    settings_dict = {
        "filter": filter_value,
        "display_mode": display_mode,
        "uart": {
            "baud": uart.get("baud", DEFAULTS["uart"]["baud"]),
            "bits": uart.get("bits", DEFAULTS["uart"]["bits"]),
            "parity": uart.get("parity", DEFAULTS["uart"]["parity"]),
            "stopbits": uart.get("stopbits", DEFAULTS["uart"]["stopbits"]),
            "frame_end_uart0": uart.get("frame_end_uart0", DEFAULTS["uart"]["frame_end_uart0"]), 
            "frame_end_uart1": uart.get("frame_end_uart1", DEFAULTS["uart"]["frame_end_uart1"]),
    }
    }

    tmp = SETTINGS_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(settings_dict, indent=2), encoding="utf-8")
    tmp.replace(SETTINGS_PATH)