"""
Alba Lexer — analizzatore lessicale per il linguaggio Alba
Converte il codice sorgente in una sequenza di token.
"""

import re
from dataclasses import dataclass
from enum import Enum, auto


# ─────────────────────────────────────────────
#  Tipi di token
# ─────────────────────────────────────────────

class TipoToken(Enum):
    # Parole chiave
    SE          = auto()
    ALTRIMENTI  = auto()
    FINCHE      = auto()
    PER_OGNI    = auto()
    IN          = auto()
    FUNZIONE    = auto()
    RESTITUISCI = auto()
    INTERROMPI  = auto()
    CONTINUA    = auto()
    PROVA       = auto()
    CATTURA     = auto()
    IMPORTA     = auto()
    CLASSE      = auto()
    SCRIVI      = auto()
    LEGGI       = auto()
    VERO        = auto()
    FALSO       = auto()
    NULLA       = auto()
    E           = auto()
    O           = auto()
    NON         = auto()

    # Tipi
    NUMERO_TIPO   = auto()
    TESTO_TIPO    = auto()
    BOOLEANO_TIPO = auto()
    LISTA_TIPO    = auto()

    # Letterali
    NUMERO      = auto()   # 42, 3.14
    STRINGA     = auto()   # "ciao"
    IDENTIF     = auto()   # nome variabile o funzione

    # Operatori aritmetici
    PIU         = auto()   # +
    MENO        = auto()   # -
    STAR        = auto()   # *
    SLASH       = auto()   # /
    PERCENTO    = auto()   # %

    # Operatori di confronto
    UGUALE      = auto()   # ==
    DIVERSO     = auto()   # !=
    MINORE      = auto()   # <
    MAGGIORE    = auto()   # >
    MIN_UGUALE  = auto()   # <=
    MAG_UGUALE  = auto()   # >=

    # Assegnazione e freccia
    ASSEGNA     = auto()   # =
    PIU_UGUALE  = auto()   # +=
    MENO_UGUALE = auto()   # -=
    STAR_UGUALE = auto()   # *=
    SLASH_UGUALE= auto()   # /=
    FRECCIA     = auto()   # ->

    # Punteggiatura
    APERTA      = auto()   # (
    CHIUSA      = auto()   # )
    QUADRA_AP   = auto()   # [
    QUADRA_CH   = auto()   # ]
    GRAFFA_AP   = auto()   # {
    GRAFFA_CH   = auto()   # }
    VIRGOLA     = auto()   # ,
    DUE_PUNTI   = auto()   # :
    PUNTO       = auto()   # .

    # Struttura
    NEWLINE     = auto()
    INDENT      = auto()
    DEDENT      = auto()
    FINE        = auto()   # fine del file


# ─────────────────────────────────────────────
#  Struttura Token
# ─────────────────────────────────────────────

@dataclass
class Token:
    tipo:   TipoToken
    valore: str
    riga:   int
    colonna: int

    def __repr__(self):
        return f"Token({self.tipo.name}, {self.valore!r}, riga={self.riga})"


# ─────────────────────────────────────────────
#  Eccezione del Lexer
# ─────────────────────────────────────────────

class ErroreLessicale(Exception):
    def __init__(self, messaggio, riga, colonna):
        super().__init__(f"[Riga {riga}, Col {colonna}] Errore lessicale: {messaggio}")
        self.riga = riga
        self.colonna = colonna


# ─────────────────────────────────────────────
#  Parole chiave
# ─────────────────────────────────────────────

PAROLE_CHIAVE = {
    "se":           TipoToken.SE,
    "altrimenti":   TipoToken.ALTRIMENTI,
    "finché":       TipoToken.FINCHE,
    "finche":       TipoToken.FINCHE,       # alias senza accento
    "per":          None,                   # gestita come "per ogni"
    "ogni":         None,                   # gestita insieme a "per"
    "in":           TipoToken.IN,
    "funzione":     TipoToken.FUNZIONE,
    "restituisci":  TipoToken.RESTITUISCI,
    "interrompi":   TipoToken.INTERROMPI,
    "continua":     TipoToken.CONTINUA,
    "prova":        TipoToken.PROVA,
    "cattura":      TipoToken.CATTURA,
    "importa":      TipoToken.IMPORTA,
    "classe":       TipoToken.CLASSE,
    "scrivi":       TipoToken.SCRIVI,
    "leggi":        TipoToken.LEGGI,
    "vero":         TipoToken.VERO,
    "falso":        TipoToken.FALSO,
    "nulla":        TipoToken.NULLA,
    "e":            TipoToken.E,
    "o":            TipoToken.O,
    "non":          TipoToken.NON,
    "numero":       TipoToken.NUMERO_TIPO,
    "testo":        TipoToken.TESTO_TIPO,
    "booleano":     TipoToken.BOOLEANO_TIPO,
    "lista":        TipoToken.LISTA_TIPO,
}


