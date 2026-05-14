# # author https://github.com/MIrrox27/Axion-Language
# Общие основные классы

import http, requests, urllib, webbrowser, socket, ssl
import json, socketserver
from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler

from axion.modules.web import AxionWebRouter, AxionWebRequest, AxionWebResponse

class Output:
    def __init__(self, module):
        self.module = module

    def debug(self, msg, out=False):
        if out: print(f"[DEBUG]: {msg}")

    def error(self, msg, func=None):
        raise Exception(f"[{self.module}]-[{func}]: {msg}")

    def log(self, msg, out=False):
        if out: print(f"[LOG]: {msg}")







