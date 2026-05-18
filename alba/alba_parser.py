"""
Alba Parser — costruisce l'Albero Sintattico Astratto (AST)
a partire dalla lista di token prodotta dal Lexer.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from alba_lexer import Token, TipoToken, tokenizza


# ─────────────────────────────────────────────
#  Nodi dell'AST
# ─────────────────────────────────────────────

@dataclass
class NodoNumero:
    """Letterale numerico: 42, 3.14"""
    valore: float
    riga: int

@dataclass
class NodoStringa:
    """Letterale stringa: "ciao" """
    valore: str
    riga: int

@dataclass
class NodoBooleano:
    """Letterale booleano: vero, falso"""
    valore: bool
    riga: int

@dataclass
class NodoNulla:
    """Valore nulla"""
    riga: int

@dataclass
class NodoIdentificatore:
    """Nome di variabile o funzione: x, risultato"""
    nome: str
    riga: int

@dataclass
class NodoAssegnazione:
    """x = espressione"""
    nome: str
    valore: "Espressione"
    riga: int

@dataclass
class NodoBinario:
    """Operazione binaria: a + b, x == y"""
    operatore: str
    sinistra: "Espressione"
    destra: "Espressione"
    riga: int

@dataclass
class NodoUnario:
    """Operazione unaria: non x"""
    operatore: str
    operando: "Espressione"
    riga: int

@dataclass
class NodoChiamata:
    """Chiamata funzione: fattoriale(5)"""
    nome: str
    argomenti: list["Espressione"]
    riga: int

@dataclass
class NodoAccesso:
    """Accesso attributo: oggetto.metodo"""
    oggetto: "Espressione"
    attributo: str
    riga: int

@dataclass
class NodoChiamataMetodo:
    """Chiamata metodo: oggetto.metodo(args)"""
    oggetto: "Espressione"
    metodo: str
    argomenti: list["Espressione"]
    riga: int

@dataclass
class NodoLista:
    """Lista letterale: [1, 2, 3]"""
    elementi: list["Espressione"]
    riga: int

@dataclass
class NodoSe:
    """se condizione\n    blocco\naltrimenti\n    blocco"""
    condizione: "Espressione"
    corpo: list["Istruzione"]
    altrimenti: list["Istruzione"]
    riga: int

@dataclass
class NodoFinche:
    """finché condizione\n    blocco"""
    condizione: "Espressione"
    corpo: list["Istruzione"]
    riga: int

@dataclass
class NodoPerOgni:
    """per ogni elemento in lista\n    blocco"""
    variabile: str
    iterabile: "Espressione"
    corpo: list["Istruzione"]
    riga: int

@dataclass
class NodoFunzione:
    """funzione nome(params) -> tipo\n    corpo"""
    nome: str
    parametri: list[tuple[str, Optional[str]]]   # (nome, tipo_opzionale)
    tipo_ritorno: Optional[str]
    corpo: list["Istruzione"]
    riga: int

@dataclass
class NodoRestituisci:
    """restituisci espressione"""
    valore: Optional["Espressione"]
    riga: int

@dataclass
class NodoInterrompi:
    """interrompi — esce dal ciclo"""
    riga: int

@dataclass
class NodoContinua:
    """continua — passa all'iterazione successiva"""
    riga: int

@dataclass
class NodoProvaCattura:
    """prova … cattura errore … """
    corpo: list["Istruzione"]
    var_errore: Optional[str]
    cattura: list["Istruzione"]
    riga: int

@dataclass
class NodoDizionario:
    """Dizionario letterale: {"chiave": valore}"""
    coppie: list[tuple["Espressione", "Espressione"]]
    riga: int

@dataclass
class NodoImporta:
    """importa "modulo.alba" """
    percorso: str
    riga: int

@dataclass
class NodoClasse:
    """classe Nome(Genitore)\n    attributi e metodi"""
    nome: str
    genitore: Optional[str]                       # nome classe genitore o None
    attributi: list[tuple[str, str]]
    metodi: list[NodoFunzione]
    riga: int

@dataclass
class NodoScrivi:
    """scrivi(espressione)"""
    valore: "Espressione"
    riga: int