# ─────────────────────────────────────────────
#  Lexer principale
# ─────────────────────────────────────────────

class Lexer:
    """
    Trasforma una stringa di codice Alba in una lista di token.

    Gestisce:
    - Keyword italiane (incluso "per ogni" come token unico)
    - Indentazione significativa (INDENT / DEDENT come in Python)
    - Stringhe con apici doppi
    - Numeri interi e decimali
    - Commenti con #
    - Operatori multi-carattere (==, !=, <=, >=, ->)
    """

    def __init__(self, sorgente: str):
        self.sorgente = sorgente
        self.pos = 0
        self.riga = 1
        self.colonna = 1
        self.token: list[Token] = []
        self._stack_indent = [0]   # stack dei livelli di indentazione

    # ── Metodi di navigazione ──────────────────

    def _corrente(self) -> str | None:
        """Carattere corrente, o None se siamo alla fine."""
        return self.sorgente[self.pos] if self.pos < len(self.sorgente) else None

    def _prossimo(self) -> str | None:
        """Carattere successivo (lookahead di 1)."""
        p = self.pos + 1
        return self.sorgente[p] if p < len(self.sorgente) else None

    def _avanza(self) -> str:
        """Consuma il carattere corrente e aggiorna posizione."""
        ch = self.sorgente[self.pos]
        self.pos += 1
        if ch == "\n":
            self.riga += 1
            self.colonna = 1
        else:
            self.colonna += 1
        return ch

    def _aggiungi(self, tipo: TipoToken, valore: str, riga: int, col: int):
        self.token.append(Token(tipo, valore, riga, col))

    # ── Analisi indentazione ───────────────────

    def _gestisci_indentazione(self, spazi: int, riga: int):
        """
        Confronta il numero di spazi con lo stack.
        Emette INDENT se aumenta, DEDENT (anche multipli) se diminuisce.
        """
        livello_attuale = self._stack_indent[-1]

        if spazi > livello_attuale:
            self._stack_indent.append(spazi)
            self._aggiungi(TipoToken.INDENT, "", riga, 1)

        elif spazi < livello_attuale:
            while self._stack_indent[-1] > spazi:
                self._stack_indent.pop()
                self._aggiungi(TipoToken.DEDENT, "", riga, 1)
            if self._stack_indent[-1] != spazi:
                raise ErroreLessicale(
                    "Indentazione non coerente", riga, 1
                )

    # ── Tokenizzazione riga per riga ───────────

    def tokenizza(self) -> list[Token]:
        """
        Punto d'ingresso principale.
        Restituisce la lista completa di token.
        """
        righe = self.sorgente.splitlines(keepends=True)
        numero_riga = 0

        for linea in righe:
            numero_riga += 1

            # Salta righe vuote o solo commento
            strisciata = linea.strip()
            if not strisciata or strisciata.startswith("#"):
                continue

            # Conta spazi iniziali (usiamo solo spazi, non tab)
            spazi = len(linea) - len(linea.lstrip(" "))
            self._gestisci_indentazione(spazi, numero_riga)

            # Tokenizza il contenuto della riga
            self._tokenizza_riga(linea.rstrip("\n"), numero_riga, spazi)
            self._aggiungi(TipoToken.NEWLINE, "\n", numero_riga, len(linea))

        # Chiudi tutti gli INDENT aperti con DEDENT
        while len(self._stack_indent) > 1:
            self._stack_indent.pop()
            self._aggiungi(TipoToken.DEDENT, "", numero_riga + 1, 1)

        self._aggiungi(TipoToken.FINE, "", numero_riga + 1, 1)
        return self.token

    def _tokenizza_riga(self, linea: str, riga: int, offset: int):
        """Scansiona una singola riga emettendo i token."""
        i = offset   # partiamo dopo l'indentazione

        while i < len(linea):
            ch = linea[i]

            # Spazi interni
            if ch in " \t":
                i += 1
                continue

            # Commento
            if ch == "#":
                break

            col = i + 1   # colonne 1-based

            # ── Stringa ────────────────────────
            if ch == '"':
                j = i + 1
                while j < len(linea) and linea[j] != '"':
                    if linea[j] == "\\" and j + 1 < len(linea):
                        j += 1  # salta carattere escape
                    j += 1
                if j >= len(linea):
                    raise ErroreLessicale("Stringa non chiusa", riga, col)
                valore = linea[i+1:j]
                self._aggiungi(TipoToken.STRINGA, valore, riga, col)
                i = j + 1
                continue

            # ── Numero ─────────────────────────
            if ch.isdigit() or (ch == "-" and i + 1 < len(linea) and linea[i+1].isdigit()):
                j = i
                if ch == "-":
                    j += 1
                while j < len(linea) and (linea[j].isdigit() or linea[j] == "."):
                    j += 1
                self._aggiungi(TipoToken.NUMERO, linea[i:j], riga, col)
                i = j
                continue

            # ── Identificatore o parola chiave ─
            if ch.isalpha() or ch == "_" or ord(ch) > 127:
                j = i
                while j < len(linea) and (linea[j].isalnum() or linea[j] in "_èéàùìò" or ord(linea[j]) > 127):
                    j += 1
                parola = linea[i:j]

                # Caso speciale: "per ogni"
                if parola == "per":
                    resto = linea[j:].lstrip(" \t")
                    if resto.startswith("ogni"):
                        salto = linea[j:].index("ogni") + 4
                        self._aggiungi(TipoToken.PER_OGNI, "per ogni", riga, col)
                        i = j + salto
                        continue

                tipo = PAROLE_CHIAVE.get(parola.lower())
                if tipo and tipo is not None:
                    self._aggiungi(tipo, parola, riga, col)
                elif tipo is None and parola.lower() not in ("per", "ogni"):
                    self._aggiungi(TipoToken.IDENTIF, parola, riga, col)
                else:
                    self._aggiungi(TipoToken.IDENTIF, parola, riga, col)
                i = j
                continue

            # ── Operatori multi-char ───────────
            due = linea[i:i+2]
            if due == "==": self._aggiungi(TipoToken.UGUALE,      "==", riga, col); i += 2; continue
            if due == "!=": self._aggiungi(TipoToken.DIVERSO,     "!=", riga, col); i += 2; continue
            if due == "<=": self._aggiungi(TipoToken.MIN_UGUALE,  "<=", riga, col); i += 2; continue
            if due == ">=": self._aggiungi(TipoToken.MAG_UGUALE,  ">=", riga, col); i += 2; continue
            if due == "->": self._aggiungi(TipoToken.FRECCIA,     "->", riga, col); i += 2; continue
            if due == "+=": self._aggiungi(TipoToken.PIU_UGUALE,  "+=", riga, col); i += 2; continue
            if due == "-=": self._aggiungi(TipoToken.MENO_UGUALE, "-=", riga, col); i += 2; continue
            if due == "*=": self._aggiungi(TipoToken.STAR_UGUALE, "*=", riga, col); i += 2; continue
            if due == "/=": self._aggiungi(TipoToken.SLASH_UGUALE,"/=", riga, col); i += 2; continue

            # ── Operatori singolo char ─────────
            OPERATORI = {
                "+": TipoToken.PIU,
                "-": TipoToken.MENO,
                "*": TipoToken.STAR,
                "/": TipoToken.SLASH,
                "%": TipoToken.PERCENTO,
                "=": TipoToken.ASSEGNA,
                "<": TipoToken.MINORE,
                ">": TipoToken.MAGGIORE,
                "(": TipoToken.APERTA,
                ")": TipoToken.CHIUSA,
                "[": TipoToken.QUADRA_AP,
                "]": TipoToken.QUADRA_CH,
                "{": TipoToken.GRAFFA_AP,
                "}": TipoToken.GRAFFA_CH,
                ",": TipoToken.VIRGOLA,
                ":": TipoToken.DUE_PUNTI,
                ".": TipoToken.PUNTO,
            }
            if ch in OPERATORI:
                self._aggiungi(OPERATORI[ch], ch, riga, col)
                i += 1
                continue

            raise ErroreLessicale(f"Carattere non riconosciuto: {ch!r}", riga, col)


