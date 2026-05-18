"""
Alba Interpreter — esegue l'AST prodotto dal Parser.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional
from alba_parser import (
    analizza,
    NodoPrograma, NodoNumero, NodoStringa, NodoBooleano, NodoNulla,
    NodoIdentificatore, NodoAssegnazione, NodoBinario, NodoUnario,
    NodoChiamata, NodoChiamataMetodo, NodoAccesso, NodoLista, NodoDizionario,
    NodoIndice, NodoAssegnaIndice,
    NodoSe, NodoFinche, NodoPerOgni,
    NodoFunzione, NodoRestituisci, NodoInterrompi, NodoContinua,
    NodoProvaCattura, NodoClasse, NodoScrivi, NodoLeggi,
    NodoArgomentoNominato, NodoImporta,
)


# ─────────────────────────────────────────────
#  Segnali di controllo del flusso
# ─────────────────────────────────────────────

class _SegnaleRestituisci(Exception):
    def __init__(self, valore):
        self.valore = valore

class _SegnaleInterrompi(Exception):
    pass

class _SegnaleContinua(Exception):
    pass


# ─────────────────────────────────────────────
#  Ambiente (scope delle variabili)
# ─────────────────────────────────────────────

class Ambiente:
    """
    Dizionario di variabili con supporto per scope annidati.
    Ogni blocco (funzione, if, ciclo) crea un figlio del padre.
    """
    def __init__(self, padre: Optional[Ambiente] = None):
        self._vars: dict[str, Any] = {}
        self.padre = padre

    def leggi(self, nome: str, riga: int) -> Any:
        if nome in self._vars:
            return self._vars[nome]
        if self.padre:
            return self.padre.leggi(nome, riga)
        raise ErroreEsecuzione(f"Variabile '{nome}' non definita", riga)

    def scrivi(self, nome: str, valore: Any):
        """Assegna nel primo scope che contiene il nome, o in quello corrente."""
        if nome in self._vars:
            self._vars[nome] = valore
        elif self.padre and self.padre._contiene(nome):
            self.padre.scrivi(nome, valore)
        else:
            self._vars[nome] = valore

    def _contiene(self, nome: str) -> bool:
        if nome in self._vars:
            return True
        return self.padre._contiene(nome) if self.padre else False

    def definisci(self, nome: str, valore: Any):
        """Sempre nel scope corrente."""
        self._vars[nome] = valore


# ─────────────────────────────────────────────
#  Oggetti Alba
# ─────────────────────────────────────────────

class FunzioneAlba:
    """Funzione definita dall'utente in Alba."""
    def __init__(self, nodo: NodoFunzione, ambiente: Ambiente):
        self.nodo = nodo
        self.ambiente_chiusura = ambiente   # closure

    def __repr__(self):
        return f"<funzione {self.nodo.nome}>"


class ClasseAlba:
    """Definizione di una classe Alba."""
    def __init__(self, nodo: NodoClasse, ambiente: Ambiente, genitore=None):
        self.nodo = nodo
        self.ambiente = ambiente
        self.genitore = genitore   # ClasseAlba genitore o None

    def __repr__(self):
        return f"<classe {self.nodo.nome}>"


class IstanzaAlba:
    """Istanza di una classe Alba."""
    def __init__(self, classe: ClasseAlba):
        self.classe = classe
        self.attributi: dict[str, Any] = {}

    def __repr__(self):
        return f"<{self.classe.nodo.nome}>"


# ─────────────────────────────────────────────
#  Eccezione dell'Interpreter
# ─────────────────────────────────────────────

class ErroreEsecuzione(Exception):
    def __init__(self, messaggio: str, riga: int = 0):
        super().__init__(f"[Riga {riga}] Errore di esecuzione: {messaggio}")
        self.riga = riga


# ─────────────────────────────────────────────
#  Interpreter principale
# ─────────────────────────────────────────────

