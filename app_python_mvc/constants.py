"""
  APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés
  
  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : constants.py
  License : MIT License

  Ce module regrpupe tous les constants et les dictionnaires  utilisés
"""
from pathlib import Path

BAUD = 460800
LOG_FILE = "app.log"

START = "start"
STOP  = "stop"
SET   = "set"
LOG   = "log"

TX    = "tx"
RX    = "rx"
ALL   = "all"

HEX  = "hex"
ASCII = "ascii"

CMD_START  = b"1"
CMD_STOP   = b"2"
CMD_SET    = b"3"
CMD_PING   = b"P"


FRAME_END = {
    "LF": b"E1",
    "CR": b"E2",
    "CRLF": b"E3",
}

BAUDRATE = {
    "1200":   b"a",
    "4800":   b"b",
    "9600":   b"c",
    "19200":  b"d",
    "38400":  b"e",
    "57600":  b"f",
    "115200": b"g",
    "230400": b"h",
    "460800": b"i",
}

BYTESIZE = {
    "5" : b"5",
    "6" : b"6",
    "7" : b"7",
    "8" : b"8",
}

STOPBITS = {
    "1": b"1",
    "2" : b"2"
}

PARITY  = {
    "N" : b"N",
    "O" : b"O",
    "E" : b"E"
}
SETTINGS_PATH = Path.home() / ".app_python_mvc_settings.json"