@dataclass
class NodoLeggi:
    """leggi(prompt)"""
    prompt: Optional["Espressione"]
    riga: int

@dataclass
class NodoIndice:
    """Accesso per indice: lista[0], testo[2]"""
    oggetto: "Espressione"
    indice: "Espressione"
    riga: int

@dataclass
class NodoAssegnaIndice:
    """Assegnazione per indice: lista[0] = valore"""
    oggetto: str
    indice: "Espressione"
    valore: "Espressione"
    riga: int

@dataclass
class NodoArgomentoNominato:
    """Argomento nominato in una chiamata: nome: valore"""
    nome: str
    valore: "Espressione"
    riga: int

@dataclass
class NodoPrograma:
    """Radice dell'AST: l'intero programma"""
    istruzioni: list["Istruzione"]

# Alias di tipo
Espressione = (
    NodoNumero | NodoStringa | NodoBooleano | NodoNulla |
    NodoIdentificatore | NodoBinario | NodoUnario |
    NodoChiamata | NodoAccesso | NodoChiamataMetodo | NodoLista
)
Istruzione = (
    NodoAssegnazione | NodoSe | NodoFinche | NodoPerOgni |
    NodoFunzione | NodoRestituisci | NodoClasse |
    NodoScrivi | NodoLeggi | Espressione
)


# ─────────────────────────────────────────────
#  Eccezione del Parser
# ─────────────────────────────────────────────

class ErroreSintattico(Exception):
    def __init__(self, messaggio: str, riga: int):
        super().__init__(f"[Riga {riga}] Errore sintattico: {messaggio}")
        self.riga = riga


# ─────────────────────────────────────────────
#  Parser principale
# ─────────────────────────────────────────────

