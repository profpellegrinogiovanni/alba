# Esercizi di Alba 🌅
### Dal principiante all'avanzato

Ogni esercizio ha un testo, un suggerimento e una soluzione.
**Prova sempre da solo prima di leggere la soluzione!**

---

## Livello 1 — Prime istruzioni

### Esercizio 1.1 — Presentati
Scrivi un programma che stampi il tuo nome, la tua età e la tua città preferita,
ognuno su una riga separata.

**Esempio di output:**
```
Mi chiamo Marco
Ho 14 anni
Vengo da Roma
```

<details>
<summary>💡 Suggerimento</summary>
Usa <code>scrivi()</code> tre volte. Ricorda le virgolette per il testo.
</details>

<details>
<summary>✅ Soluzione</summary>

```
nome = "Marco"
eta = 14
citta = "Roma"

scrivi("Mi chiamo " + nome)
scrivi("Ho " + a_testo(eta) + " anni")
scrivi("Vengo da " + citta)
```
</details>

---

### Esercizio 1.2 — Calcolatrice
Chiedi due numeri all'utente e stampa la loro somma, differenza, prodotto e quoziente.

**Esempio di output:**
```
Somma: 15
Differenza: 5
Prodotto: 50
Quoziente: 2.0
```

<details>
<summary>💡 Suggerimento</summary>
Usa <code>leggi()</code> per leggere l'input e <code>a_numero()</code> per convertirlo.
</details>

<details>
<summary>✅ Soluzione</summary>

```
a = a_numero(leggi("Primo numero: "))
b = a_numero(leggi("Secondo numero: "))

scrivi("Somma: " + a_testo(a + b))
scrivi("Differenza: " + a_testo(a - b))
scrivi("Prodotto: " + a_testo(a * b))
scrivi("Quoziente: " + a_testo(a / b))
```
</details>

---

### Esercizio 1.3 — Pari o dispari
Leggi un numero e stampa se è pari o dispari.

<details>
<summary>💡 Suggerimento</summary>
Un numero è pari se il resto della divisione per 2 è zero: <code>n % 2 == 0</code>
</details>

<details>
<summary>✅ Soluzione</summary>

```
n = a_numero(leggi("Inserisci un numero: "))

se n % 2 == 0
    scrivi(a_testo(n) + " è pari")
altrimenti
    scrivi(a_testo(n) + " è dispari")
```
</details>

---

### Esercizio 1.4 — Massimo di tre numeri
Dati tre numeri, stampa il più grande.

<details>
<summary>💡 Suggerimento</summary>
Confronta i numeri a coppie con <code>se</code> annidati, oppure usa una variabile <code>massimo</code>.
</details>

<details>
<summary>✅ Soluzione</summary>

```
a = 17
b = 42
c = 8

massimo = a
se b > massimo
    massimo = b
se c > massimo
    massimo = c

scrivi("Il massimo è: " + a_testo(massimo))
```
</details>

---

## Livello 2 — Cicli

### Esercizio 2.1 — Tabellina
Scrivi un programma che stampa la tabellina del 7.

**Output atteso:**
```
7 x 1 = 7
7 x 2 = 14
...
7 x 10 = 70
```

<details>
<summary>💡 Suggerimento</summary>
Usa <code>per ogni n in intervallo(1, 11)</code>
</details>

<details>
<summary>✅ Soluzione</summary>

```
per ogni n in intervallo(1, 11)
    risultato = 7 * n
    scrivi("7 x " + a_testo(n) + " = " + a_testo(risultato))
```
</details>

---

### Esercizio 2.2 — Conta da A a B
Leggi due numeri A e B e stampa tutti i numeri da A a B inclusi.

<details>
<summary>💡 Suggerimento</summary>
Usa <code>intervallo(a, b + 1)</code> per includere B.
</details>

<details>
<summary>✅ Soluzione</summary>

```
a = a_numero(leggi("Da: "))
b = a_numero(leggi("A: "))

per ogni n in intervallo(a, b + 1)
    scrivi(a_testo(n))
```
</details>

---

### Esercizio 2.3 — Somma di una lista
Data una lista di numeri, calcola e stampa la loro somma e la media.

```
voti = [7, 8, 6, 9, 7, 10, 5, 8]
```

<details>
<summary>💡 Suggerimento</summary>
Usa una variabile <code>totale = 0</code> e aggiungila ad ogni iterazione.
</details>

<details>
<summary>✅ Soluzione</summary>

