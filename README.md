# APP_python_MVC

Application PC permettant de piloter un espion UART et d'afficher les traces capturées en temps réel.

Le programme permet d’envoyer des commandes à un dispositif embarqué (par exemple un Raspberry Pi Pico) et d’afficher les données UART interceptées via une interface terminal.

---

# 📌 Fonctionnalités

* Communication série avec un dispositif embarqué
* Capture de trames UART en temps réel
* Interface utilisateur dans le terminal (bibliothèque `curses`)
* Commandes interactives (start, stop, set, log)
* Filtrage des trames (ALL / TX / RX)
* Affichage des données en **HEX** ou **ASCII**
* Sauvegarde des traces dans un fichier log
* Sauvegarde automatique des paramètres de configuration

---

# 🏗 Architecture logicielle

Le projet suit une architecture **MVC (Model – View – Controller)**.

| Composant      | Rôle                                              |
| -------------- | ------------------------------------------------- |
| **Model**      | Gestion de la communication série et des buffers  |
| **View**       | Interface utilisateur terminal (curses)           |
| **Controller** | Logique de l'application et gestion des commandes |

Schéma simplifié :

```
Utilisateur
    │
    ▼
  View
    │
    ▼
Controller
    │
    ▼
  Model
    │
    ▼
Espion UART (microcontrôleur)
```

---

# 📂 Structure du projet

```
APP_python_MVC/
│
├── main.py                 # Point d'entrée de l'application
├── controller.py           # Contrôleur principal
├── process_commands.py     # Traitement des commandes utilisateur
├── setting.py              # Chargement / sauvegarde des paramètres
├── logger.py               # Gestion des logs
│
├── models/
│   ├── model.py            # Communication série
│   ├── frame_builder.py    # Construction des trames
│   └── config_uart.py      # Configuration UART
│
├── views/
│   ├── view.py             # Interface curses
│   └── ui_messages.py      # Gestion des messages UI
│
├── listener.py             # Réception des trames UART
├── sender.py               # Construction des commandes
├── filter.py               # Gestion des filtres d'affichage
├── interfacecontexte.py    # Etat de l'interface utilisateur
│
├── constants.py            # Constantes globales
└── logs/                   # Dossier de sauvegarde des traces
```

---

# ⚙️ Installation

### 1️⃣ Cloner le projet

```
git clone https://github.com/ton-utilisateur/APP_python_MVC.git
cd APP_python_MVC
```

### 2️⃣ Installer les dépendances

```
pip install pyserial
```

---

# ▶️ Lancer l'application

Lister les ports série disponibles :

```
python main.py --list-ports
```

Exemple de sortie :

```
Ports disponibles :
  /dev/ttyUSB0 - USB Serial Device
```

Lancer l'application :

```
python main.py --port /dev/ttyUSB0
```

Windows :

```
python main.py --port COM3
```

---

# 🖥 Commandes disponibles

| Commande        | Description                     |
| --------------- | ------------------------------- |
| `start`         | démarre la capture UART         |
| `stop`          | arrête la capture               |
| `set`           | configure les paramètres UART   |
| `log`           | sauvegarde les traces capturées |
| `help`          | affiche l'aide                  |
| `exit` / `quit` | quitte l'application            |

---

# ⚙️ Configuration UART

Commande :

```
set <baud> <bits> <parity> <stopbits> <frame_end>
```

Exemple :

```
set 115200 8 N 1 CRLF
```

---

# 🧾 Format des trames

### Trame de commande

```
# + CMD + PARAMS + CRLF
```

Exemple :

```
#START\r\n
```

### Trame de données

```
! + DLC + DIR + PAYLOAD
```

| Champ     | Description          |
| --------- | -------------------- |
| `!`       | début de trame       |
| `DLC`     | longueur des données |
| `DIR`     | direction (TX / RX)  |
| `PAYLOAD` | données UART         |

---

# 📝 Logs

Les traces peuvent être sauvegardées dans un fichier :

```
logs/uart_log_YYYYMMDD_HHMMSS.txt
```

---

# 💾 Sauvegarde des paramètres

Les paramètres sont sauvegardés automatiquement dans un fichier JSON :

```
settings.json
```

---

# 👩‍💻 Auteur

**Mame Diarra Diop**

Projet réalisé dans le cadre d'un stage.

---

# 📜 Licence

MIT License
