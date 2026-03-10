"""
  APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés

  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : listener.py
  License : MIT License

  Ce module gère la réception des trames UART provenant de la carte.

  - Lire en continu les lignes reçues sur le port série (ser.readline()).

  - Distinguer les types de trames :
        * Trames de données de capture : commencent par '!' -> stockées dans trace_buffer
        * Trames de réponse commande : commencent par '#' -> stockées dans response_buffer

  - Décoder les trames de capture pour extraire :
        * DLC (Data Length Code) : longueur attendue du payload
        * direction : sens de la donnée (ex: 'T' ou 'R' selon ton protocole)
        * payload : octets de données
"""
import logging

logger = logging.getLogger(__name__)

def decode_data(frame: bytes) -> dict:
    """
    Décode une trame de données de capture.

    - '!' : octet indiquant une trame "DATA"
    - DLC : Data Length Code (longueur du payload en octets)
    - DIR : direction (1 caractère), par exemple :
        'T' = TX (donnée émise)
        'R' = RX (donnée reçue)
    - PAYLOAD : les données UART capturées

    Args:
        frame(bytes): trame lu dans le port série sans les caractères de fin de ligne (CR/LF).
    Returns:
        dict si la trame est valide (payload de longueur == DLC):
            {
                "direction": <str>,
                "payload": <bytes>
            }
        None si la trame est invalide ou incomplète.
    """
    if len(frame) < 3: # Vérifie qu'on a au moins '!', DLC et DIR
        return None
    dlc = frame[1]
    direction = frame[2:3].decode(errors='replace')
    payload = frame[3:]

    if len(payload) == dlc:
          return {
                  "direction": direction,
                  "payload": payload,
                                     }
    return None

def listener_thread(ser, stop_evt, capture_evt, trace_buffer, response_buffer,):
    """
    Thread de réception série.

    Fonction exécutée en boucle :
    - Lit une ligne depuis le port série (readline).
    - Supprime la fin de ligne CR/LF.
    - En fonction du premier caractère :
        * '!' : trame de cdonnée -> décodage puis stockage dans trace_buffer
        * '#' : trame de réponse -> extraction (cmd, result) puis stockage dans response_buffer

    Args:
        ser (objet serial):instance pyserial.
        stop_evt (threading.Event ): déclenche l'arrêt du thread.
        trace_buffer (queue.Queue): buffer de stockage des données décodées.
        response_buffer (queue.Queue): buffer de stockage des réponses de commandes.

    Variables locales:
        received_frame (bytes):Données brutes lues depuis le port série (incluant CR/LF).
        frame (bytes):Trame nettoyée sans caractères de fin de ligne.
        decoded_frame (dict | None):Résultat du décodage d'une trame de capture.
            Contient :
                {
                    "direction": str,
                    "payload": bytes
                }
        command_code (bytes):Code de la commande concernée par la réponse.
        command_success (bool):Indique si la commande a réussi (True) ou échoué (False).
  
    Returns:
        None
    """
    while not stop_evt.is_set():
        try:
            received_frame = ser.read_until(b'\n')
        except Exception:
            break
        if not received_frame:
            continue

        frame= received_frame.rstrip(b"\r\n")

        if frame.startswith(b"!"):
            decoded_frame= decode_data(frame)
            if decoded_frame:
                trace_buffer.put(decoded_frame)
            continue
       
        if frame.startswith(b"#") and len(frame) >= 3:
            command_code = frame[1:2]             
            command_success = (frame[2:3] == b"1")    
            response_buffer.put((command_code,command_success))
            logger.info(f"réponse commande : cmd={command_code} success={command_success}")
            continue
             
            
       