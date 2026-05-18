# Guida ad Alba 🌅
### Il linguaggio di programmazione in italiano

---

## Cos'è Alba?

**Alba** è un linguaggio di programmazione pensato per imparare a programmare in italiano.
Con Alba puoi scrivere istruzioni che il computer capisce ed esegue, usando parole italiane come `se`, `funzione`, `per ogni`.

---

## Come si usa

Apri il file `Alba.exe` (su Windows) oppure scrivi nel terminale:
```
python alba_repl.py
```

Vedrai apparire `>>>` — il computer è pronto ad ascoltarti.

---

## 1. Il tuo primo programma

```
scrivi("Ciao, mondo!")
```

`scrivi` mostra un messaggio sullo schermo. Il testo va sempre tra virgolette doppie `"..."`.

---

## 2. Variabili

Una variabile è una scatola con un nome che contiene un valore.

```
nome = "Luca"
eta = 14
altezza = 1.72

scrivi("Mi chiamo " + nome)
scrivi("Ho " + a_testo(eta) + " anni")
```

### Tipi di valori

| Tipo | Esempi | Descrizione |
|---|---|---|
| `numero` | `42`, `3.14`, `-5` | Numeri interi e decimali |
| `testo` | `"ciao"`, `"Alba"` | Parole e frasi |
| `booleano` | `vero`, `falso` | Vero o falso |
| `lista` | `[1, 2, 3]` | Sequenza di valori |
| `nulla` | `nulla` | Valore assente |

---

## 3. Operatori

### Matematici
```
scrivi(a_testo(10 + 3))   # → 13
scrivi(a_testo(10 - 3))   # → 7
scrivi(a_testo(10 * 3))   # → 30
scrivi(a_testo(10 / 3))   # → 3.333...
scrivi(a_testo(10 % 3))   # → 1  (resto della divisione)
```

### Abbreviati
```
x = 10
x += 5    # equivale a: x = x + 5  → 15
x -= 3    # equivale a: x = x - 3  → 12
x *= 2    # equivale a: x = x * 2  → 24
x /= 4    # equivale a: x = x / 4  → 6
```

### Confronto
```
5 == 5     # uguale → vero
5 != 3     # diverso → vero
5 > 3      # maggiore → vero
5 < 3      # minore → falso
5 >= 5     # maggiore o uguale → vero
5 <= 4     # minore o uguale → falso
```

### Logici
```
vero e falso   # → falso
vero o falso   # → vero
non vero       # → falso
```

---

## 4. Condizioni

```
eta = 16

se eta >= 18
    scrivi("Sei maggiorenne")
altrimenti
    scrivi("Sei minorenne")
```

> ⚠️ Il corpo del `se` deve essere **indentato di 4 spazi**.

Puoi anche controllare più condizioni:
```
voto = 8

se voto >= 9
    scrivi("Ottimo!")
altrimenti
    se voto >= 6
        scrivi("Sufficiente")
    altrimenti
        scrivi("Insufficiente")
```

---

## 5. Cicli

### `finché` — ripete finché la condizione è vera

```
i = 1
finché i <= 5
    scrivi(a_testo(i))
    i += 1
```

### `per ogni` — scorre una lista

```
frutti = ["mela", "pera", "banana"]
per ogni frutto in frutti
    scrivi(frutto)
```

### `interrompi` e `continua`

```
per ogni n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    se n % 2 != 0
        continua        # salta i dispari
    se n > 6
        interrompi      # si ferma a 6
    scrivi(a_testo(n))
# stampa: 2, 4, 6
```

---

## 6. Funzioni

Una funzione è un blocco di istruzioni con un nome che puoi richiamare più volte.

```
funzione saluta(nome: testo)
    scrivi("Ciao, " + nome + "!")

saluta("Marco")
saluta("Sofia")
```

### Funzione con valore di ritorno

```
funzione quadrato(n: numero) -> numero
    restituisci n * n

risultato = quadrato(5)
scrivi(a_testo(risultato))   # → 25
```

### Parametri con valore di default

```
funzione saluta(nome: testo, formale: booleano = falso)
    se formale
        scrivi("Buongiorno, " + nome + ".")
    altrimenti
        scrivi("Ciao, " + nome + "!")

saluta("Luca")                      # usa il default: Ciao, Luca!
saluta("Professor Rossi", vero)     # Buongiorno, Professor Rossi.
```

### Ricorsione

Una funzione può chiamare se stessa:

```
funzione fattoriale(n: numero) -> numero
    se n <= 1
        restituisci 1
    altrimenti
        restituisci n * fattoriale(n - 1)

scrivi(a_testo(fattoriale(5)))   # → 120
```

---

## 7. Liste

```
numeri = [10, 20, 30, 40, 50]

# Accesso per indice (parte da 0)
scrivi(a_testo(numeri[0]))    # → 10  (primo)
scrivi(a_testo(numeri[-1]))   # → 50  (ultimo)
scrivi(a_testo(numeri[-2]))   # → 40  (penultimo)

# Modifica
numeri[0] = 99

# Sotto-lista
scrivi(a_testo(numeri.taglia(1, 3)))   # → [20, 30]
```

### Metodi delle liste

| Metodo | Descrizione | Esempio |
|---|---|---|
| `.aggiungi(x)` | Aggiunge x alla fine | `numeri.aggiungi(60)` |
| `.rimuovi(i)` | Rimuove elemento in posizione i | `numeri.rimuovi(0)` |
| `.lunghezza()` | Numero di elementi | `numeri.lunghezza()` |
| `.contiene(x)` | Controlla se x è nella lista | `numeri.contiene(10)` |
| `.inverti()` | Inverte l'ordine | `numeri.inverti()` |
| `.ordina()` | Ordina crescente | `numeri.ordina()` |
| `.taglia(a, b)` | Sotto-lista da a a b | `numeri.taglia(1, 3)` |
| `.unisci(sep)` | Unisce in testo | `numeri.unisci(", ")` |

