"""
  APP_python_MVC - Application permettant de piloter l'espion UART, et d'afficher les traces relevés
  
  Auteur : Mame Diarra Diop
  Date : 03/03/2026
  Fichier : config_uart.py
  License : MIT License

  Ce module définit la configuration UART.
  Il fournit :
    - Une liste de valeurs autorisées (baud, bits, parité, stop bits, fin de trame).
    - La classe ConfigUART qui :
        * valide les paramètres,
        * expose les paramètres via des propriétés,
        * génère une trame de commande SET conforme au protocole pour envoyer la configuration.
"""

from app_python_mvc.models.frame_builder import build_frame
from app_python_mvc.constants import  BAUDRATE, BYTESIZE, STOPBITS, PARITY, CMD_SET, FRAME_END

BAUD_CODES = [
            "1200",
            "4800",
            "9600",
            "19200",
            "38400",
            "57600",
            "115200",
            "230400",
            "460800",
]

BYTES_CODES = [
            "5",
            "6",
            "7",
            "8"      
]

STOPS_CODES = [
            "1",
            "1.5",
            "2"
]

PARITY_CODES = [
            "N",
            "E",
            "O"
]

FRAME_END_CODES = [
    "LF",
    "CR",
    "CRLF"
]

DEFAULT_BYTES_SIZE = '8'
DEFAULT_PARITY = 'N'
DEFAULT_STOP_BITS = '1'
DEFAULT_FRAME_END ="CRLF"

class SpyDeviceConfigUART:
    """ 
    """
    def __init__(self, baud : str = None, bits : str = None, parity : str = None, stopbits : str = None, frame_end: str = "CRLF")-> None:
        """
        Initialise une configuration UART

        Args:
            baud (str, optional): Débit UART en texte. Defaults to None.
            bits (str, optional): Nombre de bits de données. Defaults to None.
            parity (str, optional): Parité. Defaults to None.
            stopbits (str, optional): Bit de stop. Defaults to None.
            frame_end (str, optional):Fin de trame. Defaults to "CRLF".
        """
        self.baud = baud
        self.bits = bits or DEFAULT_BYTES_SIZE
        self.parity = parity or DEFAULT_PARITY 
        self.stopbits = stopbits or DEFAULT_STOP_BITS
        self.frame_end = frame_end or DEFAULT_FRAME_END
        
        
    def __repr__(self) ->str:
        """
        Retourne une représentation textuelle de la configuration UART.

        Returns:
            str:Chaine représentant la configuration UART actuelle
        """
        return f"{self._baud} {self._bits} {self._parity} {self._stopbits} {self._frame_end}"

    
    def build_set_command_frame(self)->bytes:
        """
         Construit une trame de commande SET contenant les paramètres UART encodés.

        Raises:
            ValueError: Si un paramètre n'a pas de correspondance dans les tables de conversion.

        Returns:
            bytes: Trame SET complète prête à être envoyée sur le port série.
        """
        try:
            baud_code = BAUDRATE[self._baud]
            bits_code = BYTESIZE[self._bits]
            parity_code = PARITY[self._parity]
            stop_code = STOPBITS[self._stopbits]
            frame_end = FRAME_END[self.frame_end]

            params = baud_code + bits_code+ parity_code + stop_code + frame_end

            return build_frame(CMD_SET, params)
        
        except KeyError as e:
            raise ValueError(f"Paramètre UART invalide : {e}")     


    @property
    def baud(self)->str:
        """
        Débit uart configuré.

        Returns:
            str: valeur du baudrate 
        """
        return self._baud
    
    @baud.setter
    def baud (self, value: str)-> None:
        """
        Définit la validité du baudrate choisi par l'utilisateur.

        Args:
            value (str):nouvelle valeur de la baudrate 

        Raises:
            ValueError: Si la valeur est invalide
        """
        if value in BAUD_CODES:
            self._baud = value
        else:
            raise ValueError(f"parametre baud invalide")

    
    @property
    def bits(self)-> str:
        """
        Nombre de bits de données UART.

        Returns:
            str:valeur du nombre de bits
        """
        return self._bits
    
    @bits.setter
    def bits (self, value: str)-> None:
        """
        Définit la validité du nombre de bit choisi par l'utilisateur.

        Args:
            value (str): nouvelle valeur du nombre biis 

        Raises:
            ValueError: si la valeur est invalide
        """
        if value in BYTES_CODES:
            self._bits = value
        else:
            raise ValueError(f"nombre de bits invalide") 
    
    @property
    def parity(self)->str:
        """
        Type de Parité UART configuré

        Returns:
            str: la parité choisie("N", "E", "O")
        """
        return self._parity
    

    @parity.setter
    def parity (self, value: str)->None:
        """
        Définit la validité du type de parité choisi par l'utilisateur.

        Args:
            value (str): nouveau type de parité

        Raises:
            ValueError: Si la valeur est invalide
        """
        value = value.upper()
        if value in  PARITY_CODES: 
            self._parity = value
        else:
            raise ValueError(f"parité invalide ")
    
    @property
    def stopbits(self)->str:
        """_
        Nombre de bits de stop UART.

        Returns:
            str: Valeur du bits de stop
        """
        return self._stopbits
    
    @stopbits.setter
    def stopbits (self, value: str)->None:
        """
        Définit la validité du nombre de bit de stop choisi par l'utilisateur.

        Args:
            value (str):nouvelle valeur du bits de stop

        Raises:
            ValueError: si la valeur est invalide
        """
        if value in STOPS_CODES:
            self._stopbits = value
        else:
            raise ValueError(f"nombre de bits de stop invalide")
    
    @property
    def frame_end(self) -> str:
        """
        Type de fin de trame utilisé pour les données à capturer

        Returns:
            str: Fin de trame choisi
        """
        return self._frame_end

    @frame_end.setter
    def frame_end(self, value: str)-> None:
        """
        Définit la validité du type de fin de trame choisi.

        Args:
            value (str):Type de fin de trame

        Raises:
            ValueError: Si la valeur est invalide
        """
        value = value.upper()
        if value in FRAME_END_CODES:
            self._frame_end = value
        else:
            raise ValueError("fin de trame invalide (LF / CR / CRLF)")
    
       


   
            


        