```
voti = [7, 8, 6, 9, 7, 10, 5, 8]
totale = 0

per ogni v in voti
    totale += v

media = totale / lunghezza(voti)
scrivi("Somma: " + a_testo(totale))
scrivi("Media: " + a_testo(media))
```
</details>

---

### Esercizio 2.4 — FizzBuzz
Stampa i numeri da 1 a 30. Ma:
- Se il numero è divisibile per 3, stampa "Fizz"
- Se è divisibile per 5, stampa "Buzz"
- Se è divisibile per entrambi, stampa "FizzBuzz"

<details>
<summary>💡 Suggerimento</summary>
Controlla prima <code>n % 15 == 0</code>, poi 3, poi 5.
</details>

<details>
<summary>✅ Soluzione</summary>

```
per ogni n in intervallo(1, 31)
    se n % 15 == 0
        scrivi("FizzBuzz")
    altrimenti
        se n % 3 == 0
            scrivi("Fizz")
        altrimenti
            se n % 5 == 0
                scrivi("Buzz")
            altrimenti
                scrivi(a_testo(n))
```
</details>

---

### Esercizio 2.5 — Indovina il numero
Il programma ha un numero segreto. L'utente deve indovinarlo.
Il programma deve dire "troppo alto", "troppo basso" o "esatto!".

<details>
<summary>💡 Suggerimento</summary>
Usa un ciclo <code>finché</code> e <code>interrompi</code> quando l'utente indovina.
</details>

<details>
<summary>✅ Soluzione</summary>

```
segreto = 42
tentativi = 0

scrivi("Ho pensato un numero tra 1 e 100. Indovina!")

finché vero
    guess = a_numero(leggi("Il tuo tentativo: "))
    tentativi += 1

    se guess == segreto
        scrivi("Esatto! Ci hai messo " + a_testo(tentativi) + " tentativi.")
        interrompi
    altrimenti
        se guess < segreto
            scrivi("Troppo basso!")
        altrimenti
            scrivi("Troppo alto!")
```
</details>

---

## Livello 3 — Funzioni

### Esercizio 3.1 — Potenza
Scrivi una funzione `potenza(base, esponente)` che calcola base^esponente
**senza usare la moltiplicazione diretta** — solo un ciclo.

<details>
<summary>💡 Suggerimento</summary>
Moltiplica <code>base</code> per se stesso <code>esponente</code> volte usando un ciclo.
</details>

<details>
<summary>✅ Soluzione</summary>

```
funzione potenza(base: numero, esp: numero) -> numero
    risultato = 1
    per ogni n in intervallo(esp)
        risultato *= base
    restituisci risultato

scrivi(a_testo(potenza(2, 8)))    # → 256
scrivi(a_testo(potenza(3, 4)))    # → 81
scrivi(a_testo(potenza(10, 3)))   # → 1000
```
</details>

---

### Esercizio 3.2 — È primo?
Scrivi una funzione `è_primo(n)` che restituisce `vero` se n è primo, `falso` altrimenti.

<details>
<summary>💡 Suggerimento</summary>
Un numero è primo se è divisibile solo per 1 e per se stesso.
Controlla tutti i divisori da 2 fino a n-1.
</details>

<details>
<summary>✅ Soluzione</summary>

```
funzione è_primo(n: numero) -> booleano
    se n < 2
        restituisci falso
    per ogni d in intervallo(2, n)
        se n % d == 0
            restituisci falso
    restituisci vero

# Stampa i primi 20 numeri primi
contatore = 0
n = 2
finché contatore < 20
    se è_primo(n)
        scrivi(a_testo(n))
        contatore += 1
    n += 1
```
</details>

---

### Esercizio 3.3 — Inverti una stringa
Scrivi una funzione `inverti(testo)` che restituisce il testo al contrario.

**Esempio:** `inverti("ciao")` → `"oaic"`

<details>
<summary>💡 Suggerimento</summary>
Usa un ciclo che legge le lettere dal fondo con indici negativi,
oppure costruisci una lista di caratteri e usala al contrario.
</details>

<details>
<summary>✅ Soluzione</summary>

```
funzione inverti(parola: testo) -> testo
    risultato = ""
    i = lunghezza(parola) - 1
    finché i >= 0
        risultato = risultato + parola[i]
        i -= 1
    restituisci risultato

scrivi(inverti("ciao"))       # → oaic
scrivi(inverti("Alba"))       # → ablA
scrivi(inverti("radar"))      # → radar (palindromo!)
```
</details>

