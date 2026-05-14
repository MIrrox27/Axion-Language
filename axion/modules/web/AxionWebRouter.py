# # author https://github.com/MIrrox27/Axion-Language
# AxionWebRouter.py

import json
import re
#from axion.modules.web.AxionWebModule import *


class Router:
    def __init__(self):
        self.routes = []

    def add(self, method, pattern, handler):
        self.routes.append((method, pattern, handler))

    def match(self, method, path):
        for m, p, h in self.routes:
            if m == method and p == path:
                return  h, {}

        return None, None



