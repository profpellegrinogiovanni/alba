"""
Alba — punto di avvio per la versione .exe
"""
import sys
import os

# Assicura che i file del progetto siano trovabili
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

from alba_repl import avvia_repl

if __name__ == "__main__":
    avvia_repl()