---

### Esercizio 3.4 — Palindromo
Usando la funzione dell'esercizio 3.3, scrivi una funzione `è_palindromo(parola)`
che dice se una parola si legge uguale al contrario.

<details>
<summary>✅ Soluzione</summary>

```
funzione inverti(parola: testo) -> testo
    risultato = ""
    i = lunghezza(parola) - 1
    finché i >= 0
        risultato = risultato + parola[i]
        i -= 1
    restituisci risultato

funzione è_palindromo(parola: testo) -> booleano
    restituisci parola.minuscolo() == inverti(parola.minuscolo())

parole = ["radar", "alba", "anna", "kayak", "ciao", "livello"]
per ogni p in parole
    se è_palindromo(p)
        scrivi(p + " è un palindromo")
    altrimenti
        scrivi(p + " non è un palindromo")
```
</details>

---

### Esercizio 3.5 — Fibonacci con memoizzazione
La versione ricorsiva di Fibonacci è lenta per numeri grandi.
Scrivi una versione che usa un dizionario per ricordare i risultati già calcolati.

<details>
<summary>💡 Suggerimento</summary>
Prima di calcolare, controlla se il risultato è già nel dizionario <code>memo</code>.
</details>

<details>
<summary>✅ Soluzione</summary>

```
memo = {0: 0, 1: 1}

funzione fib(n: numero) -> numero
    se n in memo
        restituisci memo[n]
    risultato = fib(n - 1) + fib(n - 2)
    memo[n] = risultato
    restituisci risultato

per ogni i in intervallo(10)
    scrivi("fib(" + a_testo(i) + ") = " + a_testo(fib(i)))

scrivi("fib(30) = " + a_testo(fib(30)))
```
</details>

---

## Livello 4 — Liste avanzate

### Esercizio 4.1 — Ordina senza usare .ordina()
Implementa l'algoritmo **Bubble Sort** per ordinare una lista.

**Idea:** scorri la lista più volte, scambiando elementi adiacenti se sono nell'ordine sbagliato.

<details>
<summary>💡 Suggerimento</summary>
Usa due cicli annidati. Il ciclo esterno ripete il passaggio,
quello interno confronta coppie adiacenti.
</details>

<details>
<summary>✅ Soluzione</summary>

```
funzione bubble_sort(v: lista) -> lista
    n = lunghezza(v)
    per ogni i in intervallo(n)
        per ogni j in intervallo(n - i - 1)
            se v[j] > v[j + 1]
                temp = v[j]
                v[j] = v[j + 1]
                v[j + 1] = temp
    restituisci v

numeri = [64, 34, 25, 12, 22, 11, 90]
scrivi("Prima: " + a_testo(numeri))
bubble_sort(numeri)
scrivi("Dopo:  " + a_testo(numeri))
```
</details>

---

### Esercizio 4.2 — Ricerca binaria
Scrivi una funzione che cerca un valore in una lista **già ordinata**
usando la ricerca binaria (più efficiente della ricerca lineare).

**Idea:** controlla l'elemento a metà, poi cerca nella metà sinistra o destra.

<details>
<summary>✅ Soluzione</summary>

```
funzione ricerca_binaria(v: lista, target: numero) -> numero
    sx = 0
    dx = lunghezza(v) - 1

    finché sx <= dx
        centro = (sx + dx) / 2
        centro = a_numero(a_testo(centro).dividi(".")[0])

        se v[centro] == target
            restituisci centro
        altrimenti
            se v[centro] < target
                sx = centro + 1
            altrimenti
                dx = centro - 1

    restituisci -1

lista = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
scrivi(a_testo(ricerca_binaria(lista, 23)))    # → 5
scrivi(a_testo(ricerca_binaria(lista, 100)))   # → -1
```
</details>

---

### Esercizio 4.3 — Frequenza delle parole
Data una frase, conta quante volte appare ogni parola.

```
frase = "il gatto e il cane e il gatto dormono"
```

<details>
<summary>💡 Suggerimento</summary>
Usa un dizionario dove le chiavi sono le parole e i valori le frequenze.
</details>

<details>
<summary>✅ Soluzione</summary>

```
frase = "il gatto e il cane e il gatto dormono"
parole = frase.dividi(" ")
freq = {}

per ogni parola in parole
    se parola in freq
        freq[parola] = freq[parola] + 1
    altrimenti
        freq[parola] = 1

chiavi = freq.chiavi()
chiavi.ordina()
per ogni k in chiavi
    scrivi(k + ": " + a_testo(freq[k]))
```
</details>