class Parser:
    """
    Recursive descent parser per Alba.
    Consuma la lista di token e produce un NodoPrograma.
    """

    def __init__(self, tokens: list[Token]):
        # Filtra NEWLINE ridondanti consecutivi
        self.tokens = [t for t in tokens if t.tipo != TipoToken.NEWLINE or self._newline_utile(tokens, tokens.index(t))]
        self.pos = 0

    @staticmethod
    def _newline_utile(tokens, i):
        """Mantieni solo i NEWLINE che precedono contenuto reale."""
        return True  # li gestiamo nel parser

    # ── Navigazione ───────────────────────────

    def _corrente(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]

    def _guarda(self, offset=1) -> Token:
        i = self.pos + offset
        return self.tokens[i] if i < len(self.tokens) else self.tokens[-1]

    def _consuma(self, tipo: TipoToken = None) -> Token:
        tok = self._corrente()
        if tipo and tok.tipo != tipo:
            raise ErroreSintattico(
                f"Atteso {tipo.name}, trovato {tok.tipo.name} ({tok.valore!r})",
                tok.riga
            )
        self.pos += 1
        return tok

    def _controlla(self, *tipi: TipoToken) -> bool:
        return self._corrente().tipo in tipi

    def _salta_newline(self):
        while self._controlla(TipoToken.NEWLINE):
            self._consuma()

    # ── Punto d'ingresso ──────────────────────

    def analizza(self) -> NodoPrograma:
        istruzioni = []
        self._salta_newline()
        while not self._controlla(TipoToken.FINE):
            istruzioni.append(self._istruzione())
            self._salta_newline()
        return NodoPrograma(istruzioni)

    # ── Istruzioni ────────────────────────────

    def _istruzione(self) -> Istruzione:
        tok = self._corrente()

        if tok.tipo == TipoToken.FUNZIONE:
            return self._funzione()
        if tok.tipo == TipoToken.CLASSE:
            return self._classe()
        if tok.tipo == TipoToken.SE:
            return self._se()
        if tok.tipo == TipoToken.FINCHE:
            return self._finche()
        if tok.tipo == TipoToken.PER_OGNI:
            return self._per_ogni()
        if tok.tipo == TipoToken.RESTITUISCI:
            return self._restituisci()
        if tok.tipo == TipoToken.INTERROMPI:
            riga = self._corrente().riga
            self._consuma(TipoToken.INTERROMPI)
            self._salta_newline()
            return NodoInterrompi(riga)
        if tok.tipo == TipoToken.CONTINUA:
            riga = self._corrente().riga
            self._consuma(TipoToken.CONTINUA)
            self._salta_newline()
            return NodoContinua(riga)
        if tok.tipo == TipoToken.PROVA:
            return self._prova_cattura()
        if tok.tipo == TipoToken.IMPORTA:
            riga = self._corrente().riga
            self._consuma(TipoToken.IMPORTA)
            percorso = self._consuma(TipoToken.STRINGA).valore
            self._salta_newline()
            return NodoImporta(percorso, riga)
        if tok.tipo == TipoToken.SCRIVI:
            return self._scrivi()
        if tok.tipo == TipoToken.LEGGI:
            return self._leggi()

        # Assegnazione o espressione
        return self._assegnazione_o_espressione()

    def _assegnazione_o_espressione(self) -> Istruzione:
        """Distingue  x = expr,  x += expr,  x[i] = expr  da una semplice espressione."""
        ASSEGNA_COMPOSTA = {
            TipoToken.PIU_UGUALE:  "+",
            TipoToken.MENO_UGUALE: "-",
            TipoToken.STAR_UGUALE: "*",
            TipoToken.SLASH_UGUALE:"/",
        }
        if self._controlla(TipoToken.IDENTIF):
            prossimo = self._guarda().tipo
            # x = expr
            if prossimo == TipoToken.ASSEGNA:
                nome = self._consuma(TipoToken.IDENTIF)
                self._consuma(TipoToken.ASSEGNA)
                valore = self._espressione()
                self._salta_newline()
                return NodoAssegnazione(nome.valore, valore, nome.riga)
            # x += expr  →  x = x + expr
            if prossimo in ASSEGNA_COMPOSTA:
                nome = self._consuma(TipoToken.IDENTIF)
                op_tok = self._consuma()
                op = ASSEGNA_COMPOSTA[op_tok.tipo]
                valore = self._espressione()
                self._salta_newline()
                sx = NodoIdentificatore(nome.valore, nome.riga)
                espansione = NodoBinario(op, sx, valore, nome.riga)
                return NodoAssegnazione(nome.valore, espansione, nome.riga)
            # lista[i] = valore
            if prossimo == TipoToken.QUADRA_AP:
                nome = self._consuma(TipoToken.IDENTIF)
                self._consuma(TipoToken.QUADRA_AP)
                indice = self._espressione()
                self._consuma(TipoToken.QUADRA_CH)
                if self._controlla(TipoToken.ASSEGNA):
                    riga = nome.riga
                    self._consuma(TipoToken.ASSEGNA)
                    valore = self._espressione()
                    self._salta_newline()
                    return NodoAssegnaIndice(nome.valore, indice, valore, riga)
                nodo = NodoIndice(NodoIdentificatore(nome.valore, nome.riga), indice, nome.riga)
                return self._suffisso(nodo)
        return self._espressione()

    # ── Blocco indentato ──────────────────────

    def _blocco(self) -> list[Istruzione]:
        """Legge un blocco INDENT … DEDENT."""
        self._salta_newline()
        self._consuma(TipoToken.INDENT)
        istruzioni = []
        self._salta_newline()
        while not self._controlla(TipoToken.DEDENT, TipoToken.FINE):
            istruzioni.append(self._istruzione())
            self._salta_newline()
        self._consuma(TipoToken.DEDENT)
        return istruzioni

    # ── Strutture di controllo ────────────────

    def _se(self) -> NodoSe:
        riga = self._corrente().riga
        self._consuma(TipoToken.SE)
        condizione = self._espressione()
        corpo = self._blocco()
        altrimenti = []
        self._salta_newline()
        if self._controlla(TipoToken.ALTRIMENTI):
            self._consuma(TipoToken.ALTRIMENTI)
            altrimenti = self._blocco()
        return NodoSe(condizione, corpo, altrimenti, riga)

    def _finche(self) -> NodoFinche:
        riga = self._corrente().riga
        self._consuma(TipoToken.FINCHE)
        condizione = self._espressione()
        corpo = self._blocco()
        return NodoFinche(condizione, corpo, riga)

    def _per_ogni(self) -> NodoPerOgni:
        riga = self._corrente().riga
        self._consuma(TipoToken.PER_OGNI)
        variabile = self._consuma(TipoToken.IDENTIF).valore
        self._consuma(TipoToken.IN)
        iterabile = self._espressione()
        corpo = self._blocco()
        return NodoPerOgni(variabile, iterabile, corpo, riga)

    # ── Funzioni e classi ─────────────────────

    def _funzione(self) -> NodoFunzione:
        riga = self._corrente().riga
        self._consuma(TipoToken.FUNZIONE)
        nome = self._consuma(TipoToken.IDENTIF).valore
        self._consuma(TipoToken.APERTA)
        parametri = self._parametri()
        self._consuma(TipoToken.CHIUSA)
        tipo_ritorno = None
        if self._controlla(TipoToken.FRECCIA):
            self._consuma(TipoToken.FRECCIA)
            tipo_ritorno = self._consuma().valore
        corpo = self._blocco()
        return NodoFunzione(nome, parametri, tipo_ritorno, corpo, riga)

    def _parametri(self) -> list[tuple[str, Optional[str]]]:
        params = []
        while not self._controlla(TipoToken.CHIUSA):
            nome = self._consuma(TipoToken.IDENTIF).valore
            tipo = None
            default = None
            if self._controlla(TipoToken.DUE_PUNTI):
                self._consuma(TipoToken.DUE_PUNTI)
                tipo = self._consuma().valore
            if self._controlla(TipoToken.ASSEGNA):
                self._consuma(TipoToken.ASSEGNA)
                default = self._espressione()
            params.append((nome, tipo, default))
            if self._controlla(TipoToken.VIRGOLA):
                self._consuma(TipoToken.VIRGOLA)
        return params

    def _classe(self) -> NodoClasse:
        riga = self._corrente().riga
        self._consuma(TipoToken.CLASSE)
        nome = self._consuma(TipoToken.IDENTIF).valore
        # Genitore opzionale: classe Cane(Animale)
        genitore = None
        if self._controlla(TipoToken.APERTA):
            self._consuma(TipoToken.APERTA)
            genitore = self._consuma(TipoToken.IDENTIF).valore
            self._consuma(TipoToken.CHIUSA)
        self._salta_newline()
        self._consuma(TipoToken.INDENT)
        attributi = []
        metodi = []
        self._salta_newline()
        while not self._controlla(TipoToken.DEDENT, TipoToken.FINE):
            if self._controlla(TipoToken.FUNZIONE):
                metodi.append(self._funzione())
            else:
                n = self._consuma(TipoToken.IDENTIF).valore
                self._consuma(TipoToken.DUE_PUNTI)
                t = self._consuma().valore
                attributi.append((n, t))
            self._salta_newline()
        self._consuma(TipoToken.DEDENT)
        return NodoClasse(nome, genitore, attributi, metodi, riga)

    def _prova_cattura(self) -> NodoProvaCattura:
        riga = self._corrente().riga
        self._consuma(TipoToken.PROVA)
        corpo = self._blocco()
        self._salta_newline()
        self._consuma(TipoToken.CATTURA)
        var_errore = None
        # Accetta IDENTIF o keyword monosillaba come "e" come nome variabile
        if not self._controlla(TipoToken.NEWLINE, TipoToken.INDENT, TipoToken.FINE):
            tok = self._consuma()
            var_errore = tok.valore
        cattura = self._blocco()
        return NodoProvaCattura(corpo, var_errore, cattura, riga)

    def _restituisci(self) -> NodoRestituisci:
        riga = self._corrente().riga
        self._consuma(TipoToken.RESTITUISCI)
        valore = None
        if not self._controlla(TipoToken.NEWLINE, TipoToken.DEDENT, TipoToken.FINE):
            valore = self._espressione()
        self._salta_newline()
        return NodoRestituisci(valore, riga)

    def _scrivi(self) -> NodoScrivi:
        riga = self._corrente().riga
        self._consuma(TipoToken.SCRIVI)
        self._consuma(TipoToken.APERTA)
        valore = self._espressione()
        self._consuma(TipoToken.CHIUSA)
        self._salta_newline()
        return NodoScrivi(valore, riga)

    def _leggi(self) -> NodoLeggi:
        riga = self._corrente().riga
        self._consuma(TipoToken.LEGGI)
        self._consuma(TipoToken.APERTA)
        prompt = None
        if not self._controlla(TipoToken.CHIUSA):
            prompt = self._espressione()
        self._consuma(TipoToken.CHIUSA)
        self._salta_newline()
        return NodoLeggi(prompt, riga)

    # ── Espressioni (precedenza crescente) ────

    def _espressione(self) -> Espressione:
        return self._logico_o()

    def _logico_o(self) -> Espressione:
        sx = self._logico_e()
        while self._controlla(TipoToken.O):
            op = self._consuma().valore
            dx = self._logico_e()
            sx = NodoBinario(op, sx, dx, sx.riga)
        return sx

    def _logico_e(self) -> Espressione:
        sx = self._logico_non()
        while self._controlla(TipoToken.E):
            op = self._consuma().valore
            dx = self._logico_non()
            sx = NodoBinario(op, sx, dx, sx.riga)
        return sx

    def _logico_non(self) -> Espressione:
        if self._controlla(TipoToken.NON):
            riga = self._corrente().riga
            op = self._consuma().valore
            operando = self._logico_non()
            return NodoUnario(op, operando, riga)
        return self._confronto()

    def _confronto(self) -> Espressione:
        sx = self._addizione()
        CONFRONTI = {
            TipoToken.UGUALE, TipoToken.DIVERSO,
            TipoToken.MINORE, TipoToken.MAGGIORE,
            TipoToken.MIN_UGUALE, TipoToken.MAG_UGUALE,
        }
        while self._corrente().tipo in CONFRONTI or self._controlla(TipoToken.IN):
            op = self._consuma().valore
            dx = self._addizione()
            sx = NodoBinario(op, sx, dx, sx.riga)
        return sx

    def _addizione(self) -> Espressione:
        sx = self._moltiplicazione()
        while self._controlla(TipoToken.PIU, TipoToken.MENO):
            op = self._consuma().valore
            dx = self._moltiplicazione()
            sx = NodoBinario(op, sx, dx, sx.riga)
        return sx

    def _moltiplicazione(self) -> Espressione:
        sx = self._primario()
        while self._controlla(TipoToken.STAR, TipoToken.SLASH, TipoToken.PERCENTO):
            op = self._consuma().valore
            dx = self._primario()
            sx = NodoBinario(op, sx, dx, sx.riga)
        return sx

    def _primario(self) -> Espressione:
        tok = self._corrente()

        if tok.tipo == TipoToken.NUMERO:
            self._consuma()
            v = float(tok.valore)
            nodo = NodoNumero(int(v) if v == int(v) else v, tok.riga)
            return self._suffisso(nodo)

        if tok.tipo == TipoToken.STRINGA:
            self._consuma()
            return self._suffisso(NodoStringa(tok.valore, tok.riga))

        if tok.tipo == TipoToken.VERO:
            self._consuma()
            return NodoBooleano(True, tok.riga)

        if tok.tipo == TipoToken.FALSO:
            self._consuma()
            return NodoBooleano(False, tok.riga)

        if tok.tipo == TipoToken.NULLA:
            self._consuma()
            return NodoNulla(tok.riga)

        if tok.tipo == TipoToken.IDENTIF:
            self._consuma()
            if self._controlla(TipoToken.APERTA):
                # Chiamata funzione
                self._consuma(TipoToken.APERTA)
                args = self._argomenti()
                self._consuma(TipoToken.CHIUSA)
                nodo = NodoChiamata(tok.valore, args, tok.riga)
            else:
                nodo = NodoIdentificatore(tok.valore, tok.riga)
            return self._suffisso(nodo)

        if tok.tipo == TipoToken.QUADRA_AP:
            return self._lista()

        if tok.tipo == TipoToken.GRAFFA_AP:
            return self._dizionario()

        if tok.tipo == TipoToken.APERTA:
            self._consuma(TipoToken.APERTA)
            expr = self._espressione()
            self._consuma(TipoToken.CHIUSA)
            return expr

        if tok.tipo == TipoToken.MENO:
            riga = tok.riga
            self._consuma()
            operando = self._primario()
            return NodoUnario("-", operando, riga)

        raise ErroreSintattico(
            f"Espressione attesa, trovato {tok.tipo.name} ({tok.valore!r})",
            tok.riga
        )

    def _suffisso(self, nodo: Espressione) -> Espressione:
        """Gestisce accesso attributo (.), chiamata metodo e indice [i]."""
        while self._controlla(TipoToken.PUNTO, TipoToken.QUADRA_AP):
            if self._controlla(TipoToken.PUNTO):
                self._consuma(TipoToken.PUNTO)
                attr = self._consuma(TipoToken.IDENTIF)
                if self._controlla(TipoToken.APERTA):
                    self._consuma(TipoToken.APERTA)
                    args = self._argomenti()
                    self._consuma(TipoToken.CHIUSA)
                    nodo = NodoChiamataMetodo(nodo, attr.valore, args, attr.riga)
                else:
                    nodo = NodoAccesso(nodo, attr.valore, attr.riga)
            elif self._controlla(TipoToken.QUADRA_AP):
                riga = self._corrente().riga
                self._consuma(TipoToken.QUADRA_AP)
                indice = self._espressione()
                self._consuma(TipoToken.QUADRA_CH)
                nodo = NodoIndice(nodo, indice, riga)
        return nodo

    def _argomenti(self) -> list:
        args = []
        while not self._controlla(TipoToken.CHIUSA):
            # Argomento nominato: nome: valore
            if (self._controlla(TipoToken.IDENTIF) and
                    self._guarda().tipo == TipoToken.DUE_PUNTI):
                nome_tok = self._consuma(TipoToken.IDENTIF)
                self._consuma(TipoToken.DUE_PUNTI)
                valore = self._espressione()
                args.append(NodoArgomentoNominato(nome_tok.valore, valore, nome_tok.riga))
            else:
                args.append(self._espressione())
            if self._controlla(TipoToken.VIRGOLA):
                self._consuma(TipoToken.VIRGOLA)
        return args

    def _dizionario(self) -> NodoDizionario:
        riga = self._corrente().riga
        self._consuma(TipoToken.GRAFFA_AP)
        coppie = []
        while not self._controlla(TipoToken.GRAFFA_CH):
            chiave = self._espressione()
            self._consuma(TipoToken.DUE_PUNTI)
            valore = self._espressione()
            coppie.append((chiave, valore))
            if self._controlla(TipoToken.VIRGOLA):
                self._consuma(TipoToken.VIRGOLA)
        self._consuma(TipoToken.GRAFFA_CH)
        return NodoDizionario(coppie, riga)

    def _lista(self) -> NodoLista:
        riga = self._corrente().riga
        self._consuma(TipoToken.QUADRA_AP)
        elementi = []
        while not self._controlla(TipoToken.QUADRA_CH):
            elementi.append(self._espressione())
            if self._controlla(TipoToken.VIRGOLA):
                self._consuma(TipoToken.VIRGOLA)
        self._consuma(TipoToken.QUADRA_CH)
        return NodoLista(elementi, riga)


