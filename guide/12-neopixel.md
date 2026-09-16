# 12 - I LED NeoPixel

## Obiettivo

Comandare individualmente una fila di LED colorati usando **un filo solo**.
Dietro c'e' un'idea che vale piu' dell'effetto scenico: un protocollo di
comunicazione.

## Ti serve

- 1 striscia NeoPixel (la strisce nera con i quadratini bianchi)
- 3 jumper
- Il potenziometro su GP26, per gli esercizi

## Come funziona

### Perche' un filo solo

Nella guida 05 hai acceso un LED con un pin. Con otto LED serviranno otto pin,
otto resistenze, sedici fili. Con sessanta LED non basterebbe il Pico.

I NeoPixel risolvono il problema in modo elegante: **ogni LED ha dentro un
piccolo chip**. Non sono LED, sono LED piu' controller.

I chip sono collegati in catena. Tu mandi tutti i colori sul primo, lui si
tiene il suo e passa il resto al secondo, che si tiene il suo e passa avanti, e
cosi' via.

```
   GP17 --> [LED 0] --> [LED 1] --> [LED 2] --> [LED 3] --> ...
            tiene il    tiene il    tiene il
            1o colore   2o colore   3o colore
            passa il    passa il    passa il
            resto       resto       resto
```

Il modello si chiama **WS2812B**, ma li chiamano tutti NeoPixel perche' e' il
nome che gli ha dato Adafruit.

### Il protocollo, e perche' e' difficile

Su quel filo i bit si distinguono per la **durata dell'impulso**:

- un **bit 0** e' un impulso alto di circa **0,4 microsecondi**
- un **bit 1** e' un impulso alto di circa **0,8 microsecondi**
- se il filo resta basso per piu' di **50 microsecondi**, i LED capiscono che i
  dati sono finiti e accendono

Fermati un attimo a pensare a quei numeri. **0,4 microsecondi** sono 400
nanosecondi. Il Pico gira a 133 MHz, quindi un ciclo di clock dura circa 7,5
nanosecondi: hai una cinquantina di istruzioni macchina per generare un
singolo bit.

In MicroPython, dove ogni riga passa per un interprete, **e' impossibile**.

La cosa bella e' che qualcuno ha gia' risolto il problema per te. L'RP2040 ha
un pezzo di hardware dedicato che si chiama **PIO** (*Programmable
Input/Output*): sono piccole macchine a stati indipendenti dai core, fatte
apposta per generare segnali con tempi precisi.

Tu scrivi `np.write()` e sotto il cofano il PIO fa il lavoro sporco. **Ma vale
la pena sapere che c'e'**, perche' spiega perche' funziona una cosa che a rigor
di logica non dovrebbe.

### I colori

Ogni LED contiene tre LED minuscoli: rosso, verde, blu. Mescolandoli ottieni
qualunque colore. Ogni componente va da 0 a 255, e si esprime come una **tupla**
di tre numeri:

| Colore | Tupla |
|---|---|
| Rosso | `(255, 0, 0)` |
| Verde | `(0, 255, 0)` |
| Blu | `(0, 0, 255)` |
| Giallo | `(255, 255, 0)` |
| Ciano | `(0, 255, 255)` |
| Magenta | `(255, 0, 255)` |
| Bianco | `(255, 255, 255)` |
| Spento | `(0, 0, 0)` |
| Arancione | `(255, 100, 0)` |

## Collegamenti

**Stacca l'USB.**

La striscia ha tre contatti, marcati sul retro. Cerca le scritte:

| Contatto | Dove va |
|---|---|
| **5V** (o `VCC`, `+5V`) | pista 5V (da VBUS, come nella guida 11) |
| **GND** | pista `-` blu |
| **DIN** (o `DI`, `Data In`) | GP17 |

**Il verso conta.** La striscia ha un ingresso (`DIN`) e un'uscita (`DOUT`), e
spesso ci sono delle frecce stampate che indicano il senso dei dati. Il Pico va
collegato dal lato **`DIN`**. Se lo colleghi dall'altra parte non succede
niente di rotto, semplicemente non si accende nulla.

