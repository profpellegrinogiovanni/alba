"""
Alba Test Suite — verifica automatica del linguaggio.
Esegui con:  python alba_test.py
"""

import sys
import traceback
from alba_interpreter import Interpreter

# ─────────────────────────────────────────────
#  Infrastruttura di test
# ─────────────────────────────────────────────

_ok = 0
_falliti = 0
_errori = []

def test(nome: str, codice: str, atteso: list[str]):
    """
    Esegue `codice` e verifica che l'output corrisponda a `atteso`.
    `atteso` è una lista di righe di output.
    """
    global _ok, _falliti
    output_righe = []
    interp = Interpreter(output_fn=lambda r: output_righe.append(r))
    try:
        interp.esegui(codice)
    except Exception as e:
        _falliti += 1
        _errori.append(f"  ✗ [{nome}] Eccezione inattesa: {e}")
        return

    atteso_str  = [str(a) for a in atteso]
    if output_righe == atteso_str:
        _ok += 1
        print(f"  ✓ {nome}")
    else:
        _falliti += 1
        msg = (f"  ✗ {nome}\n"
               f"    atteso:   {atteso_str}\n"
               f"    ottenuto: {output_righe}")
        _errori.append(msg)
        print(msg)

def test_errore(nome: str, codice: str, frammento: str):
    """
    Verifica che `codice` lanci un'eccezione il cui messaggio
    contiene `frammento`.
    """
    global _ok, _falliti
    interp = Interpreter()
    try:
        interp.esegui(codice)
        _falliti += 1
        msg = f"  ✗ [{nome}] Atteso errore contenente '{frammento}', ma nessuna eccezione"
        _errori.append(msg)
        print(msg)
    except Exception as e:
        if frammento.lower() in str(e).lower():
            _ok += 1
            print(f"  ✓ {nome}")
        else:
            _falliti += 1
            msg = f"  ✗ [{nome}] Atteso '{frammento}', ottenuto: {e}"
            _errori.append(msg)
            print(msg)

def sezione(titolo: str):
    print(f"\n{'─'*50}")
    print(f"  {titolo}")
    print(f"{'─'*50}")


# ─────────────────────────────────────────────
#  Test
# ─────────────────────────────────────────────

sezione("1. Letterali e tipi")

test("numero intero", 'scrivi(a_testo(42))', ['42'])
test("numero decimale", 'scrivi(a_testo(3.14))', ['3.14'])
test("numero negativo", 'scrivi(a_testo(-7))', ['-7'])
test("stringa vuota", 'scrivi("")', [''])
test("booleano vero", 'scrivi(a_testo(vero))', ['vero'])
test("booleano falso", 'scrivi(a_testo(falso))', ['falso'])
test("nulla", 'scrivi(a_testo(nulla))', ['nulla'])


sezione("2. Operatori aritmetici")

test("addizione", 'scrivi(a_testo(3 + 4))', ['7'])
test("sottrazione", 'scrivi(a_testo(10 - 3))', ['7'])
test("moltiplicazione", 'scrivi(a_testo(3 * 4))', ['12'])
test("divisione", 'scrivi(a_testo(10 / 4))', ['2.5'])
test("modulo", 'scrivi(a_testo(10 % 3))', ['1'])
test("concatenazione testo", 'scrivi("ciao" + " " + "mondo")', ['ciao mondo'])
test("concatenazione testo+numero", 'scrivi("valore: " + a_testo(42))', ['valore: 42'])


sezione("3. Operatori composti")

test("+=", 'x = 5\nx += 3\nscrivi(a_testo(x))', ['8'])
test("-=", 'x = 10\nx -= 4\nscrivi(a_testo(x))', ['6'])
test("*=", 'x = 3\nx *= 4\nscrivi(a_testo(x))', ['12'])
test("/=", 'x = 12\nx /= 4\nscrivi(a_testo(x))', ['3'])


sezione("4. Confronto e logica")

test("uguale vero",     'scrivi(a_testo(5 == 5))', ['vero'])
test("uguale falso",    'scrivi(a_testo(5 == 6))', ['falso'])
test("diverso",         'scrivi(a_testo(5 != 6))', ['vero'])
test("minore",          'scrivi(a_testo(3 < 5))',  ['vero'])
test("maggiore",        'scrivi(a_testo(5 > 3))',  ['vero'])
test("min_uguale",      'scrivi(a_testo(5 <= 5))', ['vero'])
test("e logico",        'scrivi(a_testo(vero e falso))', ['falso'])
test("o logico",        'scrivi(a_testo(vero o falso))', ['vero'])
test("non logico",      'scrivi(a_testo(non vero))',  ['falso'])


