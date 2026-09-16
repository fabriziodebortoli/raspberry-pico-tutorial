# 14 - Progetto finale

## Obiettivo

Costruire una **serra automatica**: legge la temperatura e la luce, mostra
tutto sul display, apre e chiude una finestrella col servo, avvisa con LED e
buzzer, e si comanda da due pulsanti.

E' il primo programma che non entra in una schermata. Il vero argomento di
questa guida non e' l'elettronica: e' **come si organizza un programma lungo**
perche' resti comprensibile.

## Ti serve

Tutto quello che hai usato finora:

- Display LCD 1602 con il suo potenziometro di contrasto (guida 13)
- Termistore NTC con la resistenza da 10k su GP27 (guida 10)
- Fotoresistenza con la resistenza da 10k su GP26 (guida 10)
- Servomotore su GP16 (guida 11)
- 2 LED con resistenze su GP14 e GP15 (guida 05)
- Buzzer passivo su GP18 (guida 07)
- 2 pulsanti su GP20 e GP21 (guida 06)

E' la prima volta che monti tutto insieme. **Fallo un pezzo alla volta e prova
ogni pezzo prima di aggiungere il successivo.** Se colleghi tutto e poi non
funziona niente, hai venti fili da controllare invece di due.

## Cosa deve fare

| Situazione | Comportamento |
|---|---|
| Temperatura sopra i 26 gradi | il servo apre la finestrella, LED rosso acceso |
| Temperatura sotto i 22 gradi | il servo chiude, LED rosso spento |
| Tra 22 e 26 gradi | non cambia niente (isteresi, guida 10) |
| Poca luce | LED bianco acceso, come un lampione |
| Temperatura sopra i 32 gradi | allarme: il buzzer suona |
| Pulsante A | cambia schermata sul display |
| Pulsante B | forza l'apertura o la chiusura a mano |

## Il problema dei programmi lunghi

Se scrivi questa roba di getto, esce un `while True` di ottanta righe con
quindici `if` annidati. Funziona, magari, ma dopo due settimane non ci capisci
piu' niente e ogni modifica ne rompe un'altra.

Il metodo per evitarlo si chiama **separazione delle responsabilita'**: dividi
il programma in pezzi che fanno **una cosa sola**, e ogni pezzo lo puoi
capire, provare e sistemare da solo.

Il ciclo principale diventa questo, e non cresce mai:

```
    LEGGI  ->  DECIDI  ->  AGISCI  ->  MOSTRA
      ^                                   |
      +-----------------------------------+
```

- **Leggi**: interroga i sensori, metti via i numeri. Non decide niente.
- **Decidi**: guarda i numeri e aggiorna lo stato. Non tocca l'hardware.
- **Agisci**: guarda lo stato e comanda servo, LED, buzzer. Non decide niente.
- **Mostra**: scrive sul display. Non tocca nient'altro.

Il vantaggio e' pratico: se la finestra si apre quando non dovrebbe, il
problema e' in **Decidi** e non devi guardare altro. Se si apre al momento
giusto ma il servo non si muove, e' in **Agisci**.

## La macchina a stati

C'e' un'altra idea da mettere in piedi: lo **stato**.

Il programma in ogni momento si trova in una situazione precisa, e le
situazioni possibili sono poche e note:

```
        +-------------------+
        |  serra CHIUSA     |
        +-------------------+
            |            ^
   temp > 26|            | temp < 22
            v            |
        +-------------------+
        |  serra APERTA     |
        +-------------------+
                 |
        temp > 32|
                 v
        +-------------------+
        |     ALLARME       |
        +-------------------+
```

Una variabile tiene lo stato corrente, e il programma decide cosa fare in base
a quello. Si chiama **macchina a stati finiti**, e' uno degli strumenti piu'
usati nei sistemi embedded, e te la ritroverai in terza e in quarta.

Il punto importante: **lo stato non si deduce ogni volta dai sensori, si
ricorda.** E' proprio grazie alla memoria dello stato che funziona l'isteresi.

## Il codice

Il programma completo e' in
[`codice/14-serra/serra.py`](../codice/14-serra/serra.py). Qui commento i pezzi
che contano.

### La configurazione in cima

