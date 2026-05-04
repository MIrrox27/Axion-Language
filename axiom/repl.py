# author https://github.com/MIrrox27/Axiom-Language
# repl.py

from axiom.AxiomTokens import *
from axiom.AxiomLexer import *
from axiom.AxiomParser import *
from axiom.AxiomASTNodes import *
from axiom.AxiomInterpreter import *
from axiom import __version__, _check_author_maker



def repl():
    interpreter = AxiomInterpreter()
    #print("Запуск через repl")
    print(f"Axiom Language v{__version__} (c) 2024 Maksim Pronkin")
    #print(f"Version {__version__}")

    __all__ = [
        'AxiomLexer',
        'AxiomParser',
        'AxiomInterpreter',
        'AxiomTokenType',
        '__version__',
    ]

