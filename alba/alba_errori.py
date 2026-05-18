"""
Alba Errori — formattazione leggibile degli errori con evidenziazione della riga.
"""

# Codici ANSI (disabilitabili se il terminale non li supporta)
import os
_COLORI = os.environ.get("ALBA_NO_COLOR", "") == "" and os.name != "nt" or \
          os.environ.get("FORCE_COLOR", "") != ""

def _rosso(s):    return f"\033[91m{s}\033[0m" if _COLORI else s
def _giallo(s):   return f"\033[93m{s}\033[0m" if _COLORI else s
def _grigio(s):   return f"\033[90m{s}\033[0m" if _COLORI else s
def _grassetto(s):return f"\033[1m{s}\033[0m"  if _COLORI else s
def _ciano(s):    return f"\033[96m{s}\033[0m"  if _COLORI else s


# ─────────────────────────────────────────────
#  Classi base degli errori
# ─────────────────────────────────────────────

class ErroreAlba(Exception):
    """Classe base per tutti gli errori di Alba."""
    def __init__(self, messaggio: str, riga: int = 0, colonna: int = 0, sorgente: str = ""):
        self.messaggio = messaggio
        self.riga = riga
        self.colonna = colonna
        self.sorgente = sorgente
        super().__init__(self.formatta())

    def tipo_errore(self) -> str:
        return "Errore"

    def formatta(self) -> str:
        return formatta_errore(
            tipo=self.tipo_errore(),
            messaggio=self.messaggio,
            riga=self.riga,
            colonna=self.colonna,
            sorgente=self.sorgente,
        )


class ErroreLessicaleAlba(ErroreAlba):
    def tipo_errore(self): return "Errore lessicale"

class ErroreSintaticoAlba(ErroreAlba):
    def tipo_errore(self): return "Errore sintattico"

class ErroreEsecuzioneAlba(ErroreAlba):
    def tipo_errore(self): return "Errore di esecuzione"


# ─────────────────────────────────────────────
#  Formattatore principale
# ─────────────────────────────────────────────

def formatta_errore(
    tipo: str,
    messaggio: str,
    riga: int = 0,
    colonna: int = 0,
    sorgente: str = "",
) -> str:
    """
    Produce un messaggio di errore multiriga con:
    - tipo e descrizione
    - riga di codice incriminata
    - freccia che punta alla colonna (se disponibile)
    - suggerimento (se riconosciuto)
    """
    linee = []

    # ── Intestazione ─────────────────────────
    intestazione = _grassetto(_rosso(f"✗ {tipo}"))
    if riga > 0:
        intestazione += _grigio(f"  [riga {riga}]")
    linee.append(intestazione)
    linee.append(_grassetto(f"  {messaggio}"))

    # ── Contesto del codice ───────────────────
    if sorgente and riga > 0:
        righe_src = sorgente.splitlines()
        ctx_inizio = max(0, riga - 3)
        ctx_fine   = min(len(righe_src), riga + 1)

        linee.append("")
        for nr in range(ctx_inizio, ctx_fine):
            testo_riga = righe_src[nr]
            num = str(nr + 1).rjust(4)

            if nr + 1 == riga:
                # Riga con l'errore
                linee.append(_rosso(f" {num} │ ") + _grassetto(testo_riga))
                # Freccia sotto
                if colonna > 0:
                    spazio = " " * (colonna + 6)
                    linee.append(_rosso(f"{spazio}^"))
                else:
                    # evidenzia tutta la riga
                    spazio = "      "
                    linee.append(_rosso(f"{spazio}" + "─" * max(1, len(testo_riga.rstrip()))))
            else:
                linee.append(_grigio(f" {num} │ {testo_riga}"))

    # ── Suggerimento ──────────────────────────
    suggerimento = _suggerisci(messaggio)
    if suggerimento:
        linee.append("")
        linee.append(_ciano(f"  💡 {suggerimento}"))

    linee.append("")
    return "\n".join(linee)


# ─────────────────────────────────────────────
#  Suggerimenti automatici
# ─────────────────────────────────────────────

_SUGGERIMENTI = [
    ("Divisione per zero",
     "Controlla che il divisore non sia zero prima di dividere."),
    ("non definita",
     "Hai dimenticato di assegnare un valore a questa variabile?"),
    ("non è una funzione",
     "Stai cercando di chiamare qualcosa che non è una funzione. Controlla il nome."),
    ("non ha il metodo",
     "Controlla i metodi disponibili: lista → aggiungi, rimuovi, lunghezza; testo → maiuscolo, minuscolo, dividi…"),
    ("Stringa non chiusa",
     'Le stringhe devono iniziare e finire con le virgolette doppie: "ciao".'),
    ("Indentazione non coerente",
     "Usa sempre 4 spazi per ogni livello di indentazione. Non mescolare spazi e tab."),
    ("Indice",
     "Gli indici partono da 0: il primo elemento è lista[0], non lista[1]."),
    ("Ciclo infinito",
     "La condizione del ciclo non diventa mai falsa. Assicurati di modificare la variabile nel corpo."),
    ("argomenti, ricevuti",
     "Il numero di argomenti passati non corrisponde a quelli dichiarati nella funzione."),
    ("non trovata nel dizionario",
     "Usa dizionario.chiavi() per vedere le chiavi disponibili."),
    ("Atteso INDENT",
     "Il corpo di funzione, se, finché o per ogni deve essere indentato di 4 spazi."),
    ("Atteso",
     "Controlla la sintassi: potrebbe mancare una parentesi, una virgola o una parola chiave."),
    ("Modulo",
     "Il file da importare deve trovarsi nella stessa cartella del programma Alba."),
]

def _suggerisci(messaggio: str) -> str:
    for parola_chiave, suggerimento in _SUGGERIMENTI:
        if parola_chiave.lower() in messaggio.lower():
            return suggerimento
    return ""


# ─────────────────────────────────────────────
#  Funzione di utilità per il REPL e i test
# ─────────────────────────────────────────────

def stampa_errore(errore: Exception, sorgente: str = "") -> None:
    """
    Stampa un errore in modo leggibile.
    Funziona con ErroreAlba, ErroreLessicale, ErroreSintattico e Exception generiche.
    """
    # Import locale per evitare import circolari
    from alba_lexer import ErroreLessicale
    from alba_parser import ErroreSintattico
    from alba_interpreter import ErroreEsecuzione

    if isinstance(errore, ErroreAlba):
        print(errore.formatta())
        return

    riga = getattr(errore, "riga", 0)
    col  = getattr(errore, "colonna", 0)
    msg  = str(errore)

    # Pulisce messaggi tipo "[Riga 5] Errore di esecuzione: ..."
    for prefisso in ["Errore lessicale: ", "Errore sintattico: ", "Errore di esecuzione: "]:
        if prefisso in msg:
            msg = msg.split(prefisso, 1)[-1]
            break

    if isinstance(errore, ErroreLessicale):
        tipo = "Errore lessicale"
    elif isinstance(errore, ErroreSintattico):
        tipo = "Errore sintattico"
    elif isinstance(errore, ErroreEsecuzione):
        tipo = "Errore di esecuzione"
    else:
        tipo = "Errore interno"

    print(formatta_errore(tipo, msg, riga, col, sorgente))
