"""
 APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés
 
  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : signal.py
  License : MIT License
"""
class Signal:
    def __init__(self):
        self._subs = []

    def connect(self, fn):
        self._subs.append(fn)

    def emit(self, *args, **kwargs):
        for fn in list(self._subs):
            fn(*args, **kwargs)