---

## Livello 5 — Classi e oggetti

### Esercizio 5.1 — Conto bancario
Crea una classe `ContoBancario` con:
- Attributi: `intestatario` (testo), `saldo` (numero)
- Metodi: `deposita(importo)`, `preleva(importo)`, `mostra_saldo()`
- Il prelievo non deve andare in negativo

<details>
<summary>✅ Soluzione</summary>

```
classe ContoBancario
    intestatario: testo
    saldo: numero

    funzione deposita(importo: numero)
        saldo += importo
        scrivi("Depositato €" + a_testo(importo) + ". Saldo: €" + a_testo(saldo))

    funzione preleva(importo: numero)
        se importo > saldo
            scrivi("Fondi insufficienti! Saldo disponibile: €" + a_testo(saldo))
        altrimenti
            saldo -= importo
            scrivi("Prelevato €" + a_testo(importo) + ". Saldo: €" + a_testo(saldo))

    funzione mostra_saldo()
        scrivi(intestatario + " — Saldo: €" + a_testo(saldo))

conto = ContoBancario(intestatario: "Luca Rossi", saldo: 1000)
conto.mostra_saldo()
conto.deposita(500)
conto.preleva(200)
conto.preleva(2000)
```
</details>

---

### Esercizio 5.2 — Biblioteca
Crea un sistema per gestire una biblioteca con:
- Classe `Libro`: titolo, autore, disponibile (booleano)
- Classe `Biblioteca`: lista di libri, metodi per aggiungere, prestare e restituire libri

<details>
<summary>✅ Soluzione</summary>

```
classe Libro
    titolo: testo
    autore: testo
    disponibile: booleano

    funzione info()
        stato = "disponibile"
        se non disponibile
            stato = "in prestito"
        scrivi(titolo + " — " + autore + " [" + stato + "]")

classe Biblioteca
    libri: lista

    funzione aggiungi_libro(libro: testo)
        aggiungi(libri, libro)
        scrivi("Aggiunto: " + libro.titolo)

    funzione presta(titolo_cercato: testo)
        per ogni libro in libri
            se libro.titolo == titolo_cercato
                se libro.disponibile
                    libro.disponibile = falso
                    scrivi("Prestato: " + titolo_cercato)
                    restituisci nulla
                altrimenti
                    scrivi(titolo_cercato + " è già in prestito")
                    restituisci nulla
        scrivi("Libro non trovato: " + titolo_cercato)

    funzione restituisci(titolo_cercato: testo)
        per ogni libro in libri
            se libro.titolo == titolo_cercato
                libro.disponibile = vero
                scrivi("Restituito: " + titolo_cercato)
                restituisci nulla

    funzione catalogo()
        scrivi("=== CATALOGO ===")
        per ogni libro in libri
            libro.info()

bib = Biblioteca(libri: [])
aggiungi(bib.libri, Libro(titolo: "Il Piccolo Principe", autore: "Saint-Exupéry", disponibile: vero))
aggiungi(bib.libri, Libro(titolo: "1984", autore: "Orwell", disponibile: vero))
aggiungi(bib.libri, Libro(titolo: "Odissea", autore: "Omero", disponibile: vero))

bib.catalogo()
bib.presta("1984")
bib.presta("1984")
bib.restituisci("1984")
bib.catalogo()
```
</details>

---

### Esercizio 5.3 — Forma geometrica (ereditarietà)
Crea una gerarchia di classi:
- `Forma`: ha colore e metodo `area()` che restituisce 0
- `Cerchio(Forma)`: ha raggio, sovrascrive `area()` (π × r²; usa π ≈ 3.14159)
- `Rettangolo(Forma)`: ha larghezza e altezza, sovrascrive `area()`
- `Triangolo(Forma)`: ha base e altezza, sovrascrive `area()` (base × altezza / 2)

<details>
<summary>✅ Soluzione</summary>

