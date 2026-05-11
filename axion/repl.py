# author https://github.com/MIrrox27/Axion-Language
# repl.py

from axion.AxionTokens import *
from axion.AxionLexer import *
from axion.AxionParser import *
from axion.AxionASTNodes import *
from axion.AxionInterpreter import *
from axion import __version__, _check_author_maker



def repl():
    interpreter = AxionInterpreter()
    #print("Запуск через repl")
    print(f"Axion Language v{__version__} (c) 2024 Maksim Pronkin")
    #print(f"Version {__version__}")

    __all__ = [
        'AxionLexer.py',
        'AxionParser',
        'AxionInterpreter',
        'AxionTokenType',
        '__version__',
    ]

