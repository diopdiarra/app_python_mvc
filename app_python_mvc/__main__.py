"""
  APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés
  
  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : main.py
  License : MIT License

  Ce module constitue le point d'entrée principal de l'application.
"""
import threading
import serial
import argparse
import sys
import logging
import time

from typing import Sequence
from serial.tools import list_ports 

from app_python_mvc.constants import BAUD, LOG_FILE
from app_python_mvc.models.model import AppModel
from app_python_mvc.views.view import AppView
from app_python_mvc.controler import AppControler

LOGGER = logging.getLogger("uart_spy")

def configure_logging() -> None:
    """Configure l'enregistrement des logs de l'application dans un fichier.
    """
    logging.basicConfig(
        filename=LOG_FILE,
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

def available_ports() -> list[str]:
    """ Récupère la liste des ports série disponibles sur le système.

    Returns:
        list[str]:Liste des noms de ports série détectés
    """
    return [p.device for p in list_ports.comports()]

def is_valid_port(port_name: str, ports: Sequence[str] | None = None) -> bool:
    """ Vérifie si un port série donné est valide.

    Args:
        port_name (str): Nom du port série à vérifier.
        ports (Sequence[str] | None, optional): Liste des ports disponibles.Defaults to None
            
    Returns:
        bool: _description_
    """
    ports = list(ports) if ports is not None else available_ports()
    return port_name in ports

def print_ports() -> None:
    """Affiche la liste des ports série disponibles sur le système.
    """
    ports = list_ports.comports()
    if not ports:
        print("Aucun port série détecté.")
        return
    print("Ports disponibles :")
    for p in ports:
        if p.description != "n/a": 
          desc = f" - {p.description}" if getattr(p, "description", None) else ""
          print(f"  {p.device}{desc}")

def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """ Analyse les arguments fournis en ligne de commande.

    Args:
        argv (Sequence[str] | None, optional):Liste des arguments passés au programme en ligne de commande. Defaults to None.

    Returns:
        argparse.Namespace: Objet contenant les arguments analysés.
    """
    parser = argparse.ArgumentParser(description="UART Spy Tool")
    parser.add_argument("--port", help="Port série (ex: /dev/ttyUSB0, COM3)")
    parser.add_argument(
        "--list-ports",
        action="store_true",
        help="Affiche les ports série disponibles et quitte",
    )
    return parser.parse_args(argv)

def run_app(port: str) -> int:
    """Lance l'application principale.
    Args:
        port (str):Nom du port série à utiliser.

    Returns:
        int: Code de retour de l'application :
                0 : arrêt normal
                1 : erreur port série
                2 : erreur inattendue
    """
    LOGGER.info("Démarrage application (port=%s, baud=%s)", port, BAUD)

    capture_evt = threading.Event()
    stop_evt = threading.Event()

    try:
        ser = None
        for _ in range(5):  # 5 tentatives
            try:
                ser = serial.Serial(port, BAUD, timeout=0.2)
                break
            except serial.SerialException:
                LOGGER.warning("Port %s pas encore prêt, nouvelle tentative...", port)
                time.sleep(0.5)

        if ser is None:
            print(f"Impossible d'ouvrir le port : {port}")
            return 1

        with ser:
            model = AppModel(ser, stop_evt, capture_evt)
            view = AppView(stop_evt)
            controller = AppControler(model, view)

            try:
                controller.run()
            finally:
                model.stop_listener()

        LOGGER.info("Arrêt application (normal).")
        return 0

    except KeyboardInterrupt:
        LOGGER.info("Arrêt application (Ctrl+C).")
        return 0

    except serial.SerialException:
        LOGGER.exception("Erreur ouverture/usage du port série")
        print(f"Erreur ouverture port : {port}")
        return 1

    except Exception:
        LOGGER.exception("Erreur inattendue")
        print("Erreur inattendue (voir app.log).")
        return 2   


def main(argv: Sequence[str] | None = None)->int:
    """  Fonction principale de l'application.

    Args:
        argv (Sequence[str] | None, optional): Arguments de ligne de commande.. Defaults to None.

    Returns:
        int: Code de sortie de l'application.
    """
    configure_logging()
    
    args = parse_args(argv)

    if args.list_ports:
        print_ports()
        return 0

    if not args.port:
        print("Erreur: --port est requis (ou utilisez --list-ports).")
        return 2

    ports = available_ports()
    if not is_valid_port(args.port, ports):

        print(f"Port {args.port} indisponible, recherche automatique...")

        args.port = None

        # attendre qu'un port ACM apparaisse et soit ouvrable
        for _ in range(10):

            ports = available_ports()

            for p in ports:
                if p.startswith("/dev/ttyACM"):

                    try:
                        test = serial.Serial(p, BAUD, timeout=0.2)
                        test.close()

                        args.port = p
                        print(f"Port trouvé automatiquement : {p}")
                        break

                    except serial.SerialException:
                        pass

            if args.port:
                break

            time.sleep(0.5)

        if not args.port:
            print("Aucun port espion disponible.")
            print_ports()
            return 2

    return run_app(args.port)
                    

if __name__ == "__main__":
  raise SystemExit(main())