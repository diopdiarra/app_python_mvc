"""
  APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés
  
  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : ui_draw.py
  License : MIT License

 Ce module gère l'affichage de l’interface utilisateur en mode terminal via curses.
    Il permet :
    - d’afficher les lignes de trace (données capturées),
    - d’appliquer un filtre (all / tx / rx),
    - d’afficher l’état (capture, configuration UART, taille buffer),
    - d’afficher un message d’information si présent,
    - d’afficher la zone de saisie utilisateur.
"""
import curses

from app_python_mvc.views.interfacecontents import InterfaceContentsDTO

def _draw_text_safe(stdscr, y:int, x:int, text:str, max_len:int, attr:int=0)-> None:
    """
   Cette fonction empêche l’application de planter si l’écriture dépasse les limites de l’écran.
    Elle limite également le nombre de caractères affichés grâce à addnstr.
    
    Args:
        stdscr (_type_): Fenêtre principale curses
        y (int):position ligne
        x (int):position colonne
        text (str): texte à afficher
        max_len (int):Nombre maximum de caractères à écrire.
        attr (int, optional): Attribut curses pour la pair de couleur a uitiliser.Defaults to 0.
    """ 
    try:
        if attr:
            stdscr.attron(attr)
        stdscr.addnstr(y, x, text, max_len)
        if attr:
            stdscr.attroff(attr)
    except curses.error:
        pass

def redraw_interface(stdscr, context: InterfaceContentsDTO)-> None:
    """
    Redessine complètement l’interface utilisateur.
        -Zone principale : traces (filtrées et colorées TX/RX).
        - Ligne filtres : filtre actif (all / tx / rx).
        - Ligne types : mode d’affichage (ex: hex / ascii).
        - Ligne status : état capture, config UART, occupation du buffer.
        - Ligne message : message d’information (si présent).
        - Ligne input : champ de saisie utilisateur.

    Args:
        stdscr:  Fenêtre principale curses.
        context (InterfaceContentsDTO): Contexte contenant l’état de l’interface (traces, filtre, mode, message, input, ).
    """
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK) 
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)

    stdscr.erase()
    h, w = stdscr.getmaxyx()
    data_height = max(1, h - 6)

   
    if context.filter == "all":
        filtered_lines = context.trace
    else:
        tag = "T"if context.filter.lower() == "tx" else "R"
        filtered_lines = [l for l in context.trace if tag in l]


    start_index = max(0, len(filtered_lines) - data_height)
    visible_lines= filtered_lines[start_index:]
    for i, line in enumerate(visible_lines):
           if i < data_height:
               attr = curses.color_pair(0)
               if "T" in line or " TX " in line:
                      attr = curses.color_pair(2)
               elif "R" in line or " RX " in line:
                      attr = curses.color_pair(1)
  
               _draw_text_safe(stdscr, i, 0, line, w - 1, attr)
   
    _draw_text_safe(stdscr, h - 5, 0, f"FILTRES:{context.filter} ", w - 1,curses.color_pair(4))
    _draw_text_safe(stdscr, h - 4, 0, f"TYPES:{context.display_mode}", w - 1,curses.color_pair(4))

    capture_status = "ACTIVE" if context.capture_active else "INACTIVE"

    status = (
        f"STATUS: {capture_status} | "
        f"Config:{context.config} | "
        f"BUF={context.buffer_size}/{context.max_buffer_size} "
    )

    _draw_text_safe(stdscr, h - 3, 0, status, w - 1, curses.color_pair(3))

    if context.message:
        _draw_text_safe(stdscr, h - 2, 0, context.message, w - 1)

    _draw_text_safe(stdscr, h - 1, 0, "> " + context.input_buffer, w - 1)
    try:
        stdscr.clrtoeol()
    except curses.error:
        pass

    stdscr.refresh()