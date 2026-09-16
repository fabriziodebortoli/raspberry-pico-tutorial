# Codice pronto

Qui c'e' il programma finito di ogni guida.

**Usalo per confrontare, non per copiare.** Se copi prima di aver provato a
scriverlo, hai perso il pomeriggio e non hai imparato niente: il codice
funzionera' e tu non saprai perche'.

Il modo giusto di usare questa cartella:

1. Leggi la guida
2. Scrivi il codice tu, guardando solo gli esempi dentro la guida
3. Se non funziona, prova a capire perche'
4. **Poi** apri il file qui dentro e confronta

## Cosa c'e'

| Cartella | Guida | File |
|---|---|---|
| `04-led-interno/` | 04 | `blink.py`, `sos.py` |
| `05-led-esterno/` | 05 | `led-esterno.py`, `semaforo.py` |
| `06-pulsante/` | 06 | `pulsante-led.py`, `conta-debounce.py`, `interruttore.py` |
| `07-buzzer/` | 07 | `scala.py`, `melodia.py`, `spegni-buzzer.py` |
| `08-potenziometro/` | 08 | `leggi-pot.py`, `dimmer.py`, `temperatura-chip.py` |
| `10-sensori/` | 10 | `leggi-luce.py`, `lampione.py`, `temperatura.py` |
| `11-servo/` | 11 | `servo-angolo.py`, `servo-pot.py` |
| `12-neopixel/` | 12 | `arcobaleno.py`, `corsa.py`, `spegni-tutto.py` |
| `13-display/` | 13 | `lcd1602.py` (libreria), `ciao.py`, `cronometro.py`, `termometro.py` |
| `14-serra/` | 14 | `serra.py` (il progetto finale) |

## Attenzione a due cose

**`lcd1602.py` e' una libreria, non un programma.** Va **caricata sul Pico**
(non solo eseguita) prima di usare qualsiasi programma che scrive sul display.
Con MicroPico: apri il file e fai **Upload current file to Pico**.

**I file `spegni-*.py` servono per le emergenze.** Quando il buzzer resta
acceso o i NeoPixel restano illuminati, esegui quelli e tornano a posto.

## I pin usati

Tutti i programmi seguono lo schema di [pinout.md](../riferimenti/pinout.md),
quindi puoi lasciare il circuito montato e passare da un programma all'altro
senza rifare i collegamenti.