sezione("5. Condizioni")

test("se vero", '''
se 5 > 3
    scrivi("sì")
''', ['sì'])

test("se falso con altrimenti", '''
se 3 > 5
    scrivi("no")
altrimenti
    scrivi("sì")
''', ['sì'])

test("se annidato", '''
x = 7
se x > 10
    scrivi("grande")
altrimenti
    se x > 5
        scrivi("medio")
    altrimenti
        scrivi("piccolo")
''', ['medio'])


sezione("6. Cicli")

test("finché base", '''
i = 0
finché i < 3
    scrivi(a_testo(i))
    i += 1
''', ['0', '1', '2'])

test("per ogni lista", '''
per ogni x in [10, 20, 30]
    scrivi(a_testo(x))
''', ['10', '20', '30'])

test("interrompi", '''
per ogni n in [1, 2, 3, 4, 5]
    se n == 3
        interrompi
    scrivi(a_testo(n))
''', ['1', '2'])

test("continua", '''
per ogni n in [1, 2, 3, 4, 5]
    se n % 2 == 0
        continua
    scrivi(a_testo(n))
''', ['1', '3', '5'])

test("intervallo", '''
per ogni n in intervallo(4)
    scrivi(a_testo(n))
''', ['0', '1', '2', '3'])

test("intervallo con inizio", '''
per ogni n in intervallo(2, 5)
    scrivi(a_testo(n))
''', ['2', '3', '4'])


sezione("7. Funzioni")

test("funzione semplice", '''
funzione saluta(nome: testo)
    scrivi("Ciao " + nome)
saluta("Luca")
''', ['Ciao Luca'])

test("funzione con ritorno", '''
funzione doppio(n: numero) -> numero
    restituisci n * 2
scrivi(a_testo(doppio(5)))
''', ['10'])

test("ricorsione fattoriale", '''
funzione fatt(n: numero) -> numero
    se n <= 1
        restituisci 1
    altrimenti
        restituisci n * fatt(n - 1)
scrivi(a_testo(fatt(5)))
''', ['120'])

test("chiusura (closure)", '''
funzione crea_moltiplicatore(n: numero)
    funzione moltiplica(x: numero) -> numero
        restituisci x * n
    restituisci moltiplica
doppio = crea_moltiplicatore(2)
scrivi(a_testo(doppio(7)))
''', ['14'])

test("parametro con default", '''
funzione saluta(nome: testo, formale: booleano = falso)
    se formale
        scrivi("Buongiorno " + nome)
    altrimenti
        scrivi("Ciao " + nome)
saluta("Marco")
saluta("Prof", vero)
''', ['Ciao Marco', 'Buongiorno Prof'])


sezione("8. Liste")

test("lista letterale", '''
v = [1, 2, 3]
scrivi(a_testo(v))
''', ['[1, 2, 3]'])

test("indice positivo", '''
v = [10, 20, 30]
scrivi(a_testo(v[0]))
scrivi(a_testo(v[2]))
''', ['10', '30'])

test("indice negativo", '''
v = [10, 20, 30]
scrivi(a_testo(v[-1]))
scrivi(a_testo(v[-3]))
''', ['30', '10'])

test("assegnazione per indice", '''
v = [1, 2, 3]
v[1] = 99
scrivi(a_testo(v))
''', ['[1, 99, 3]'])

test("aggiungi e lunghezza", '''
v = []
aggiungi(v, "a")
aggiungi(v, "b")
scrivi(a_testo(lunghezza(v)))
''', ['2'])

test("ordina", '''
v = [3, 1, 4, 1, 5]
v.ordina()
scrivi(a_testo(v))
''', ['[1, 1, 3, 4, 5]'])

test("taglia", '''
v = [10, 20, 30, 40, 50]
scrivi(a_testo(v.taglia(1, 4)))
''', ['[20, 30, 40]'])

test("unisci", '''
v = ["a", "b", "c"]
scrivi(v.unisci("-"))
''', ['a-b-c'])

test("in lista vero", '''
v = [1, 2, 3]
scrivi(a_testo(2 in v))
''', ['vero'])

test("in lista falso", '''
v = [1, 2, 3]
scrivi(a_testo(5 in v))
''', ['falso'])


sezione("9. Testo")

