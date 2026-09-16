# 10 - Luce e temperatura

## Obiettivo

Misurare il mondo vero. Due sensori che funzionano allo stesso modo - cambiano
resistenza - e che ti obbligano a capire il **partitore di tensione**, il
circuito piu' usato dell'elettronica.

## Ti serve

- 1 fotoresistenza (LDR), quella tondina con la serpentina
- 1 termistore NTC, la perlina nera o verde
- 2 resistenze da **10 kohm** (marrone-nero-arancione-oro)
- 4 jumper
- Il LED su GP15 con la sua resistenza

## Come funziona

### Sensori che cambiano resistenza

La fotoresistenza e il termistore hanno una cosa in comune: **non producono
tensione, cambiano resistenza**.

| Sensore | Al buio / freddo | Alla luce / caldo |
|---|---|---|
| **LDR** (luce) | ~100 kohm | ~1 kohm |
| **NTC** (temperatura) | ~50 kohm a 0 gradi | ~5 kohm a 50 gradi |

NTC sta per *Negative Temperature Coefficient*: piu' sale la temperatura, piu'
scende la resistenza. Al contrario di quello che verrebbe da pensare.

### Il problema

L'ADC del Pico misura **tensioni**, non resistenze. Quindi non puoi collegargli
direttamente un sensore resistivo: devi prima trasformare la variazione di
resistenza in una variazione di tensione.

Il circuito che fa questo si chiama **partitore di tensione**, e l'hai gia'
usato nella guida 08 senza accorgertene: il potenziometro **e'** un partitore.

### Il partitore di tensione

Due resistenze in serie tra 3,3V e massa. Nel punto in mezzo c'e' una tensione
che dipende dal rapporto tra le due.

```
       3,3V
        |
       [R1]   <- il sensore (LDR o NTC)
        |
        +----> al pin ADC    (qui misuri)
        |
       [R2]   <- resistenza fissa, 10 kohm
        |
       GND
```

La formula:

```
V_uscita = 3,3 x R2 / (R1 + R2)
```

Facciamo due conti con la LDR:

- **Al buio**, LDR = 100 kohm: `V = 3,3 x 10 / (100 + 10) = 0,30 V` → ADC basso
- **Alla luce**, LDR = 1 kohm: `V = 3,3 x 10 / (1 + 10) = 3,0 V` → ADC alto

Quindi piu' luce, piu' alto il numero. Intuitivo.

> **Perche' proprio 10 kohm?** Perche' un partitore e' piu' sensibile quando la
> resistenza fissa e' nell'ordine di grandezza di quella variabile. Con 100 ohm
> o con 1 Mohm il segnale si schiaccerebbe a un estremo e leggeresti quasi
> sempre lo stesso numero.

## Collegamenti - la fotoresistenza

**Stacca l'USB.**

| # | Da | A |
|---|---|---|
| 1 | **LDR**, un piedino | pista `+` rossa (3,3V) |
| 2 | **LDR**, altro piedino | riga 50 |
| 3 | **resistenza 10k**, una zampa | riga 50 (stessa della LDR) |
| 4 | **resistenza 10k**, altra zampa | pista `-` blu (massa) |
| 5 | riga 50 | riga del **GP26** (pin fisico 31) |

```
  pista rossa (+) --- [ LDR ] --- riga50 --- [ 10k ] --- pista blu (-)
                                    |
                                    +---[filo]--- GP26
```

La LDR non ha polarita': puoi montarla in qualunque verso.

## Il codice - luce

```python
# 10a-luce.py - misura la luce ambientale

from machine import ADC, Pin
import time

ldr = ADC(Pin(26))

while True:
    valore = ldr.read_u16()
    print("Luce:", valore)
    time.sleep(0.3)
```

Esegui, poi fai tre prove:

1. Lascia stare, e guarda il valore a riposo
2. **Copri la LDR con un dito**: il numero crolla
3. **Puntaci sopra la torcia del telefono**: il numero schizza in alto

Segnati i tre numeri, ti servono subito.