# ─────────────────────────────────────────────
#  Funzione di utilità
# ─────────────────────────────────────────────

def analizza(sorgente: str) -> NodoPrograma:
    """Scorciatoia: tokenizza e analizza il sorgente."""
    tokens = tokenizza(sorgente)
    return Parser(tokens).analizza()


# ─────────────────────────────────────────────
#  Stampa leggibile dell'AST
# ─────────────────────────────────────────────

def stampa_ast(nodo, indent=0):
    pref = "  " * indent
    nome = type(nodo).__name__

    if isinstance(nodo, NodoPrograma):
        print(f"{pref}Programma")
        for i in nodo.istruzioni:
            stampa_ast(i, indent + 1)

    elif isinstance(nodo, NodoFunzione):
        params = ", ".join(f"{n}:{t}" if t else n for n, t in nodo.parametri)
        ritorno = f" -> {nodo.tipo_ritorno}" if nodo.tipo_ritorno else ""
        print(f"{pref}Funzione {nodo.nome}({params}){ritorno}")
        for i in nodo.corpo:
            stampa_ast(i, indent + 1)

    elif isinstance(nodo, NodoClasse):
        print(f"{pref}Classe {nodo.nome}")
        for n, t in nodo.attributi:
            print(f"{pref}  Attributo {n}: {t}")
        for m in nodo.metodi:
            stampa_ast(m, indent + 1)

    elif isinstance(nodo, NodoSe):
        print(f"{pref}Se")
        print(f"{pref}  condizione:")
        stampa_ast(nodo.condizione, indent + 2)
        print(f"{pref}  corpo:")
        for i in nodo.corpo:
            stampa_ast(i, indent + 2)
        if nodo.altrimenti:
            print(f"{pref}  altrimenti:")
            for i in nodo.altrimenti:
                stampa_ast(i, indent + 2)

    elif isinstance(nodo, NodoPerOgni):
        print(f"{pref}PerOgni {nodo.variabile} in:")
        stampa_ast(nodo.iterabile, indent + 2)
        for i in nodo.corpo:
            stampa_ast(i, indent + 1)

    elif isinstance(nodo, NodoFinche):
        print(f"{pref}Finché")
        stampa_ast(nodo.condizione, indent + 1)
        for i in nodo.corpo:
            stampa_ast(i, indent + 1)

    elif isinstance(nodo, NodoAssegnazione):
        print(f"{pref}Assegna {nodo.nome} =")
        stampa_ast(nodo.valore, indent + 1)

    elif isinstance(nodo, NodoBinario):
        print(f"{pref}Binario '{nodo.operatore}'")
        stampa_ast(nodo.sinistra, indent + 1)
        stampa_ast(nodo.destra, indent + 1)

    elif isinstance(nodo, NodoUnario):
        print(f"{pref}Unario '{nodo.operatore}'")
        stampa_ast(nodo.operando, indent + 1)

    elif isinstance(nodo, NodoChiamata):
        print(f"{pref}Chiamata {nodo.nome}()")
        for a in nodo.argomenti:
            stampa_ast(a, indent + 1)

    elif isinstance(nodo, NodoChiamataMetodo):
        print(f"{pref}ChiamataMetodo .{nodo.metodo}()")
        stampa_ast(nodo.oggetto, indent + 1)
        for a in nodo.argomenti:
            stampa_ast(a, indent + 1)

    elif isinstance(nodo, NodoScrivi):
        print(f"{pref}Scrivi")
        stampa_ast(nodo.valore, indent + 1)

    elif isinstance(nodo, NodoRestituisci):
        print(f"{pref}Restituisci")
        if nodo.valore:
            stampa_ast(nodo.valore, indent + 1)

    elif isinstance(nodo, NodoLista):
        print(f"{pref}Lista[{len(nodo.elementi)}]")
        for e in nodo.elementi:
            stampa_ast(e, indent + 1)

    elif isinstance(nodo, NodoNumero):
        print(f"{pref}Numero({nodo.valore})")

    elif isinstance(nodo, NodoStringa):
        print(f"{pref}Stringa({nodo.valore!r})")

    elif isinstance(nodo, NodoBooleano):
        print(f"{pref}Booleano({nodo.valore})")

    elif isinstance(nodo, NodoNulla):
        print(f"{pref}Nulla")

    elif isinstance(nodo, NodoIdentificatore):
        print(f"{pref}Identif({nodo.nome})")

    else:
        print(f"{pref}{nome}")


# ─────────────────────────────────────────────
#  Demo
# ─────────────────────────────────────────────

if __name__ == "__main__":
    codice = """\
funzione fattoriale(n: numero) -> numero
    se n <= 1
        restituisci 1
    altrimenti
        restituisci n * fattoriale(n - 1)

risultato = fattoriale(5)
scrivi("5! = " + risultato)

numeri = [1, 2, 3, 4, 5]
per ogni n in numeri
    se n % 2 == 0
        scrivi(n + " è pari")
    altrimenti
        scrivi(n + " è dispari")
"""

    print("═" * 50)
    print("  Alba Parser — Albero Sintattico (AST)")
    print("═" * 50)

    try:
        ast = analizza(codice)
        stampa_ast(ast)
        print("\n✓ Analisi completata con successo")
    except Exception as e:
        print(f"\n✗ {e}")
