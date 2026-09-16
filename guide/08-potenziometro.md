# 08 - Il potenziometro

## Obiettivo

Leggere un valore che non e' ne' acceso ne' spento, ma una via di mezzo.
Finisce qui la prima parte del percorso: dopo questa guida hai in mano input
digitale, output digitale, PWM e input analogico, cioe' i quattro mattoni con
cui si costruisce tutto il resto.

## Ti serve

- 1 potenziometro (la manopolina blu con 3 piedini)
- 3 jumper
- Il LED su GP15 con la resistenza

## Come funziona

### Digitale contro analogico

Il pulsante della guida 06 era **digitale**: premuto o non premuto, `0` o `1`,
niente in mezzo.

Il mondo vero pero' non e' cosi'. La luce non e' accesa o spenta, e' piu' o meno
intensa. La temperatura non e' calda o fredda. Queste grandezze si chiamano
**analogiche**, e per leggerle serve qualcosa che traduca una tensione in un
numero.

Quel qualcosa si chiama **ADC** (*Analog to Digital Converter*), ed e' dentro
il Pico.

### L'ADC del Pico

Solo **tre pin** sanno leggere valori analogici:

| Pin GP | Pin fisico | Canale ADC |
|---|---|---|
| GP26 | 31 | ADC0 |
| GP27 | 32 | ADC1 |
| GP28 | 34 | ADC2 |

(Ce n'e' un quarto, ADC4, collegato a un sensore di temperatura dentro il chip.
Ci giochiamo negli esercizi.)

L'ADC misura una tensione tra **0V e 3,3V** e la traduce in un numero. In
MicroPython si legge con `read_u16()`, che restituisce un valore da `0` a
`65535`:

| Tensione sul pin | `read_u16()` |
|---|---|
| 0 V | ~0 |
| 0,825 V | ~16000 |
| 1,65 V | ~32768 |
| 3,3 V | ~65535 |

> Curiosita' tecnica: l'ADC del Pico e' in realta' a **12 bit**, quindi legge
> 4096 livelli distinti. MicroPython moltiplica il risultato per 16 in modo che
> tutte le schede parlino la stessa scala 0-65535. Vuol dire che i valori
> saltano di 16 in 16: non e' un difetto, e' la risoluzione vera del
> convertitore.

### Il potenziometro e' un partitore di tensione

Il potenziometro ha tre piedini e dentro c'e' una pista resistiva con un
cursore che scorre, comandato dalla manopola.

```
   3,3V ----[=========|=========]---- GND
            ^         ^
            |         |
        piedino 1   cursore      piedino 3
                  (piedino 2)
                       |
                       v
                  al pin GP26
```

Collegando i due estremi a 3,3V e massa, il piedino centrale ti da' una
tensione che varia con continuita' tra 0 e 3,3V a seconda di dove hai girato la
manopola.

Questa configurazione si chiama **partitore di tensione**, e la ritrovi
identica nella guida 10 con la fotoresistenza. Vale la pena averla capita qui,
dove e' semplice.

## Collegamenti

**Stacca l'USB.**

Il potenziometro si monta con i tre piedini in tre righe consecutive.

| # | Da | A |
|---|---|---|
| 1 | **potenziometro**, 3 piedini | tre righe consecutive, es. 45, 46, 47 |
| 2 | riga 45 (piedino laterale) | pista `+` rossa (3,3V) |
| 3 | riga 46 (piedino **centrale**) | riga del **GP26** (pin fisico 31) |
| 4 | riga 47 (altro laterale) | pista `-` blu (massa) |

```
  pista rossa (+) ---[filo]--- riga45  \
                                riga46  >  [ POTENZIOMETRO ]
  pista blu (-)   ---[filo]--- riga47  /
                                  |
                               riga46 ---[filo]--- GP26
```

> Il piedino **centrale** e' sempre il cursore. I due laterali sono
> intercambiabili: se li scambi, la manopola gira al contrario. Non e' un
> errore, e' solo scomodo.

## Il codice

### Leggi e basta

```python
# 08a-leggi-pot.py - stampa il valore del potenziometro

from machine import ADC, Pin
import time

pot = ADC(Pin(26))

while True:
    valore = pot.read_u16()
    print(valore)
    time.sleep(0.2)
```

Esegui e gira la manopola guardando la Shell. Il numero va da circa 0 a circa
65535.

Nota due cose:

- **Gli estremi non sono esatti.** Probabilmente leggi 200 invece di 0 e 65300
  invece di 65535. Normale: i componenti reali hanno tolleranze, e l'ADC ha un
  po' di rumore. Nessun sensore vero da' numeri perfetti.
- **Il valore balla di qualche unita' anche a manopola ferma.** Anche questo e'
  normale, ed e' il motivo per cui in un progetto serio si fa una media di
  piu' letture.

### Trasformalo in qualcosa di leggibile

Un numero da 0 a 65535 non dice niente a un essere umano. Convertiamolo in
percentuale:

