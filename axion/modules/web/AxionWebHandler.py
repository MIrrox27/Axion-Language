# author https://github.com/MIrrox27/Axion-Language
# AxionWebHandler

from axion.modules.web.AxionWebModule import *

class WebHandler(BaseHTTPRequestHandler):
    router = None


    def do_GET(self):
        router = self.__class__.router
        headers, params = self.__class__.router.match("GET", self.path)

        



    def do_POST(self):
        pass

    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass
