# 09 - Da Thonny a Cursor

## Obiettivo

Passare a un IDE vero, mettere il tuo codice sotto git, e capire come usare
l'AI senza che ti rubi il mestiere. Nessun circuito nuovo: e' una guida di
strumenti.

## Perche' adesso e non prima

Thonny e' fatto per imparare, e per le prime otto guide era la scelta giusta:
si apre, funziona, non ti distrae. Ma ha dei limiti che ormai inizi a sentire:

- Non gestisce bene progetti su piu' file
- Non ha git
- Ti fa lavorare su un file per volta, e i progetti veri non sono cosi'

Cursor e' un editor professionale (e' una versione modificata di VS Code) e fa
tutte queste cose. Ed e' quello che usa tuo padre per lavoro, quindi se ti
blocchi ha senso che sappiate parlare della stessa cosa.

Thonny non buttarlo: **resta lo strumento migliore quando qualcosa non va**.
La sua Shell e' immediata e in dieci secondi ti dice se il Pico e' vivo.

## Passo 1 - Installa le due estensioni

Apri Cursor. Nella barra laterale clicca l'icona delle **Estensioni** (i quattro
quadratini), poi cerca e installa:

| Estensione | A cosa serve |
|---|---|
| **MicroPico** (di paulober) | il cuore: REPL, upload dei file, autocompletamento MicroPython |
| **Raspberry Pi Pico** (di Raspberry Pi) | serve a MicroPico per flashare il firmware |

> Cursor non usa il marketplace di Microsoft ma un registro aperto che si
> chiama Open VSX. Entrambe le estensioni ci sono e sono aggiornate, quindi si
> installano normalmente dal pannello. Se un domani cerchi un'estensione e non
> la trovi, e' quasi sempre questo il motivo.

## Passo 2 - Apri il progetto

**File > Apri cartella** e scegli la cartella di questo repository.

Importante: apri **la cartella**, non un singolo file. MicroPico ha bisogno di
una cartella di progetto per funzionare.

In basso, nella barra di stato, dovresti vedere comparire dei pulsanti nuovi:
`Pico Connected` (o `Pico Disconnected`), `Run`, `Stop`.

Se c'e' scritto disconnesso, collega l'USB e clicca sulla scritta.

## Passo 3 - Il tuo primo upload

Crea un file `progetti-daniele/prova.py`:

```python
from machine import Pin
import time

led = Pin(25, Pin.OUT)

for i in range(10):
    led.toggle()
    time.sleep(0.2)

print("Fatto")
```

Ora premi `Ctrl+Shift+P` per aprire la **palette dei comandi**, scrivi
`MicroPico` e guarda le opzioni. Quelle che userai:

| Comando | Cosa fa |
|---|---|
| **Run current file on Pico** | esegue il file senza salvarlo sulla scheda |
| **Upload current file to Pico** | copia il file nella memoria del Pico |
| **Upload project to Pico** | copia tutta la cartella |
| **Download project from Pico** | il contrario, tira giu' quello che c'e' sulla scheda |
| **Delete all files from Pico** | pulizia totale, quando ti sei incasinato |

Lancia **Run current file on Pico**. Il LED lampeggia dieci volte e nel
terminale compare `Fatto`.

C'e' anche la REPL: comando **MicroPico: Connect** e poi il terminale diventa
la Shell del Pico, esattamente come in Thonny.

### Run o Upload?

Serve chiarirlo perche' e' fonte di confusione:

- **Run** esegue il file **dalla RAM**, senza scriverlo sulla scheda. Se
  stacchi l'USB, sparisce. Ottimo mentre provi.
- **Upload** lo **scrive nella flash** del Pico. Resta li' anche senza PC. Un
  file caricato come `main.py` parte da solo all'accensione.

Durante lo sviluppo usi **Run**. Quando il progetto e' finito e lo vuoi far
funzionare da solo, fai **Upload** come `main.py`.

## Passo 4 - Il firmware, se ti serve

Non ti serve adesso (l'hai gia' flashato nella guida 03), ma segnatelo per il
giorno in cui vorrai aggiornarlo.

MicroPico ha un comando **Easy Flash**: metti il Pico in BOOTSEL, lanci il
comando, e lui scarica il firmware giusto e lo installa da solo. E' comodo, e
funziona perche' l'estensione ufficiale Raspberry Pi gli fornisce uno strumento
che si chiama `picotool`.

Detto questo: **continua a saper fare il metodo manuale** della guida 03
(BOOTSEL, disco `RPI-RP2`, trascini il `.uf2`). Quando lo strumento comodo si
rompe - e prima o poi capita - chi sa fare la cosa a mano in tre minuti ne
esce, chi sa solo cliccare un pulsante resta fermo.

## Passo 5 - mpremote, per quando vuoi fare in fretta

C'e' un terzo modo di parlare col Pico, che non dipende da nessun editor:
`mpremote`, lo strumento ufficiale di MicroPython. Si installa una volta sola:

```bash
pip install mpremote
```

E poi dal terminale:

| Comando | Cosa fa |
|---|---|
| `mpremote` | apri la REPL (esci con `Ctrl+]`) |
| `mpremote run prova.py` | esegui un file |
| `mpremote cp prova.py :` | copia un file sul Pico |
| `mpremote ls` | elenca i file sulla scheda |
| `mpremote rm prova.py` | cancella un file |
| `mpremote reset` | riavvia la scheda |

