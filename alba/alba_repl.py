"""
Alba REPL — shell interattiva per il linguaggio Alba.
Esegui con:  python alba_repl.py
"""

import sys
from alba_interpreter import Interpreter, ErroreEsecuzione
from alba_parser import ErroreSintattico
from alba_lexer import ErroreLessicale
from alba_errori import stampa_errore

BANNER = """
╔══════════════════════════════════════════╗
║        Alba  —  linguaggio educativo     ║
║        digita  :aiuto  per i comandi     ║
╚══════════════════════════════════════════╝
"""

AIUTO = """
Comandi speciali:
  :aiuto      mostra questo messaggio
  :esci       chiude il REPL
  :pulisci    azzera tutte le variabili
  :vars       mostra le variabili definite

Blocchi multiriga:
  Inizia una riga con 'funzione', 'se', 'classe', ecc.
  Alba raccoglie le righe finché non inserisci una riga vuota.
"""

PAROLE_BLOCCO = ("funzione", "se", "finché", "finche", "per ogni", "classe")


def avvia_repl():
    interprete = Interpreter()
    print(BANNER)

    buffer: list[str] = []
    in_blocco = False

    while True:
        try:
            prompt = "... " if in_blocco else ">>> "
            try:
                riga = input(prompt)
            except EOFError:
                print("\nArrivederci!")
                break

            # ── Comandi speciali ──────────────────
            if not in_blocco:
                if riga.strip() == ":esci":
                    print("Arrivederci!")
                    break

                if riga.strip() == ":aiuto":
                    print(AIUTO)
                    continue

                if riga.strip() == ":pulisci":
                    interprete = Interpreter()
                    print("Ambiente azzerato.")
                    continue

                if riga.strip() == ":vars":
                    vars_utente = {
                        k: v for k, v in interprete.globale._vars.items()
                        if not callable(v)
                    }
                    if vars_utente:
                        for nome, valore in vars_utente.items():
                            print(f"  {nome} = {interprete._a_testo(valore)}")
                    else:
                        print("  (nessuna variabile definita)")
                    continue

            # ── Gestione blocchi multiriga ────────
            strisciata = riga.strip()

            # Riga vuota chiude il blocco
            if in_blocco and strisciata == "":
                codice = "\n".join(buffer)
                buffer = []
                in_blocco = False
                _esegui(interprete, codice)
                continue

            # Inizia un blocco
            if any(strisciata.startswith(kw) for kw in PAROLE_BLOCCO):
                in_blocco = True
                buffer.append(riga)
                continue

            # Continua il blocco (riga indentata)
            if in_blocco:
                buffer.append(riga)
                continue

            # ── Esecuzione riga singola ───────────
            if strisciata:
                _esegui(interprete, riga)

        except KeyboardInterrupt:
            print("\n(interrotto — usa :esci per uscire)")
            buffer = []
            in_blocco = False


def _esegui(interprete: Interpreter, codice: str):
    """Esegue il codice e gestisce gli errori in modo leggibile."""
    try:
        risultato = interprete.esegui(codice)
        if risultato is not None and not codice.strip().startswith("scrivi"):
            print(interprete._a_testo(risultato))
    except (ErroreLessicale, ErroreSintattico, ErroreEsecuzione) as e:
        stampa_errore(e, codice)
    except Exception as e:
        stampa_errore(e, codice)


if __name__ == "__main__":
    avvia_repl()
