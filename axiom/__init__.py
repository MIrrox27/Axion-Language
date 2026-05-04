# author https://github.com/MIrrox27/Axiom-Language
# __init__.py


__version__ = "0.2.3"

import os, sys

def _check_author_maker():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    required_marker = "# author https://github.com/MIrrox27/Axiom-Language"

    for filename in os.listdir(current_dir):
        if filename.endswith('.py') and not filename.startswith("__"):
            filepath = os.path.join(current_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line != required_marker:
                        raise RuntimeError(
                            f"Integrity check failed: {filename} does not contain required author marker.\n"
                            f"All Axiom source files must start with: {required_marker}"
                        )

            except Exception as e:
                print(f'Fatal error: {e}')
                sys.exit(1)

_check_author_maker()

import builtins
builtins.__axiom_verified__ = True

from axiom.AxiomTokens import *
from axiom.AxiomLexer import *
from axiom.AxiomParser import *
from axiom.AxiomASTNodes import *
from axiom.AxiomInterpreter import *
from axiom.repl import *