class Interpreter:
    """
    Visita i nodi dell'AST e li esegue.
    Mantiene un ambiente globale e gestisce gli scope annidati.
    """

    def __init__(self, output_fn=print):
        self.globale = Ambiente()
        self._output = output_fn
        self._moduli_caricati: set = set()
        self._profondita_chiamata = 0
        self._MAX_RICORSIONE = 500
        self._registra_builtin()

    # ── Funzioni built-in ─────────────────────

    def _registra_builtin(self):
        """Funzioni native disponibili in ogni programma Alba."""

        def lunghezza(args, riga):
            if len(args) != 1:
                raise ErroreEsecuzione("lunghezza() vuole 1 argomento", riga)
            v = args[0]
            if isinstance(v, (str, list)):
                return len(v)
            raise ErroreEsecuzione("lunghezza() si applica a testo o lista", riga)

        def tipo(args, riga):
            if len(args) != 1:
                raise ErroreEsecuzione("tipo() vuole 1 argomento", riga)
            v = args[0]
            if isinstance(v, bool):   return "booleano"
            if isinstance(v, (int, float)): return "numero"
            if isinstance(v, str):    return "testo"
            if isinstance(v, list):   return "lista"
            if v is None:             return "nulla"
            if isinstance(v, IstanzaAlba): return v.classe.nodo.nome
            return "sconosciuto"

        def a_numero(args, riga):
            if len(args) != 1:
                raise ErroreEsecuzione("a_numero() vuole 1 argomento", riga)
            try:
                v = args[0]
                return int(v) if isinstance(v, str) and "." not in v else float(v)
            except (ValueError, TypeError):
                raise ErroreEsecuzione(f"Impossibile convertire '{args[0]}' in numero", riga)

        def a_testo(args, riga):
            if len(args) != 1:
                raise ErroreEsecuzione("a_testo() vuole 1 argomento", riga)
            return self._a_testo(args[0])

        def aggiungi(args, riga):
            if len(args) != 2 or not isinstance(args[0], list):
                raise ErroreEsecuzione("aggiungi(lista, elemento) vuole lista e valore", riga)
            args[0].append(args[1])
            return args[0]

        def rimuovi(args, riga):
            if len(args) != 2 or not isinstance(args[0], list):
                raise ErroreEsecuzione("rimuovi(lista, indice) vuole lista e indice", riga)
            try:
                return args[0].pop(int(args[1]))
            except IndexError:
                raise ErroreEsecuzione("Indice fuori dalla lista", riga)

        def intervallo(args, riga):
            if not (1 <= len(args) <= 3):
                raise ErroreEsecuzione("intervallo() vuole 1-3 argomenti", riga)
            try:
                return list(range(*[int(a) for a in args]))
            except TypeError:
                raise ErroreEsecuzione("intervallo() vuole argomenti numerici", riga)

        BUILTIN = {
            "lunghezza": lunghezza,
            "tipo": tipo,
            "a_numero": a_numero,
            "a_testo": a_testo,
            "aggiungi": aggiungi,
            "rimuovi": rimuovi,
            "intervallo": intervallo,
        }
        for nome, fn in BUILTIN.items():
            self.globale.definisci(nome, fn)

    # ── Punto d'ingresso ──────────────────────

    def esegui(self, sorgente: str) -> Any:
        ast = analizza(sorgente)
        return self._esegui_programma(ast, self.globale)

    def _esegui_programma(self, nodo: NodoPrograma, amb: Ambiente) -> Any:
        risultato = None
        for istr in nodo.istruzioni:
            risultato = self._valuta(istr, amb)
        return risultato

    # ── Dispatcher ────────────────────────────

    def _valuta(self, nodo, amb: Ambiente) -> Any:
        tipo = type(nodo)

        if tipo == NodoNumero:      return nodo.valore
        if tipo == NodoStringa:     return nodo.valore
        if tipo == NodoBooleano:    return nodo.valore
        if tipo == NodoNulla:       return None

        if tipo == NodoIdentificatore:
            return amb.leggi(nodo.nome, nodo.riga)

        if tipo == NodoAssegnazione:
            v = self._valuta(nodo.valore, amb)
            amb.scrivi(nodo.nome, v)
            return v

        if tipo == NodoBinario:     return self._binario(nodo, amb)
        if tipo == NodoUnario:      return self._unario(nodo, amb)
        if tipo == NodoLista:
            return [self._valuta(e, amb) for e in nodo.elementi]

        if tipo == NodoImporta:
            import os
            percorso = nodo.percorso
            if not percorso.endswith(".alba"):
                percorso += ".alba"
            # Cerca prima nella stessa cartella del file corrente, poi nella cwd
            if not os.path.isabs(percorso):
                percorso = os.path.join(os.getcwd(), percorso)
            if percorso in self._moduli_caricati:
                return None   # evita importazioni circolari
            if not os.path.exists(percorso):
                raise ErroreEsecuzione(f"Modulo '{nodo.percorso}' non trovato", nodo.riga)
            self._moduli_caricati.add(percorso)
            with open(percorso, encoding="utf-8") as f:
                sorgente = f.read()
            ast = analizza(sorgente)
            self._esegui_programma(ast, self.globale)
            return None

        if tipo == NodoDizionario:
            return {self._valuta(k, amb): self._valuta(v, amb) for k, v in nodo.coppie}

        if tipo == NodoIndice:
            obj = self._valuta(nodo.oggetto, amb)
            idx = self._valuta(nodo.indice, amb)
            if isinstance(obj, dict):
                if idx not in obj:
                    raise ErroreEsecuzione(f"Chiave '{idx}' non trovata nel dizionario", nodo.riga)
                return obj[idx]
            if not isinstance(idx, (int, float)):
                raise ErroreEsecuzione("L'indice deve essere un numero", nodo.riga)
            idx = int(idx)
            if isinstance(obj, (list, str)):
                # Supporto indici negativi
                if idx < 0:
                    idx = len(obj) + idx
                if idx < 0 or idx >= len(obj):
                    raise ErroreEsecuzione(f"Indice fuori dalla lista (lunghezza {len(obj)})", nodo.riga)
                return obj[idx]
            raise ErroreEsecuzione("Gli indici si usano solo su liste, dizionari e testo", nodo.riga)

        if tipo == NodoAssegnaIndice:
            obj = amb.leggi(nodo.oggetto, nodo.riga)
            idx = self._valuta(nodo.indice, amb)
            val = self._valuta(nodo.valore, amb)
            if isinstance(obj, dict):
                obj[idx] = val
                return val
            idx = int(idx)
            if not isinstance(obj, list):
                raise ErroreEsecuzione("Puoi assegnare per indice solo su una lista o dizionario", nodo.riga)
            if idx < 0 or idx >= len(obj):
                raise ErroreEsecuzione(f"Indice {idx} fuori dalla lista (lunghezza {len(obj)})", nodo.riga)
            obj[idx] = val
            return val

        if tipo == NodoChiamata:    return self._chiama(nodo, amb)
        if tipo == NodoChiamataMetodo: return self._chiama_metodo(nodo, amb)
        if tipo == NodoAccesso:     return self._accesso(nodo, amb)

        if tipo == NodoSe:          return self._se(nodo, amb)
        if tipo == NodoFinche:      return self._finche(nodo, amb)
        if tipo == NodoPerOgni:     return self._per_ogni(nodo, amb)

        if tipo == NodoFunzione:
            fn = FunzioneAlba(nodo, amb)
            amb.definisci(nodo.nome, fn)
            return fn

        if tipo == NodoClasse:
            genitore = None
            if nodo.genitore:
                genitore = amb.leggi(nodo.genitore, nodo.riga)
                if not isinstance(genitore, ClasseAlba):
                    raise ErroreEsecuzione(f"'{nodo.genitore}' non è una classe", nodo.riga)
            cls = ClasseAlba(nodo, amb, genitore)
            amb.definisci(nodo.nome, cls)
            return cls

        if tipo == NodoRestituisci:
            v = self._valuta(nodo.valore, amb) if nodo.valore else None
            raise _SegnaleRestituisci(v)

        if tipo == NodoProvaCattura:
            try:
                for i in nodo.corpo:
                    self._valuta(i, amb)
            except (_SegnaleRestituisci, _SegnaleInterrompi, _SegnaleContinua):
                raise
            except Exception as e:
                scope = Ambiente(amb)
                msg = str(e).split("Errore di esecuzione: ")[-1] if "Errore di esecuzione" in str(e) else str(e)
                if nodo.var_errore:
                    scope.definisci(nodo.var_errore, msg)
                for i in nodo.cattura:
                    self._valuta(i, scope)
            return None

        if tipo == NodoInterrompi:
            raise _SegnaleInterrompi()

        if tipo == NodoContinua:
            raise _SegnaleContinua()

        if tipo == NodoScrivi:
            v = self._valuta(nodo.valore, amb)
            self._output(self._a_testo(v))
            return None

        if tipo == NodoLeggi:
            prompt = ""
            if nodo.prompt:
                prompt = self._a_testo(self._valuta(nodo.prompt, amb))
            return input(prompt)

        raise ErroreEsecuzione(f"Nodo sconosciuto: {tipo.__name__}", 0)

    # ── Operatori ─────────────────────────────

    def _binario(self, nodo: NodoBinario, amb: Ambiente) -> Any:
        sx = self._valuta(nodo.sinistra, amb)
        dx = self._valuta(nodo.destra, amb)
        op = nodo.operatore
        riga = nodo.riga

        try:
            if op == "+":
                if isinstance(sx, list) and isinstance(dx, list):
                    return sx + dx
                if isinstance(sx, str) or isinstance(dx, str):
                    return self._a_testo(sx) + self._a_testo(dx)
                return sx + dx
            if op == "-":  return sx - dx
            if op == "*":  return sx * dx
            if op == "/":
                if dx == 0:
                    raise ErroreEsecuzione("Divisione per zero", riga)
                return sx / dx
            if op == "%":  return sx % dx
            if op == "==": return sx == dx
            if op == "!=": return sx != dx
            if op == "<":  return sx < dx
            if op == ">":  return sx > dx
            if op == "<=": return sx <= dx
            if op == ">=": return sx >= dx
            if op == "in":
                if isinstance(dx, (list, str, dict)):
                    return sx in dx
                raise ErroreEsecuzione("'in' si applica a liste, testo e dizionari", riga)
            if op == "e":  return bool(sx) and bool(dx)
            if op == "o":  return bool(sx) or bool(dx)
        except TypeError as e:
            raise ErroreEsecuzione(f"Operazione '{op}' non valida tra questi tipi", riga)

        raise ErroreEsecuzione(f"Operatore sconosciuto: {op}", riga)

    def _unario(self, nodo: NodoUnario, amb: Ambiente) -> Any:
        v = self._valuta(nodo.operando, amb)
        if nodo.operatore == "-":
            return -v
        if nodo.operatore == "non":
            return not v
        raise ErroreEsecuzione(f"Operatore unario sconosciuto: {nodo.operatore}", nodo.riga)

    # ── Strutture di controllo ────────────────

    def _se(self, nodo: NodoSe, amb: Ambiente) -> Any:
        if self._valuta(nodo.condizione, amb):
            scope = Ambiente(amb)
            for i in nodo.corpo:
                self._valuta(i, scope)
        elif nodo.altrimenti:
            scope = Ambiente(amb)
            for i in nodo.altrimenti:
                self._valuta(i, scope)
        return None

    def _finche(self, nodo: NodoFinche, amb: Ambiente) -> Any:
        while self._valuta(nodo.condizione, amb):
            scope = Ambiente(amb)
            try:
                for i in nodo.corpo:
                    self._valuta(i, scope)
            except _SegnaleInterrompi:
                break
            except _SegnaleContinua:
                continue
        return None

    def _per_ogni(self, nodo: NodoPerOgni, amb: Ambiente) -> Any:
        iterabile = self._valuta(nodo.iterabile, amb)
        if not isinstance(iterabile, list):
            raise ErroreEsecuzione("'per ogni' si applica a una lista", nodo.riga)
        for elemento in iterabile:
            scope = Ambiente(amb)
            scope.definisci(nodo.variabile, elemento)
            try:
                for i in nodo.corpo:
                    self._valuta(i, scope)
            except _SegnaleInterrompi:
                break
            except _SegnaleContinua:
                continue
        return None

    # ── Chiamate ──────────────────────────────

    def _chiama(self, nodo: NodoChiamata, amb: Ambiente) -> Any:
        fn = amb.leggi(nodo.nome, nodo.riga)
        args = []
        for a in nodo.argomenti:
            if isinstance(a, NodoArgomentoNominato):
                args.append((a.nome, self._valuta(a.valore, amb)))
            else:
                args.append(self._valuta(a, amb))

        # Funzione built-in (callable Python)
        if callable(fn) and not isinstance(fn, FunzioneAlba):
            return fn(args, nodo.riga)

        # Classe → costruisce istanza
        if isinstance(fn, ClasseAlba):
            return self._costruisci(fn, args, nodo.riga)

        # Funzione Alba
        if isinstance(fn, FunzioneAlba):
            return self._esegui_funzione(fn, args, nodo.riga)

        raise ErroreEsecuzione(f"'{nodo.nome}' non è una funzione", nodo.riga)

    def _esegui_funzione(self, fn: FunzioneAlba, args: list, riga: int) -> Any:
        self._profondita_chiamata += 1
        if self._profondita_chiamata > self._MAX_RICORSIONE:
            self._profondita_chiamata = 0
            raise ErroreEsecuzione(
                f"Limite di ricorsione raggiunto ({self._MAX_RICORSIONE} chiamate). "
                "Controlla che la funzione abbia un caso base.", riga
            )
        params = fn.nodo.parametri
        # Conta parametri senza default
        obbligatori = sum(1 for _, _, d in params if d is None)
        if len(args) < obbligatori or len(args) > len(params):
            raise ErroreEsecuzione(
                f"'{fn.nodo.nome}' vuole {obbligatori}-{len(params)} argomenti, ricevuti {len(args)}",
                riga
            )
        scope = Ambiente(fn.ambiente_chiusura)
        for i, (nome, _, default) in enumerate(params):
            if i < len(args):
                scope.definisci(nome, args[i])
            else:
                # Valuta il default nell'ambiente della funzione
                scope.definisci(nome, self._valuta(default, fn.ambiente_chiusura))
        try:
            for istr in fn.nodo.corpo:
                self._valuta(istr, scope)
        except _SegnaleRestituisci as r:
            self._profondita_chiamata -= 1
            return r.valore
        self._profondita_chiamata -= 1
        return None

    def _costruisci(self, cls: ClasseAlba, args: list, riga: int) -> IstanzaAlba:
        istanza = IstanzaAlba(cls)
        # Eredita attributi dal genitore (in ordine: genitore prima, figlio dopo)
        for antenato in self._catena_classi(cls):
            for nome, _ in antenato.nodo.attributi:
                if nome not in istanza.attributi:
                    istanza.attributi[nome] = None
        # Argomenti nominati
        for arg in args:
            if isinstance(arg, tuple) and len(arg) == 2:
                nome, valore = arg
                if nome in istanza.attributi:
                    istanza.attributi[nome] = valore
        # Chiama inizializza se esiste (partendo dalla classe figlio)
        args_pos = [a for a in args if not (isinstance(a, tuple) and len(a) == 2)]
        metodo_init = self._trova_metodo(cls, "inizializza")
        if metodo_init:
            fn = FunzioneAlba(metodo_init, metodo_init._cls_amb)
            self._esegui_metodo(fn, istanza, args_pos, riga)
        return istanza

    def _catena_classi(self, cls: ClasseAlba) -> list:
        """Restituisce la catena di classi dal genitore più lontano al figlio."""
        catena = []
        c = cls
        while c:
            catena.append(c)
            c = c.genitore
        return list(reversed(catena))

    def _trova_metodo(self, cls: ClasseAlba, nome: str):
        """Cerca un metodo nella classe e nei suoi antenati."""
        c = cls
        while c:
            for m in c.nodo.metodi:
                if m.nome == nome:
                    m._cls_amb = c.ambiente
                    return m
            c = c.genitore
        return None

    def _esegui_metodo(self, fn: FunzioneAlba, istanza: IstanzaAlba, args: list, riga: int) -> Any:
        scope = Ambiente(fn.ambiente_chiusura)
        scope.definisci("se_stesso", istanza)
        for nome, valore in istanza.attributi.items():
            scope.definisci(nome, valore)
        params = [p for p in fn.nodo.parametri if p[0] != "se_stesso"]
        # Gestisce tuple (nome, tipo) e (nome, tipo, default)
        for i, param in enumerate(params):
            nome = param[0]
            if i < len(args):
                scope.definisci(nome, args[i])
            elif len(param) > 2 and param[2] is not None:
                scope.definisci(nome, self._valuta(param[2], fn.ambiente_chiusura))
        try:
            for istr in fn.nodo.corpo:
                self._valuta(istr, scope)
            for nome in istanza.attributi:
                if nome in scope._vars:
                    istanza.attributi[nome] = scope._vars[nome]
        except _SegnaleRestituisci as r:
            for nome in istanza.attributi:
                if nome in scope._vars:
                    istanza.attributi[nome] = scope._vars[nome]
            return r.valore
        return None

    def _chiama_metodo(self, nodo: NodoChiamataMetodo, amb: Ambiente) -> Any:
        oggetto = self._valuta(nodo.oggetto, amb)
        args = [self._valuta(a, amb) for a in nodo.argomenti]
        riga = nodo.riga

        # Metodi su dizionario
        if isinstance(oggetto, dict):
            return self._metodo_dizionario(oggetto, nodo.metodo, args, nodo.riga)

        # Metodi su lista
        if isinstance(oggetto, list):
            return self._metodo_lista(oggetto, nodo.metodo, args, riga)

        # Metodi su testo
        if isinstance(oggetto, str):
            return self._metodo_testo(oggetto, nodo.metodo, args, riga)

        # Metodi su istanza
        if isinstance(oggetto, IstanzaAlba):
            metodo_nodo = self._trova_metodo(oggetto.classe, nodo.metodo)
            if metodo_nodo:
                fn = FunzioneAlba(metodo_nodo, metodo_nodo._cls_amb)
                return self._esegui_metodo(fn, oggetto, args, riga)
            raise ErroreEsecuzione(
                f"'{oggetto.classe.nodo.nome}' non ha il metodo '{nodo.metodo}'", riga
            )

        raise ErroreEsecuzione(f"Il tipo non supporta metodi", riga)

    def _accesso(self, nodo: NodoAccesso, amb: Ambiente) -> Any:
        oggetto = self._valuta(nodo.oggetto, amb)
        if isinstance(oggetto, IstanzaAlba):
            if nodo.attributo in oggetto.attributi:
                return oggetto.attributi[nodo.attributo]
            raise ErroreEsecuzione(
                f"Attributo '{nodo.attributo}' non trovato", nodo.riga
            )
        raise ErroreEsecuzione("Accesso ad attributo non supportato", nodo.riga)

    # ── Metodi built-in su lista e testo ──────

    def _metodo_dizionario(self, diz, metodo, args, riga):
        if metodo == "chiavi":   return list(diz.keys())
        if metodo == "valori":   return list(diz.values())
        if metodo == "contiene": return args[0] in diz
        if metodo == "rimuovi":
            if args[0] not in diz:
                raise ErroreEsecuzione(f"Chiave '{args[0]}' non trovata", riga)
            return diz.pop(args[0])
        if metodo == "lunghezza": return len(diz)
        raise ErroreEsecuzione(f"Dizionario non ha il metodo '{metodo}'", riga)

    def _metodo_lista(self, lista, metodo, args, riga):
        if metodo == "aggiungi":  lista.append(args[0]); return lista
        if metodo == "rimuovi":   return lista.pop(int(args[0]))
        if metodo == "lunghezza": return len(lista)
        if metodo == "contiene":  return args[0] in lista
        if metodo == "inverti":   lista.reverse(); return lista
        if metodo == "taglia":
            inizio = int(args[0]) if len(args) > 0 else 0
            fine   = int(args[1]) if len(args) > 1 else len(lista)
            return lista[inizio:fine]
        if metodo == "ordina":    lista.sort(); return lista
        if metodo == "unisci":
            sep = str(args[0]) if args else ", "
            return sep.join(self._a_testo(e) for e in lista)
        raise ErroreEsecuzione(f"Lista non ha il metodo '{metodo}'", riga)

    def _metodo_testo(self, testo, metodo, args, riga):
        if metodo == "lunghezza":
            return len(testo)
        if metodo == "maiuscolo":
            return testo.upper()
        if metodo == "minuscolo":
            return testo.lower()
        if metodo == "contiene":
            return args[0] in testo
        if metodo == "inizia_con":
            return testo.startswith(args[0])
        if metodo == "finisce_con":
            return testo.endswith(args[0])
        if metodo == "sostituisci":
            return testo.replace(args[0], args[1])
        if metodo == "dividi":
            sep = args[0] if args else " "
            return testo.split(sep)
        raise ErroreEsecuzione(f"Testo non ha il metodo '{metodo}'", riga)

    # ── Conversione a testo ───────────────────

    def _a_testo(self, v: Any) -> str:
        if v is None:   return "nulla"
        if v is True:   return "vero"
        if v is False:  return "falso"
        if isinstance(v, float) and v == int(v):
            return str(int(v))
        if isinstance(v, dict):
            coppie = ", ".join(f"{self._a_testo(k)}: {self._a_testo(val)}" for k, val in v.items())
            return "{" + coppie + "}"
        if isinstance(v, list):
            return "[" + ", ".join(self._a_testo(e) for e in v) + "]"
        return str(v)