### Operatore `in`

```
colori = ["rosso", "verde", "blu"]

se "verde" in colori
    scrivi("verde trovato!")

se non ("giallo" in colori)
    scrivi("giallo non c'è")
```

---

## 8. Testo (stringhe)

```
saluto = "ciao mondo"

scrivi(saluto.maiuscolo())             # → CIAO MONDO
scrivi(saluto.minuscolo())             # → ciao mondo
scrivi(saluto.sostituisci("mondo", "Alba"))  # → ciao Alba
scrivi(a_testo(saluto.lunghezza()))    # → 10
scrivi(a_testo(saluto.contiene("ciao")))     # → vero

parole = saluto.dividi(" ")           # → ["ciao", "mondo"]
scrivi(parole[0])                      # → ciao
```

---

## 9. Dizionari

Un dizionario collega **chiavi** a **valori**.

```
persona = {"nome": "Luca", "eta": 25}

# Leggi
scrivi(persona["nome"])         # → Luca
scrivi(a_testo(persona["eta"])) # → 25

# Aggiungi o modifica
persona["citta"] = "Roma"

# Metodi
scrivi(a_testo(persona.chiavi()))    # → [nome, eta, citta]
scrivi(a_testo(persona.valori()))    # → [Luca, 25, Roma]
scrivi(a_testo(persona.contiene("nome")))  # → vero
```

---

## 10. Classi e oggetti

Una **classe** è un modello. Un **oggetto** è un'istanza di quella classe.

```
classe Animale
    nome: testo
    zampe: numero

    funzione presenta()
        scrivi("Sono " + nome + " e ho " + a_testo(zampe) + " zampe.")

gatto = Animale(nome: "Micio", zampe: 4)
gatto.presenta()
```

### Ereditarietà

Una classe figlia eredita tutto dal genitore e può aggiungere o cambiare comportamenti.

```
classe Cane(Animale)
    razza: testo

    funzione verso()
        scrivi(nome + " dice: Bau!")

fido = Cane(nome: "Fido", zampe: 4, razza: "Labrador")
fido.presenta()   # ereditato da Animale
fido.verso()      # definito in Cane
```

---

## 11. Gestione degli errori

```
prova
    x = 10 / 0
cattura errore
    scrivi("Errore: " + errore)
```

---

## 12. Moduli

Puoi dividere il codice in più file `.alba`:

```
# matematica.alba
funzione quadrato(n: numero) -> numero
    restituisci n * n
```

```
# programma.alba
importa "matematica.alba"
scrivi(a_testo(quadrato(7)))   # → 49
```

---

## 13. Funzioni predefinite

| Funzione | Descrizione | Esempio |
|---|---|---|
| `scrivi(x)` | Stampa x | `scrivi("ciao")` |
| `leggi(prompt)` | Legge input | `nome = leggi("Nome: ")` |
| `a_testo(x)` | Converte in testo | `a_testo(42)` → `"42"` |
| `a_numero(x)` | Converte in numero | `a_numero("42")` → `42` |
| `lunghezza(x)` | Lunghezza lista o testo | `lunghezza([1,2,3])` → `3` |
| `tipo(x)` | Tipo del valore | `tipo(42)` → `"numero"` |
| `intervallo(n)` | Lista da 0 a n-1 | `intervallo(5)` → `[0,1,2,3,4]` |
| `intervallo(a,b)` | Lista da a a b-1 | `intervallo(2,5)` → `[2,3,4]` |

---

## 14. Comandi del REPL

Quando usi il REPL interattivo (`python alba_repl.py`):

| Comando | Descrizione |
|---|---|
| `:aiuto` | Mostra i comandi disponibili |
| `:vars` | Mostra le variabili definite |
| `:pulisci` | Azzera tutte le variabili |
| `:esci` | Chiude il REPL |

---

## Errori comuni

| Errore | Causa | Soluzione |
|---|---|---|
| `Variabile 'x' non definita` | Hai usato x senza assegnarle un valore | Scrivi `x = ...` prima |
| `Divisione per zero` | Hai diviso per 0 | Controlla il divisore |
| `Indice fuori dalla lista` | Hai usato un indice troppo grande | Gli indici partono da 0 |
| `Stringa non chiusa` | Manca la virgoletta finale | Chiudi con `"` |
| `Atteso INDENT` | Il blocco non è indentato | Aggiungi 4 spazi |
| `Ciclo infinito` | Il ciclo non termina mai | Modifica la variabile del ciclo |

---

## Esempio completo

```
# Programma: gestione lista della spesa

classe Prodotto
    nome: testo
    prezzo: numero
    quantita: numero

    funzione totale() -> numero
        restituisci prezzo * quantita

    funzione descrizione()
        t = prezzo * quantita
        scrivi(nome + " x" + a_testo(quantita) + " = €" + a_testo(t))

spesa = []
aggiungi(spesa, Prodotto(nome: "Pane", prezzo: 1.5, quantita: 2))
aggiungi(spesa, Prodotto(nome: "Latte", prezzo: 1.2, quantita: 3))
aggiungi(spesa, Prodotto(nome: "Pasta", prezzo: 0.9, quantita: 4))

totale = 0
per ogni prodotto in spesa
    prodotto.descrizione()
    totale += prodotto.totale()

scrivi("─────────────────")
scrivi("Totale: €" + a_testo(totale))
```

---

*Alba — un nuovo inizio nella programmazione* 🌅
