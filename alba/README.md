# Alba 🌅
### Linguaggio di Programmazione Educativo in Italiano

> **Creato dal Prof. Giovanni Pellegrino**

Alba è un linguaggio di programmazione pensato per insegnare i fondamenti
della programmazione usando parole italiane. Sintassi semplice, errori in
italiano, strumenti pronti all'uso.

---

## ✨ Caratteristiche

- **Sintassi in italiano** — `se`, `funzione`, `per ogni`, `classe`
- **Tipi completi** — numeri, testo, booleani, liste, dizionari
- **OOP** — classi con ereditarietà
- **Gestione errori** — `prova` / `cattura`
- **Moduli** — `importa "file.alba"`
- **Messaggi di errore in italiano** con evidenziazione della riga
- **Editor web** con syntax highlighting e autocomplete
- **80 test automatici**

---

## 🚀 Come iniziare

### Requisiti
- Python 3.10 o superiore

### Avvio REPL
```bash
python alba_repl.py
```

### Primo programma
```
scrivi("Ciao, mondo!")

funzione saluta(nome: testo)
    scrivi("Ciao, " + nome + "!")

saluta("Alba")
```

### Editor web
Apri `alba_editor.html` nel browser — nessuna installazione necessaria.

---

## 📁 Struttura del progetto

| File | Descrizione |
|---|---|
| `alba_lexer.py` | Analizzatore lessicale |
| `alba_parser.py` | Parser e nodi AST |
| `alba_interpreter.py` | Interprete |
| `alba_errori.py` | Messaggi di errore |
| `alba_repl.py` | Shell interattiva |
| `alba.py` | Punto di avvio (.exe) |
| `alba_test.py` | Suite 80 test automatici |
| `alba_editor.html` | Editor web completo |
| `guida_alba.pdf` | Guida per studenti |
| `esercizi_alba.pdf` | 20 esercizi con soluzioni |

---

## 📖 Esempio di codice

```
# Classe con ereditarietà
classe Animale
    nome: testo
    zampe: numero

    funzione presenta()
        scrivi("Sono " + nome + " e ho " + a_testo(zampe) + " zampe.")

classe Cane(Animale)
    razza: testo

    funzione verso()
        scrivi(nome + " dice: Bau!")

fido = Cane(nome: "Fido", zampe: 4, razza: "Labrador")
fido.presenta()
fido.verso()
```

---

## 🌐 Editor web online

👉 **[Apri l'editor web](https://pellegrino-giovanni.github.io/alba/alba_editor.html)**
*(disponibile dopo la pubblicazione su GitHub Pages)*

---

## 📄 Licenza

© 2025 Prof. Giovanni Pellegrino

Distribuito sotto licenza **Creative Commons BY-NC 4.0** —
uso libero per scopi didattici con attribuzione obbligatoria.
Vedere [LICENSE.txt](LICENSE.txt) per i dettagli.

---

## 📬 Contatti

Per collaborazioni, segnalazioni o uso istituzionale,
aprire una **Issue** su questo repository.