# ─────────────────────────────────────────────
#  Funzione di utilità
# ─────────────────────────────────────────────

def esegui(sorgente: str, output_fn=print) -> Any:
    """Scorciatoia: crea l'Interpreter ed esegue il sorgente."""
    return Interpreter(output_fn=output_fn).esegui(sorgente)


# ─────────────────────────────────────────────
#  Demo
# ─────────────────────────────────────────────

if __name__ == "__main__":

    programmi = {

        "Fattoriale ricorsivo": """\
funzione fattoriale(n: numero) -> numero
    se n <= 1
        restituisci 1
    altrimenti
        restituisci n * fattoriale(n - 1)

scrivi("5! = " + a_testo(fattoriale(5)))
scrivi("10! = " + a_testo(fattoriale(10)))
""",

        "Ciclo e lista": """\
numeri = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
pari = []
per ogni n in numeri
    se n % 2 == 0
        aggiungi(pari, n)
scrivi("Numeri pari: " + a_testo(pari))
""",

        "Classe Animale": """\
classe Animale
    nome: testo
    zampe: numero

    funzione presenta()
        scrivi("Sono " + nome + " e ho " + a_testo(zampe) + " zampe.")

gatto = Animale(nome: "Micio", zampe: 4)
gatto.presenta()
""",

        "Fibonacci": """\
funzione fibonacci(n: numero) -> numero
    se n <= 1
        restituisci n
    altrimenti
        restituisci fibonacci(n - 1) + fibonacci(n - 2)

i = 0
finché i < 8
    scrivi("fib(" + a_testo(i) + ") = " + a_testo(fibonacci(i)))
    i = i + 1
""",

        "Metodi su testo e lista": """\
saluto = "ciao mondo"
scrivi(saluto.maiuscolo())
scrivi(saluto.sostituisci("mondo", "Alba"))

parole = saluto.dividi(" ")
scrivi("Parole: " + a_testo(parole))
scrivi("Lunghezza: " + a_testo(lunghezza(parole)))
""",
    }

    separatore = "═" * 50
    interprete = Interpreter()

    for titolo, codice in programmi.items():
        print(f"\n{separatore}")
        print(f"  {titolo}")
        print(separatore)
        try:
            interprete.esegui(codice)
        except Exception as e:
            print(f"✗ {e}")

    print(f"\n{separatore}")
    print("  Alba è pronto.")
    print(separatore)