# ─────────────────────────────────────────────
#  Funzione di utilità
# ─────────────────────────────────────────────

def tokenizza(sorgente: str) -> list[Token]:
    """Scorciatoia: crea il Lexer e restituisce i token."""
    return Lexer(sorgente).tokenizza()


# ─────────────────────────────────────────────
#  Demo — eseguibile direttamente
# ─────────────────────────────────────────────

if __name__ == "__main__":
    codice_esempio = """\
# Calcolo del fattoriale
funzione fattoriale(n: numero) -> numero
    se n <= 1
        restituisci 1
    altrimenti
        restituisci n * fattoriale(n - 1)

risultato = fattoriale(5)
scrivi("5! = " + risultato)

# Ciclo su una lista
numeri = [1, 2, 3, 4, 5]
per ogni n in numeri
    se n % 2 == 0
        scrivi(n + " è pari")
    altrimenti
        scrivi(n + " è dispari")
"""

    print("═" * 50)
    print("  Alba Lexer — output token")
    print("═" * 50)

    try:
        tokens = tokenizza(codice_esempio)
        for tok in tokens:
            print(tok)
        print(f"\n✓ Tokenizzazione completata: {len(tokens)} token trovati")
    except ErroreLessicale as e:
        print(f"\n✗ {e}")