```python
# 08b-percentuale.py - il potenziometro in percentuale

from machine import ADC, Pin
import time

pot = ADC(Pin(26))

while True:
    valore = pot.read_u16()
    percento = valore * 100 // 65535     # // e' la divisione intera
    print(percento, "%")
    time.sleep(0.2)
```

Questa operazione - prendere un numero in un intervallo e riportarlo in un
altro - si chiama **mappatura**, e la farai continuamente. Vale la pena farsene
una funzione:

```python
def mappa(valore, da_min, da_max, a_min, a_max):
    """Riporta 'valore' dall'intervallo (da_min, da_max) a (a_min, a_max)."""
    proporzione = (valore - da_min) / (da_max - da_min)
    return a_min + proporzione * (a_max - a_min)
```

Cosi' `mappa(32768, 0, 65535, 0, 180)` ti da' 90, che e' esattamente quello che
ti servira' nella guida 11 per il servo.

### Il potenziometro comanda il LED

Adesso uniamo tutto: PWM della guida 07 piu' ADC di questa.

```python
# 08c-pot-led.py - la manopola regola la luminosita' del LED

from machine import ADC, Pin, PWM
import time

pot = ADC(Pin(26))
led = PWM(Pin(15))
led.freq(1000)          # 1000 Hz: abbastanza veloce da non vedere sfarfallio

while True:
    valore = pot.read_u16()
    led.duty_u16(valore)      # la lettura va dritta nel duty: stessa scala!
    time.sleep(0.02)
```

Il bello e' la riga `led.duty_u16(valore)`: sia `read_u16()` che `duty_u16()`
lavorano sulla scala 0-65535, quindi il valore passa **senza nessuna
conversione**. Non e' un caso, e' proprio per questo che MicroPython ha scelto
quella scala.

Gira la manopola e guarda il LED. Hai costruito un dimmer.

### Il potenziometro comanda il buzzer

```python
# 08d-pot-buzzer.py - la manopola cambia la nota

from machine import ADC, Pin, PWM
import time

pot = ADC(Pin(26))
buzzer = PWM(Pin(18))
buzzer.duty_u16(32768)

while True:
    valore = pot.read_u16()
    frequenza = 100 + (valore * 1900 // 65535)    # da 100 a 2000 Hz
    buzzer.freq(frequenza)
    time.sleep(0.02)
```

Un theremin. Fai attenzione alle orecchie di chi ti sta intorno.

## Prova a cambiare

1. **Barra di livello.** Stampa una barra testuale che cresce con la manopola:

   ```python
   quadretti = valore * 20 // 65535
   print("[" + "#" * quadretti + "-" * (20 - quadretti) + "]")
   ```

2. **Smorza il rumore.** Fai la media di 10 letture invece di prenderne una
   sola, e guarda quanto si stabilizza il numero:

   ```python
   somma = 0
   for i in range(10):
       somma = somma + pot.read_u16()
   media = somma // 10
   ```

3. **Il termometro nascosto.** Il Pico ha un sensore di temperatura dentro il
   chip, sul canale ADC 4. Provalo:

   ```python
   from machine import ADC
   import time

   sensore = ADC(4)

   while True:
       lettura = sensore.read_u16() * 3.3 / 65535
       temperatura = 27 - (lettura - 0.706) / 0.001721
       print(round(temperatura, 1), "gradi")
       time.sleep(1)
   ```

   Quella formula viene dal manuale dell'RP2040. Misura la temperatura **del
   chip**, non della stanza, quindi legge qualche grado in piu'. Prova a
   tenere un dito sul chip e guarda il numero salire.

## Se non funziona

| Sintomo | Causa | Soluzione |
|---|---|---|
| Il valore non cambia girando la manopola | Hai collegato GP26 a un piedino laterale | Il filo del segnale va sul piedino **centrale** |
| Il valore resta a 0 | Manca il 3,3V su un estremo | Controlla che la pista rossa sia collegata al pin 36 |
| Il valore resta a 65535 | Manca la massa sull'altro estremo | Controlla la pista blu |
| Salta tra 0 e 65535 senza vie di mezzo | Stai leggendo un pin non-ADC | Solo GP26, GP27, GP28 hanno l'ADC |
| `ValueError: invalid pin` | Hai scritto `ADC(Pin(15))` o simile | Vedi sopra |
| Il valore balla di 200-300 unita' | Rumore, o alimentazione USB sporca | Fai la media (esercizio 2). E' normale. |
| Il LED sfarfalla visibilmente | Frequenza PWM troppo bassa | Mettila a 1000 Hz |

## Fine della prima parte

A questo punto sai fare quattro cose, e con quelle quattro si costruisce
qualunque progetto di questo kit:

| | Digitale | Analogico |
|---|---|---|
| **Output** | `Pin.OUT`, `value()` | `PWM`, `duty_u16()` |
| **Input** | `Pin.IN`, `value()` | `ADC`, `read_u16()` |

Tutto quello che viene dopo e' una variazione su questi quattro.

## Prossima guida

[09 - Da Thonny a Cursor](09-da-thonny-a-cursor.md): cambiamo strumenti.