test("maiuscolo", 'scrivi("ciao".maiuscolo())', ['CIAO'])
test("minuscolo", 'scrivi("CIAO".minuscolo())', ['ciao'])
test("sostituisci", 'scrivi("ciao mondo".sostituisci("mondo", "alba"))', ['ciao alba'])
test("dividi", 'scrivi(a_testo("a,b,c".dividi(",")))', ['[a, b, c]'])
test("lunghezza testo", 'scrivi(a_testo(lunghezza("ciao")))', ['4'])
test("in testo", 'scrivi(a_testo("ao" in "ciao"))', ['vero'])
test("inizia con", 'scrivi(a_testo("ciao".inizia_con("ci")))', ['vero'])
test("finisce con", 'scrivi(a_testo("ciao".finisce_con("ao")))', ['vero'])


sezione("10. Dizionari")

test("dizionario letterale", '''
d = {"a": 1, "b": 2}
scrivi(a_testo(d["a"]))
''', ['1'])

test("aggiungi chiave", '''
d = {"x": 10}
d["y"] = 20
scrivi(a_testo(d["y"]))
''', ['20'])

test("contiene chiave", '''
d = {"k": 99}
scrivi(a_testo(d.contiene("k")))
scrivi(a_testo(d.contiene("z")))
''', ['vero', 'falso'])

test("in dizionario", '''
d = {"nome": "Luca"}
scrivi(a_testo("nome" in d))
''', ['vero'])

test("chiavi", '''
d = {"a": 1, "b": 2}
k = d.chiavi()
k.ordina()
scrivi(a_testo(k))
''', ['[a, b]'])


sezione("11. Classi e oggetti")

test("classe base", '''
classe Punto
    x: numero
    y: numero

    funzione descrivi()
        scrivi(a_testo(x) + "," + a_testo(y))

p = Punto(x: 3, y: 4)
p.descrivi()
''', ['3,4'])

test("metodo con ritorno", '''
classe Rettangolo
    larghezza: numero
    altezza: numero

    funzione area() -> numero
        restituisci larghezza * altezza

r = Rettangolo(larghezza: 5, altezza: 3)
scrivi(a_testo(r.area()))
''', ['15'])

test("ereditarietà", '''
classe Forma
    colore: testo

    funzione info()
        scrivi("Forma " + colore)

classe Cerchio(Forma)
    raggio: numero

    funzione area() -> numero
        restituisci raggio * raggio

c = Cerchio(colore: "rosso", raggio: 5)
c.info()
scrivi(a_testo(c.area()))
''', ['Forma rosso', '25'])


sezione("12. Gestione errori")

test("prova/cattura divisione zero", '''
prova
    x = 1 / 0
cattura e
    scrivi("catturato")
''', ['catturato'])

test("prova/cattura variabile errore", '''
prova
    y = z + 1
cattura msg
    scrivi("errore: " + a_testo(msg != nulla))
''', ['errore: vero'])

test("prova senza errori", '''
prova
    x = 10 + 5
cattura e
    scrivi("non dovrebbe stampare")
scrivi(a_testo(x))
''', ['15'])

test_errore("divisione per zero senza cattura",
    'x = 5 / 0', 'zero')

test_errore("variabile non definita",
    'scrivi(a_testo(variabile_inesistente))', 'non definita')

test_errore("indice fuori lista",
    'v = [1, 2]\nscrivi(a_testo(v[5]))', 'fuori')


sezione("13. Funzioni predefinite")

test("tipo numero",    'scrivi(tipo(42))',      ['numero'])
test("tipo testo",     'scrivi(tipo("ciao"))',  ['testo'])
test("tipo booleano",  'scrivi(tipo(vero))',    ['booleano'])
test("tipo lista",     'scrivi(tipo([1,2]))',   ['lista'])
test("tipo nulla",     'scrivi(tipo(nulla))',   ['nulla'])
test("a_numero",       'scrivi(a_testo(a_numero("42")))', ['42'])
test("lunghezza lista",'scrivi(a_testo(lunghezza([1,2,3])))', ['3'])


# ─────────────────────────────────────────────
#  Riepilogo
# ─────────────────────────────────────────────

totale = _ok + _falliti
print(f"\n{'═'*50}")
print(f"  Risultati: {_ok}/{totale} test passati", end="")
if _falliti == 0:
    print("  🎉 Tutto ok!")
else:
    print(f"  ⚠ {_falliti} falliti")
print(f"{'═'*50}\n")

if _falliti > 0:
    sys.exit(1)