### Il lampione automatico

```python
# 10b-lampione.py - accende il LED quando c'e' buio

from machine import ADC, Pin
import time

ldr = ADC(Pin(26))
led = Pin(15, Pin.OUT)

SOGLIA = 20000       # <- metti qui il TUO numero (vedi sotto)

while True:
    luce = ldr.read_u16()
    if luce < SOGLIA:
        led.value(1)      # buio: accendi
    else:
        led.value(0)      # c'e' luce: spegni
    print(luce)
    time.sleep(0.1)
```

**La soglia devi tararla tu**, con i numeri che hai segnato prima. Prendi il
valore con il dito sopra e quello a luce normale, e metti `SOGLIA` a meta'
strada.

Questo e' un punto importante e vale oltre questo esercizio: **un sensore va
sempre tarato nell'ambiente dove lavora**. Il valore che funziona in camera tua
di giorno non funziona la sera, e non funziona a casa di un altro. Nessun
numero magico copiato da Internet ti salva: devi misurare.

### Il problema dell'oscillazione

Metti il dito sopra la LDR lentamente, fino a farti trovare esattamente sulla
soglia. Il LED impazzisce: acceso-spento-acceso-spento decine di volte al
secondo.

Succede perche' il valore balla di qualche centinaio di unita' per il rumore, e
se sei proprio sul confine ogni lettura cade da una parte diversa.

La soluzione si chiama **isteresi**: usi **due** soglie invece di una.

```python
# 10c-isteresi.py - lampione che non sfarfalla

from machine import ADC, Pin
import time

ldr = ADC(Pin(26))
led = Pin(15, Pin.OUT)

SOGLIA_ACCENDI = 18000    # sotto questo, accendi
SOGLIA_SPEGNI  = 25000    # sopra questo, spegni
# tra i due valori: non cambiare niente

acceso = False

while True:
    luce = ldr.read_u16()
    if not acceso and luce < SOGLIA_ACCENDI:
        acceso = True
    elif acceso and luce > SOGLIA_SPEGNI:
        acceso = False
    led.value(1 if acceso else 0)
    time.sleep(0.05)
```

Tra 18000 e 25000 c'e' una **zona morta** dove il sistema tiene lo stato che
ha. Per farlo cambiare devi superare il confine per bene, non sfiorarlo.

E' lo stesso principio del termostato di casa: accende a 19 gradi e spegne a
21, non accende e spegne di continuo a 20.

## Collegamenti - il termistore

Adesso il secondo sensore, su GP27. Il partitore e' identico.

| # | Da | A |
|---|---|---|
| 1 | **NTC**, un piedino | pista `+` rossa (3,3V) |
| 2 | **NTC**, altro piedino | riga 55 |
| 3 | **resistenza 10k**, una zampa | riga 55 |
| 4 | **resistenza 10k**, altra zampa | pista `-` blu (massa) |
| 5 | riga 55 | riga del **GP27** (pin fisico 32) |

## Il codice - temperatura

### Prima, i numeri grezzi

```python
# 10d-ntc-grezzo.py - lettura grezza del termistore

from machine import ADC, Pin
import time

ntc = ADC(Pin(27))

while True:
    print(ntc.read_u16())
    time.sleep(0.5)
```

Stringi la perlina tra le dita: il numero cambia. Sta funzionando, ma quel
numero non e' una temperatura.

### Da numero a gradi

Qui serve un po' di matematica. La relazione tra resistenza e temperatura di un
NTC non e' una retta, e si approssima con la **formula di Steinhart-Hart
semplificata**, detta equazione Beta:

```
1/T = 1/T0 + (1/B) x ln(R/R0)
```

