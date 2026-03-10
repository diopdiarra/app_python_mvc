"""
  APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés
  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : view.py
  License : MIT License

  Ce module implémente la couche "View" (MVC) en mode terminal avec la bibliothèque curses.

        - Initialiser l’environnement curses.
        - Afficher l’interface .
        - Récupérer les interactions utilisateur.
        - Émettre un signal quand l’utilisateur valide une commande .
        - Maintenir un contexte d’affichage (InterfaceContentsDTO) contenant l’état de l’UI :
        traces, filtres, mode d’affichage, configuration UART, messages d'infos.

"""
import curses

from app_python_mvc.views.signals import Signal
from app_python_mvc.views.ui_draw import redraw_interface
from app_python_mvc.views.interfacecontents import InterfaceContentsDTO
from app_python_mvc.logger import LOG_MAX_LINES
from app_python_mvc.filter import cycle_filter,toggle_display_mode
from app_python_mvc.setting import load_settings

class AppView:
    def __init__(self, stop_evt)-> None:
        """
        Initialise la vue et construit une chaîne lisible ("config", "status","message d'info, "filtre")pour l'affichage dans l'UI.

        Args:
            stop_evt (threading.Event): Événement utilisé pour demander l'arrêt de l'application
        """
        self._stop_evt = stop_evt
        self.entered_command = ""
        self.on_submit = Signal()
        s = load_settings()
        uart = s["uart"]
        frame_end_uart0 = uart.get("frame_end_uart0", "CRLF")
        frame_end_uart1 = uart.get("frame_end_uart1", "CRLF")
        config_str = f'{uart["baud"]} {uart["bits"]} {uart["parity"]} {uart["stopbits"]} {frame_end_uart0} {frame_end_uart1}'

        self.context = InterfaceContentsDTO(
                                              trace=[],
                                              filter=s["filter"],
                                              buffer_size=0,
                                              max_buffer_size=LOG_MAX_LINES,
                                              config=config_str,
                                              capture_active=False,
                                              message="",
                                              message_until=0.0,
                                              input_buffer="",
                                              display_mode=s["display_mode"],
                                              frame_end_uart0 =frame_end_uart0,
                                              frame_end_uart1= frame_end_uart1
                                              )

    def init(self, stdscr)->None:
        """
        Confiure l'environnement curses;
            - Active le curseur.
            - Active le mode non bloquant (nodelay + timeout).
            - Active la gestion de la souris.
            - Initialise les paires de couleurs.

        Args:
            stdscr: Fenêtre principale curses
        """
        curses.curs_set(1)
        stdscr.nodelay(True)
        stdscr.timeout(100)
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        curses.mouseinterval(0)


        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_CYAN, -1)     
            curses.init_pair(2, curses.COLOR_GREEN, -1)    
            curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  

   
    def step(self, stdscr)-> None:
        """
        Rafraîchit l'affichage de l'interface.

        Args:
            stdscr: Fenêtre principale curses.
        """
        redraw_interface(stdscr, self.context)

    def get_user_command(self, stdscr)-> None:
        """
        Lit les actions utilisateur (clavier/souris) et met à jour le contexte.
        
            Double clic souris :
            Ligne FILTRES → change le filtre
            Ligne TYPES → change le mode d’affichage

            Clavier :
            Caractères → ajout dans le champ de saisie
            Backspace → suppression d’un caractère
            Enter → valide la commande

            Lors de la validation, la commande est enregistrée et un signal est émis.

        Args:
            stdscr: Fenêtre principale curses.
        """
        user_event = stdscr.getch()

        if user_event == -1:
            return
        
        if user_event == curses.KEY_MOUSE:
            try:
                _, x, y, _, Button_state = curses.getmouse()

                if Button_state & curses.BUTTON1_DOUBLE_CLICKED:
                    h, w = stdscr.getmaxyx()
                    filter_line_y = h - 5 
                    type_line_y   = h - 4  

                    if y == filter_line_y:
                        self.context.filter = cycle_filter(self.context.filter)

                    elif y == type_line_y:
                        self.context.display_mode = toggle_display_mode(self.context.display_mode)

            except curses.error:
                     pass
            
        elif 32 <= user_event<= 126:
            self.context.input_buffer += chr(user_event)

        elif user_event in (curses.KEY_BACKSPACE, 263, 127, 8):
            if self.context.input_buffer:
                self.context.input_buffer = self.context.input_buffer[:-1]

        elif user_event in (10, 13):
            user_command= self.context.input_buffer.strip()
            self.context.input_buffer = ""
            if not user_command:
                return
            self.entered_command = user_command
            self.on_submit.emit(user_command)

   