Sembra scomodo rispetto ai pulsanti, ma ha due vantaggi seri. Primo: funziona
sempre, anche quando l'estensione fa i capricci. Secondo: essendo un comando da
terminale, puoi metterlo dentro uno script e automatizzare.

## Passo 6 - Git

Da qui in avanti il tuo codice sta in un repository. Ti bastano tre comandi.

Nel terminale di Cursor (`Ctrl+ backtick`):

```bash
git add progetti-daniele/
git commit -m "Aggiunto il mio primo programma"
git push
```

Cosa vuol dire:

- `git add` - dice a git quali file vuoi salvare
- `git commit` - crea un punto di salvataggio, con un messaggio che spiega cosa
  hai fatto
- `git push` - manda tutto su GitHub

**Fai un commit ogni volta che qualcosa funziona.** Non alla fine della
serata: ogni volta che una cosa comincia a girare. Cosi' quando rompi tutto
alle undici di sera, puoi tornare alla versione delle nove.

Sui messaggi di commit: scrivi **cosa hai fatto**, non "modifiche" o "prova".
Tra due mesi `Il servo ora si muove col potenziometro` ti dice qualcosa,
`update` no.

Cursor ha anche il pannello grafico di git nella barra laterale (l'icona con i
rami). Usalo pure, ma impara anche i tre comandi: i pulsanti cambiano da un
programma all'altro, `git commit` e' uguale ovunque da vent'anni.

## Passo 7 - L'AI, e come non farsi fregare

Qui c'e' la parte delicata della guida.

Cursor ha l'intelligenza artificiale integrata. Se inizi a scrivere `while`, ti
propone tutto il resto. Se le chiedi "fammi il codice per il servo", te lo
scrive in tre secondi e funziona pure.

**E questo e' un problema, adesso.**

Non per principio - tuo padre l'AI la usa tutti i giorni per lavoro, ed e' uno
strumento serio. Il punto e' un altro: lui la usa per fare in fretta cose che
saprebbe fare da solo. Tu la useresti per saltare la parte in cui impari a
farle. Sono due situazioni diverse.

Pensala cosi': in palestra puoi farti sollevare i pesi da qualcun altro. I pesi
salgono, il lavoro e' fatto, ma i muscoli non sono i tuoi.

### Come si usa bene

In questo repository c'e' un file `AGENTS.md` che dice all'AI di Cursor come
comportarsi con te: fare domande invece di dare risposte, non scriverti il
codice, spiegarti gli errori invece di correggerli. Leggitelo, e' scritto
anche per te.

Non e' un blocco: se insisti, l'AI ti aiuta comunque. E' un modo per farle
tenere il comportamento giusto **di default**, cosi' devi scegliere
attivamente di farti dare la pappa pronta.

Le domande che vale la pena farle:

- "Perche' questo codice da' questo errore?" (invece di "correggimelo")
- "Cosa fa `duty_u16` esattamente?"
- "Ho scritto questa funzione, secondo te si puo' semplificare?"
- "Come si chiama il concetto per cui il pin legge valori casuali?"

Le domande da non farle, per ora:

- "Scrivimi il codice che..."
- "Fammi l'esercizio 3"

### Consiglio pratico

**Spegni il completamento automatico mentre fai gli esercizi delle guide.** Si
disattiva dalle impostazioni, o cliccando sull'indicatore di Cursor Tab in
basso a destra.

Poi lo riaccendi per i tuoi progetti in `progetti-daniele/`. Li' sei tu che
decidi, e va benissimo cosi'.

## Prova a cambiare

1. Prendi uno dei programmi delle guide 04-08, aprilo in Cursor, eseguilo con
   **Run current file on Pico** e verifica che si comporti come in Thonny.

2. Fai il tuo primo commit: crea un file in `progetti-daniele/`, aggiungi,
   committa, pusha. Poi guarda su GitHub se e' arrivato.

3. Installa `mpremote` e fai lampeggiare il LED **senza aprire nessun editor**,
   solo da terminale. Serve a capire che tutta questa roba grafica sta sopra
   una cosa piu' semplice.

4. Apri `AGENTS.md` e leggi la tabella "Cosa ha gia' incontrato". Chiedi all'AI
   qualcosa che sta due guide piu' avanti e guarda come reagisce.

## Se non funziona

| Sintomo | Causa | Soluzione |
|---|---|---|
| `Pico Disconnected` e non si collega | Thonny e' aperto e tiene la porta | Chiudi Thonny. La porta seriale la puo' usare un programma solo. |
| Non trovo le estensioni nel pannello | Stai cercando nel posto giusto? | Icona dei quattro quadratini, cerca `MicroPico` |
| I comandi MicroPico non compaiono | Hai aperto un file invece che una cartella | **File > Apri cartella** |
| `Run` non fa niente | Nessun file attivo, o il Pico e' scollegato | Clicca dentro il file e controlla la barra di stato |
| `mpremote: command not found` | Non e' nel PATH | Prova `python -m mpremote` |
| `could not open port COM3` | La porta e' occupata | Chiudi Thonny, chiudi la REPL di MicroPico, riprova |
| Git chiede utente e password | Non sei autenticato | Chiedi a tuo padre, si configura una volta sola |

## Prossima guida

[10 - Luce e temperatura](10-luce-e-temperatura.md): torniamo all'elettronica,
con due sensori veri.