dove `T0` = 298,15 K (cioe' 25 gradi), `R0` = resistenza a 25 gradi (10 kohm) e
`B` = un parametro del componente, tipicamente 3950.

```python
# 10e-temperatura.py - il termistore in gradi centigradi

from machine import ADC, Pin
import time
import math

ntc = ADC(Pin(27))

R_FISSA = 10000       # la resistenza da 10k del partitore
R0 = 10000            # resistenza dell'NTC a 25 gradi
T0 = 298.15           # 25 gradi espressi in kelvin
BETA = 3950           # parametro del componente

while True:
    lettura = ntc.read_u16()

    # 1. dal numero dell'ADC risali alla tensione
    tensione = lettura * 3.3 / 65535

    # 2. dalla tensione risali alla resistenza dell'NTC
    #    (invertendo la formula del partitore)
    resistenza = R_FISSA * (3.3 - tensione) / tensione

    # 3. dalla resistenza risali alla temperatura (equazione Beta)
    inverso_T = 1 / T0 + (1 / BETA) * math.log(resistenza / R0)
    kelvin = 1 / inverso_T
    celsius = kelvin - 273.15

    print(round(celsius, 1), "gradi  (R =", int(resistenza), "ohm)")
    time.sleep(1)
```

Le tre conversioni in fila - **numero → tensione → resistenza → temperatura** -
sono il cuore della guida. Ogni passaggio annulla una trasformazione fisica,
all'indietro.

> **Non aspettarti precisione da laboratorio.** Se legge 2-3 gradi diversi dal
> termometro di casa e' normale: `BETA` varia da componente a componente, le
> resistenze hanno il 5% di tolleranza e la perlina si scalda da sola. Per
> misurare **variazioni** va benissimo, per misurare **valori assoluti** ci
> vorrebbe una taratura.

## Prova a cambiare

1. **Termometro a LED.** Tre LED: verde sotto i 20 gradi, giallo tra 20 e 25,
   rosso sopra i 25. Scalda l'NTC con le dita e guardali cambiare.

2. **Min e max.** Tieni traccia della temperatura minima e massima viste da
   quando il programma e' partito, e stampale a ogni lettura.

3. **Allarme luce con buzzer.** Rimonta il buzzer della guida 07: quando
   qualcuno copre la LDR con la mano (la luce crolla di colpo), suona. Un
   antifurto per la scatola dei biscotti.

4. **Media mobile.** Le letture ballano. Tieni le ultime 10 in una lista e
   stampa la media:

   ```python
   letture = []
   # nel ciclo:
   letture.append(ntc.read_u16())
   if len(letture) > 10:
       letture.pop(0)
   media = sum(letture) / len(letture)
   ```

   Confronta quanto e' piu' stabile del valore singolo.

5. **Il sensore di fiamma.** Nel kit c'e' anche il modulo blu con il LED scuro:
   e' un sensore a infrarossi che rileva le fiamme. Ha un'uscita digitale
   (`DO`) e a volte una analogica (`AO`). Collega `VCC` a 3,3V, `GND` a massa e
   `DO` a un GPIO in ingresso. **Nessun esperimento con fiamme vere senza un
   adulto presente**: per provarlo basta il telecomando della TV, che emette
   infrarossi.

## Se non funziona

| Sintomo | Causa | Soluzione |
|---|---|---|
| Il valore non cambia mai | Il filo ADC e' sul punto sbagliato | Deve stare **in mezzo** alle due resistenze, non agli estremi |
| Valore fisso a ~65535 | Manca la resistenza da 10k verso massa | Controlla il partitore |
| Valore fisso a ~0 | Manca il 3,3V, o il sensore e' interrotto | Controlla la pista rossa |
| Il LED sfarfalla sulla soglia | Nessuna isteresi | Usa `10c` |
| La temperatura e' assurda (tipo 200 gradi) | Sensore e resistenza invertiti nel partitore | Scambiali, oppure cambia segno nella formula |
| La temperatura e' sbagliata di 3-4 gradi | `BETA` non e' esattamente 3950 | Normale. Aggiustalo empiricamente se ti serve preciso. |
| `ValueError: math domain error` | `math.log` di un numero negativo o zero | La tensione letta e' 0 o 3,3: il partitore non e' collegato bene |

## Prossima guida

[11 - Il servomotore](11-servomotore.md): dopo aver sentito il mondo, muoviamo
qualcosa.