```python
# --- CONFIGURAZIONE ---
PIN_NTC = 27
PIN_LDR = 26
PIN_SERVO = 16
# ...

TEMP_APRI = 26.0
TEMP_CHIUDI = 22.0
TEMP_ALLARME = 32.0
SOGLIA_BUIO = 18000
```

Tutti i numeri regolabili stanno **in cima al file**, in maiuscolo, con un
nome che dice cosa sono.

Perche' conta: quando fra un mese vorrai cambiare la soglia, la trovi in tre
secondi invece di cercare un `26.0` sparso in mezzo al codice. E se lo stesso
numero compare in due posti, cambiandone uno solo introduci un bug che ci
metti un'ora a trovare.

### Leggere

```python
def leggi_temperatura():
    """Restituisce la temperatura in gradi centigradi."""
    tensione = ntc.read_u16() * 3.3 / 65535
    resistenza = R_FISSA * (3.3 - tensione) / tensione
    inverso_T = 1 / T0 + (1 / BETA) * math.log(resistenza / R0)
    return 1 / inverso_T - 273.15


def leggi_luce():
    """Restituisce la luce come numero grezzo 0-65535."""
    return ldr.read_u16()
```

Ogni funzione fa una cosa e restituisce un valore. **Non stampa niente, non
accende niente.** Questo le rende facili da provare: le chiami dalla REPL e
guardi cosa tornano.

### Decidere

```python
def aggiorna_stato(temperatura, manuale):
    """Decide il nuovo stato. Non tocca l'hardware."""
    global stato

    if manuale:
        return                      # in manuale comanda l'utente

    if temperatura > TEMP_ALLARME:
        stato = "allarme"
    elif stato == "chiusa" and temperatura > TEMP_APRI:
        stato = "aperta"
    elif stato == "aperta" and temperatura < TEMP_CHIUDI:
        stato = "chiusa"
    elif stato == "allarme" and temperatura < TEMP_ALLARME - 2:
        stato = "aperta"            # isteresi anche sull'allarme
```

Qui c'e' tutta la logica del progetto, in dodici righe leggibili. Nota che le
condizioni guardano **sia la temperatura sia lo stato attuale**: e' quello che
crea l'isteresi e impedisce l'oscillazione.

### Agire

```python
def applica_stato():
    """Comanda l'hardware in base allo stato. Non decide niente."""
    if stato == "chiusa":
        servo_vai_a(0)
        led_rosso.value(0)
        buzzer.duty_u16(0)
    elif stato == "aperta":
        servo_vai_a(90)
        led_rosso.value(1)
        buzzer.duty_u16(0)
    elif stato == "allarme":
        servo_vai_a(180)
        led_rosso.toggle()          # lampeggia
        buzzer.freq(880)
        buzzer.duty_u16(20000)
```

Ogni stato ha il suo blocco. Se domani aggiungi uno stato "notte", aggiungi un
`elif` qui e uno in `aggiorna_stato()`, e hai finito. Il resto del programma
non si tocca.

### Il ciclo principale

```python
while True:
    # 1. LEGGI
    temperatura = leggi_temperatura()
    luce = leggi_luce()
    controlla_pulsanti()

    # 2. DECIDI
    aggiorna_stato(temperatura, modo_manuale)

    # 3. AGISCI
    applica_stato()
    led_bianco.value(1 if luce < SOGLIA_BUIO else 0)

    # 4. MOSTRA
    aggiorna_display(temperatura, luce)

    time.sleep(0.1)
```

Dodici righe. **E resterebbero dodici anche con il triplo dei sensori**, perche'
la complessita' sta dentro le funzioni, non qui.

Quando avrai a che fare con programmi veri, questa e' la differenza tra codice
che si puo' far crescere e codice che a un certo punto va buttato.

## Far partire tutto da solo

Quando funziona, caricalo sul Pico col nome **`main.py`** (guida 09, comando
**Upload project to Pico**).

Da quel momento stacchi il PC, colleghi il Pico a un caricabatterie da telefono
e la serra funziona da sola. Non e' piu' un esperimento collegato al computer:
e' un oggetto.

> Se poi Thonny o MicroPico non riescono piu' a collegarsi, e' perche' `main.py`
> parte subito e occupa la scheda. Premi `Ctrl+C` nella REPL appena colleghi
> l'USB. Se proprio non ne esci, rifai il BOOTSEL e riflasha il firmware:
> perdi i file sul Pico, ma il codice ce l'hai su GitHub. E' esattamente per
> questo che si usa git.

