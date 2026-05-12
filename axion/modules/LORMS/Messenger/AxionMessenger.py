# author https://github.com/MIrrox27/Axion-Language
# AxionMessenger.py

from axion.modules.LORMS.AxionLORMSModule import Messenger

from pathlib import Path
from socketserver import ThreadingMixIn

import threading
import urllib.parse
import json
import time
import socket


class MessengerHTTP(Messenger):
    current_path = Path(__file__).parent
    templates_html = '../templates/Messenger/html/'

    templates = {
        "chat": current_path / f"{templates_html}chat.html",
        "register": current_path / f"{templates_html}register.html"
    }

    messages = [] # потом будет {"user" : "message"}