| # | Da | A |
|---|---|---|
| 1 | striscia **5V** | pista `+` a 5V (VBUS) |
| 2 | striscia **GND** | pista `-` blu |
| 3 | striscia **DIN** | riga del **GP17** (pin fisico 22) |

> **Una nota sulla corrente.** Ogni LED a bianco pieno assorbe circa 60 mA. Con
> 8 LED tutti bianchi al massimo fanno mezzo ampere, e la porta USB inizia a
> soffrire. Nelle guide teniamo la luminosita' bassa: **non e' per delicatezza,
> e' perche' altrimenti il Pico si riavvia.**

## Il codice

### Accendine uno

```python
# 12a-neopixel-base.py - accende il primo LED di rosso

from machine import Pin
import neopixel
import time

NUM_LED = 8                            # quanti ne ha la tua striscia
np = neopixel.NeoPixel(Pin(17), NUM_LED)

np[0] = (30, 0, 0)     # primo LED, rosso tenue
np.write()             # <-- senza questa riga non succede NIENTE

time.sleep(2)

np[0] = (0, 0, 0)
np.write()
```

**`np.write()` e' la riga che conta.** Assegnare `np[0] = (30, 0, 0)` cambia
solo un valore nella memoria del Pico: e' `write()` che manda tutto sul filo.

E' un errore che farai almeno una volta: cambi i colori, non succede niente,
e ci metti dieci minuti a capire che manca `write()`.

> Nota sulla luminosita': `(30, 0, 0)` invece di `(255, 0, 0)`. Questi LED a
> pieno regime sono davvero fastidiosi da guardare da vicino, oltre che
> assetati di corrente. Per provare, 20-50 basta e avanza.

### Accendili tutti

```python
# 12b-arcobaleno.py - ogni LED di un colore diverso

from machine import Pin
import neopixel
import time

NUM_LED = 8
np = neopixel.NeoPixel(Pin(17), NUM_LED)

colori = [
    (30, 0, 0),      # rosso
    (30, 15, 0),     # arancione
    (30, 30, 0),     # giallo
    (0, 30, 0),      # verde
    (0, 30, 30),     # ciano
    (0, 0, 30),      # blu
    (15, 0, 30),     # viola
    (30, 0, 30),     # magenta
]

for i in range(NUM_LED):
    np[i] = colori[i]

np.write()      # una sola write per tutti e otto
```

Nota che `write()` si chiama **una volta sola**, alla fine. Prepari tutta
l'immagine e poi la mandi, come si fa con la grafica.

### Un LED che corre

```python
# 12c-corsa.py - un puntino luminoso che scorre avanti e indietro

from machine import Pin
import neopixel
import time

NUM_LED = 8
np = neopixel.NeoPixel(Pin(17), NUM_LED)

def spegni_tutti():
    for i in range(NUM_LED):
        np[i] = (0, 0, 0)

while True:
    for posizione in range(NUM_LED):
        spegni_tutti()
        np[posizione] = (0, 30, 0)
        np.write()
        time.sleep(0.08)
    for posizione in range(NUM_LED - 2, 0, -1):
        spegni_tutti()
        np[posizione] = (0, 30, 0)
        np.write()
        time.sleep(0.08)
```

Se hai riconosciuto l'effetto della macchina di Supercar, hai visto abbastanza
TV vecchia.

### La ruota dei colori