## Prova a cambiare

1. **Registra i dati.** Salva temperatura e luce in un file sul Pico ogni
   minuto. Poi scaricalo con **Download project from Pico** e fai un grafico
   con Excel.

   ```python
   with open("dati.csv", "a") as f:
       f.write("{},{}\n".format(temperatura, luce))
   ```

   Occhio: la flash del Pico ha un numero finito di scritture. Ogni minuto va
   benissimo, ogni 100 millisecondi no.

2. **Togli tutti gli `sleep`.** Al momento il programma dorme 100 ms per giro,
   e in quel tempo non risponde ai pulsanti. Riscrivilo usando
   `time.ticks_ms()` per fare le cose "quando e' ora" invece di "dopo una
   pausa". E' il passo che separa un programma didattico da uno vero.

3. **Modalita' notte.** Se e' buio da piu' di dieci minuti, ignora la
   temperatura e chiudi comunque. Aggiungi lo stato, aggiungi le due
   transizioni.

4. **Grafico sul display.** Tieni le ultime 16 temperature in una lista e
   disegnale sulla seconda riga del display con i caratteri personalizzati
   della guida 13.

5. **Il PIR.** Nel kit c'e' il sensore di movimento a cupoletta che non abbiamo
   mai usato. Ha tre piedini (`VCC`, `OUT`, `GND`) e l'uscita e' digitale:
   niente ADC, si legge come un pulsante. Fai accendere il LED bianco quando
   passa qualcuno.

## Se non funziona

| Sintomo | Causa | Soluzione |
|---|---|---|
| Niente funziona dopo aver montato tutto | Troppi pezzi insieme | Stacca tutto e rimonta un blocco alla volta, provando |
| Il Pico si riavvia | Servo e display insieme assorbono troppo | Alimenta il servo da una fonte separata, o mettici il condensatore (guida 11) |
| Il display e' pieno di caratteri strani | Interferenza dal servo sui fili dati | Allontana i fili del servo da quelli del display |
| Il servo trema in continuazione | L'ADC balla e lo stato cambia di continuo | Aumenta la distanza tra le due soglie |
| Il buzzer non si spegne piu' | Manca `duty_u16(0)` in uno stato | Controlla tutti i rami di `applica_stato()` |
| `MemoryError` | Il programma e' troppo grande | Togli i commenti lunghi, oppure usa `import gc` e `gc.collect()` |
| Funziona col PC ma non col caricabatterie | Il caricabatterie non da' abbastanza corrente | Provane uno da almeno 1 A |

## Sei arrivato in fondo

Facciamo il conto di cosa sai fare adesso:

- accendere e spegnere cose (guide 04, 05)
- leggere pulsanti e gestire i rimbalzi (06)
- generare segnali PWM per suono, luce e movimento (07, 11)
- leggere grandezze analogiche e convertirle in unita' vere (08, 10)
- usare l'isteresi per sistemi che non oscillano (10)
- pilotare un protocollo di comunicazione (12, 13)
- usare una libreria e scriverne una (13)
- strutturare un programma lungo con una macchina a stati (14)
- usare un IDE professionale e git (09)

E' piu' o meno il programma di un intero corso di sistemi, fatto con un
microcontrollore da 5 euro.

## E adesso?

Qualche direzione, se ti e' piaciuto:

- **Il Pico W** costa due euro in piu' e ha il WiFi. Da li' si aprono i
  progetti collegati a Internet: mandare la temperatura a un server, comandare
  la serra dal telefono.
- **Il secondo core.** Il Pico ne ha due e finora ne hai usato uno. Cerca
  `_thread` in MicroPython.
- **Il PIO**, quello che fa funzionare i NeoPixel. Puoi programmarlo tu, ed e'
  una cosa che pochissimi microcontrollori sanno fare.
- **C/C++ con il Pico SDK.** Lo stesso hardware, senza interprete di mezzo.
  Piu' difficile, molto piu' veloce, ed e' quello che vedrai a scuola.
- **I tuoi progetti.** La cartella
  [`progetti-daniele/`](../progetti-daniele/) e' li' apposta.

Buon divertimento.