```
classe Forma
    colore: testo

    funzione area() -> numero
        restituisci 0

    funzione descrivi()
        scrivi(tipo(se_stesso) + " " + colore + " — area: " + a_testo(area()))

classe Cerchio(Forma)
    raggio: numero

    funzione area() -> numero
        restituisci 3.14159 * raggio * raggio

classe Rettangolo(Forma)
    larghezza: numero
    altezza: numero

    funzione area() -> numero
        restituisci larghezza * altezza

classe Triangolo(Forma)
    base: numero
    altezza: numero

    funzione area() -> numero
        restituisci base * altezza / 2

forme = []
aggiungi(forme, Cerchio(colore: "rosso", raggio: 5))
aggiungi(forme, Rettangolo(colore: "blu", larghezza: 4, altezza: 6))
aggiungi(forme, Triangolo(colore: "verde", base: 3, altezza: 8))

totale = 0
per ogni f in forme
    f.descrivi()
    totale += f.area()

scrivi("Area totale: " + a_testo(totale))
```
</details>

---

## Livello 6 — Sfide finali

### Sfida 6.1 — Gioco della vita semplificato
Simula una popolazione di animali per 10 generazioni.
Ogni anno: se ci sono più di 10 animali, 3 muoiono; se sono meno di 5, nascono 4 cuccioli.

<details>
<summary>✅ Soluzione</summary>

```
popolazione = 7
scrivi("Anno 0: " + a_testo(popolazione) + " animali")

per ogni anno in intervallo(1, 11)
    se popolazione > 10
        popolazione -= 3
    altrimenti
        se popolazione < 5
            popolazione += 4
    scrivi("Anno " + a_testo(anno) + ": " + a_testo(popolazione) + " animali")
```
</details>

---

### Sfida 6.2 — Cifrario di Cesare
Implementa il cifrario di Cesare: sposta ogni lettera di N posizioni nell'alfabeto.

**Esempio con N=3:** `"ciao"` → `"fldr"`

<details>
<summary>💡 Suggerimento</summary>
Crea una lista con le lettere dell'alfabeto. Per ogni carattere, trova la sua posizione,
aggiungi N (con modulo 26) e prendi la lettera corrispondente.
</details>

<details>
<summary>✅ Soluzione</summary>

```
alfabeto = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
            "n","o","p","q","r","s","t","u","v","w","x","y","z"]

funzione cifra(testo_in: testo, n: numero) -> testo
    risultato = ""
    per ogni ch in testo_in.dividi("")
        se ch in alfabeto
            idx = 0
            per ogni i in intervallo(lunghezza(alfabeto))
                se alfabeto[i] == ch
                    idx = i
                    interrompi
            nuovo_idx = (idx + n) % 26
            risultato = risultato + alfabeto[nuovo_idx]
        altrimenti
            risultato = risultato + ch
    restituisci risultato

funzione decifra(testo_in: testo, n: numero) -> testo
    restituisci cifra(testo_in, 26 - n)

msg = "ciao mondo"
cifrato = cifra(msg, 3)
scrivi("Originale: " + msg)
scrivi("Cifrato:   " + cifrato)
scrivi("Decifrato: " + decifra(cifrato, 3))
```
</details>

---

### Sfida 6.3 — Gestione studenti
Crea un sistema completo per gestire una classe scolastica:
- Classe `Studente` con nome, voti (lista), metodi per aggiungere voto e calcolare media
- Funzione per trovare il miglior studente
- Funzione per stampare la classifica

<details>
<summary>✅ Soluzione</summary>

```
classe Studente
    nome: testo
    voti: lista

    funzione aggiungi_voto(v: numero)
        aggiungi(voti, v)

    funzione media() -> numero
        se lunghezza(voti) == 0
            restituisci 0
        totale = 0
        per ogni v in voti
            totale += v
        restituisci totale / lunghezza(voti)

    funzione info()
        scrivi(nome + " — media: " + a_testo(media()) + " — voti: " + a_testo(voti))

funzione miglior_studente(classe: lista) -> testo
    migliore = classe[0]
    per ogni s in classe
        se s.media() > migliore.media()
            migliore = s
    restituisci migliore.nome

classe_scolastica = []
nomi = ["Alice", "Bruno", "Carla", "Davide", "Elena"]
voti_lista = [
    [8, 7, 9, 8],
    [6, 7, 6, 8],
    [9, 10, 9, 10],
    [7, 6, 8, 7],
    [8, 9, 7, 9]
]

per ogni i in intervallo(lunghezza(nomi))
    s = Studente(nome: nomi[i], voti: voti_lista[i])
    aggiungi(classe_scolastica, s)

scrivi("=== REGISTRO ===")
per ogni s in classe_scolastica
    s.info()

scrivi("")
scrivi("Miglior studente: " + miglior_studente(classe_scolastica))
```
</details>

---

*Buono studio con Alba! 🌅*
*Se ti blocchi, rileggi la guida o chiedi aiuto.*