```python
# 12d-ruota.py - arcobaleno che scorre

from machine import Pin
import neopixel
import time

NUM_LED = 8
np = neopixel.NeoPixel(Pin(17), NUM_LED)

def ruota(posizione):
    """Da un numero 0-255 restituisce un colore dell'arcobaleno."""
    posizione = posizione % 255
    if posizione < 85:
        return (255 - posizione * 3, posizione * 3, 0)
    elif posizione < 170:
        posizione = posizione - 85
        return (0, 255 - posizione * 3, posizione * 3)
    else:
        posizione = posizione - 170
        return (posizione * 3, 0, 255 - posizione * 3)

def attenua(colore, fattore):
    """Riduce la luminosita' di un colore. fattore da 0.0 a 1.0"""
    r, g, b = colore
    return (int(r * fattore), int(g * fattore), int(b * fattore))

offset = 0
while True:
    for i in range(NUM_LED):
        colore = ruota(i * 255 // NUM_LED + offset)
        np[i] = attenua(colore, 0.12)      # al 12% della luminosita'
    np.write()
    offset = offset + 3
    time.sleep(0.03)
```

La funzione `ruota()` percorre lo spettro dei colori spostandosi lungo tre
tratti: da rosso a verde, da verde a blu, da blu a rosso. E' un modo grezzo ma
efficace di attraversare la tonalita' senza usare matematica complicata.

Guarda anche `attenua()`: separare "quale colore" da "quanto luminoso" e' una
buona idea, perche' ti permette di cambiare la luminosita' di tutto senza
riscrivere ogni tupla.

## Prova a cambiare

1. **Barra di livello.** Il potenziometro decide quanti LED sono accesi, da 0 a
   8. Un VU-meter.

2. **Termometro colorato.** Con l'NTC della guida 10: blu quando e' freddo,
   rosso quando e' caldo, e i colori in mezzo per le temperature intermedie.

3. **Respiro.** Tutti i LED dello stesso colore, con la luminosita' che sale e
   scende dolcemente. Suggerimento: usa `math.sin()` per avere un andamento
   morbido invece che lineare.

4. **Il fuoco.** Ogni LED sul rosso-arancione con una componente casuale che
   cambia a ogni ciclo. Usa `random.randint(0, 20)` e guarda quanto sembra
   davvero una fiamma con pochissime righe.

5. **Conta quanti LED hai.** Se `NUM_LED` e' sbagliato in eccesso non succede
   niente di male (i comandi in piu' cadono nel vuoto), se e' sbagliato in
   difetto gli ultimi LED restano spenti. Trova il numero giusto per tentativi.

## Se non funziona

| Sintomo | Causa | Soluzione |
|---|---|---|
| Non si accende niente | Manca `np.write()` | E' la causa piu' comune in assoluto |
| Non si accende niente | Filo su `DOUT` invece che su `DIN` | Guarda le frecce sulla striscia e girala |
| Non si accende niente | Manca l'alimentazione a 5V | Il `5V` della striscia va su **VBUS**, non su 3V3 |
| Il primo LED si accende, gli altri no | `NUM_LED` troppo basso | Alzalo |
| I colori sono sbagliati (rosso e verde scambiati) | Alcune strisce usano l'ordine GRB | Scambia i primi due valori delle tuple |
| Lampeggiano a caso | Segnale disturbato | Accorcia i fili. Il segnale e' velocissimo e i fili lunghi lo rovinano. |
| Il Pico si riavvia | Assorbimento eccessivo | Abbassa la luminosita'. Non superare 50 su 255. |
| `ImportError: no module named 'neopixel'` | Firmware vecchio | Riflasha MicroPython con una versione recente (guida 03) |

### Se funzionano solo a meta'

Un problema noto: i WS2812 sono progettati per un segnale dati a 5V, e il Pico
ne manda 3,3. Di solito funziona lo stesso, ma se hai comportamenti erratici -
il primo LED sbaglia colore, gli altri vanno bene - e' quello il motivo.

Il rimedio da elettronici e' un traslatore di livello. Il rimedio da smanettoni
e' alimentare la striscia a 3,3V invece che a 5V: sono meno luminosi, ma il
segnale e' della stessa ampiezza dell'alimentazione e tutto torna a posto.
Provalo se ti capita.

## Prossima guida

[13 - Il display LCD](13-display-lcd.md). Ti avviso: e' la piu' difficile del
percorso. Arrivaci con calma e quando hai tempo.
