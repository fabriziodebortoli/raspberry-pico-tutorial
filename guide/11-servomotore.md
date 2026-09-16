# 11 - Il servomotore

## Obiettivo

Muovere qualcosa nel mondo fisico e portarlo in una posizione precisa. E'
diverso da accendere un LED: qui c'e' un motore che spinge, e le cose si
muovono davvero.

## Ti serve

- 1 servomotore SG90 (il cubetto blu)
- 3 jumper
- Il potenziometro su GP26 della guida 08, per l'esercizio 1

## Come funziona

### Un servo non e' un motore normale

Un motore normale gira finche' gli dai corrente, e tu non sai dov'e' arrivato.

Un **servomotore** e' diverso: gli dici **a quale angolo** vuole stare, e ci va
da solo. Dentro c'e' un motorino, una serie di ingranaggi di riduzione e un
potenziometro che misura la posizione dell'albero. Un circuito confronta di
continuo dove sta con dove dovrebbe stare, e corregge.

E' un **anello di retroazione**, uno dei concetti centrali dell'automazione.

L'SG90 si muove tra **0 e 180 gradi**, non oltre. Non e' fatto per girare.

### Come si comanda: PWM di nuovo

Il servo si comanda con un segnale PWM, ma lo usa in modo diverso dal buzzer.

Qui la **frequenza e' fissa a 50 Hz** (un impulso ogni 20 millisecondi), e
l'informazione sta tutta nella **durata dell'impulso**:

| Durata impulso | Angolo |
|---|---|
| 0,5 ms | 0 gradi |
| 1,5 ms | 90 gradi (centro) |
| 2,5 ms | 180 gradi |

```
  0 gradi     _                    _
             | |                  | |
           __| |__________________| |____
             0,5ms      20 ms

  90 gradi    ___                  ___
             |   |                |   |
           __|   |________________|   |__
             1,5ms

  180 gradi   _____                _____
             |     |              |     |
           __|     |______________|     |__
             2,5ms
```

Nota bene: **la frequenza non cambia mai**. Cambia solo quanto e' largo
l'impulso dentro i 20 millisecondi. E' esattamente il "duty cycle" della guida
07, visto da un'altra angolazione.

### Calcolare il duty

Servono due modi, tutti e due utili.

**Modo 1, con `duty_ns()`** - si dichiara direttamente la durata in nanosecondi:

```python
servo.duty_ns(1_500_000)    # 1,5 ms = 1.500.000 ns = 90 gradi
```

E' il modo piu' leggibile: il numero che scrivi e' la cosa che ti interessa.

**Modo 2, con `duty_u16()`** - devi convertire:

Il periodo e' 20 ms. Se l'impulso deve durare 1,5 ms, la frazione e'
`1,5 / 20 = 0,075`, cioe' il 7,5%. Su scala 65535:

```
0,075 x 65535 = 4915
```

| Angolo | ms | duty_u16 |
|---|---|---|
| 0 | 0,5 | 1638 |
| 90 | 1,5 | 4915 |
| 180 | 2,5 | 8192 |

Useremo `duty_ns()` perche' e' piu' chiaro, ma trovi `duty_u16()` in quasi
tutti i tutorial online, quindi meglio saperlo leggere.

## Collegamenti

**Stacca l'USB.** Qui e' importante piu' del solito.

Il servo ha tre fili con un connettore. I colori sono quasi sempre questi:

| Colore | Cos'e' | Dove va |
|---|---|---|
| **Marrone** (o nero) | massa | pista `-` blu |
| **Rosso** | alimentazione **5V** | pista `+` **rossa collegata a VBUS** |
| **Arancione** (o giallo) | segnale | GP16 |

**ATTENZIONE, leggi questa parte due volte.**

Il servo va alimentato a **5 volt**, non a 3,3. I 5V sul Pico stanno sul pin
**VBUS** (pin fisico 40), che porta la tensione che arriva dall'USB.

Il **segnale** invece resta a 3,3V, e va bene cosi': l'SG90 riconosce
tranquillamente impulsi a 3,3V.

**Non collegare mai il filo rosso del servo a un pin GPIO, e non collegare mai
VBUS a un GPIO.** Se il 5V finisce su un piedino GPIO, il Pico si danneggia.

Visto che finora la pista rossa della breadboard era a 3,3V, ti conviene
**usare l'altra coppia di piste**, quella sul bordo opposto, per i 5V. Cosi'
non rischi di confonderti.

| # | Da | A |
|---|---|---|
| 1 | riga di **VBUS** (pin fisico 40) | pista `+` rossa del **bordo opposto** |
| 2 | riga di un **GND** | pista `-` blu del bordo opposto |
| 3 | servo **rosso** | pista `+` del bordo opposto (5V) |
| 4 | servo **marrone** | pista `-` del bordo opposto |
| 5 | servo **arancione** | riga del **GP16** (pin fisico 21) |

I fili del servo finiscono in un connettore femmina: ci infili dentro tre
jumper maschio-maschio e poi metti l'altra estremita' nella breadboard.

## Il codice

### Tre posizioni

```python
# 11a-servo-base.py - il servo va in tre posizioni

from machine import Pin, PWM
import time

servo = PWM(Pin(16))
servo.freq(50)              # 50 Hz, fisso, sempre

print("0 gradi")
servo.duty_ns(500_000)      # 0,5 ms
time.sleep(1)

print("90 gradi")
servo.duty_ns(1_500_000)    # 1,5 ms
time.sleep(1)

print("180 gradi")
servo.duty_ns(2_500_000)    # 2,5 ms
time.sleep(1)

print("torno al centro")
servo.duty_ns(1_500_000)
time.sleep(1)

servo.deinit()
```

Il servo scatta nelle tre posizioni. Se senti un ronzio quando e' fermo, e'
normale: sta correggendo continuamente la posizione.

### Una funzione per gli angoli

Scrivere `1_500_000` ogni volta e' scomodo e illeggibile. Facciamoci una
funzione:

```python
# 11b-servo-angolo.py - comanda il servo in gradi

from machine import Pin, PWM
import time

servo = PWM(Pin(16))
servo.freq(50)

def vai_a(gradi):
    """Muove il servo all'angolo indicato, da 0 a 180 gradi."""
    if gradi < 0:
        gradi = 0
    if gradi > 180:
        gradi = 180
    # 0 gradi -> 500000 ns, 180 gradi -> 2500000 ns
    ns = 500_000 + (gradi * 2_000_000 // 180)
    servo.duty_ns(ns)

# Spazzata avanti e indietro
while True:
    for angolo in range(0, 181, 5):
        vai_a(angolo)
        time.sleep(0.02)
    for angolo in range(180, -1, -5):
        vai_a(angolo)
        time.sleep(0.02)
```

Il controllo `if gradi < 0` e `if gradi > 180` si chiama **clamping**, e serve
a proteggere il servo: mandarlo oltre i suoi limiti meccanici lo fa forzare
contro il fine corsa, scalda e a lungo andare spacca gli ingranaggi. Che sono
di plastica.

**Questa e' una differenza importante rispetto al LED**: il software che
comanda un LED sbagliando accende una luce sbagliata. Il software che comanda
un motore sbagliando **rompe delle cose**. Da qui in avanti i controlli sui
limiti non sono pignoleria.

### Il servo segue il potenziometro

```python
# 11c-servo-pot.py - la manopola comanda l'angolo

from machine import ADC, Pin, PWM
import time

pot = ADC(Pin(26))
servo = PWM(Pin(16))
servo.freq(50)

def vai_a(gradi):
    if gradi < 0:
        gradi = 0
    if gradi > 180:
        gradi = 180
    servo.duty_ns(500_000 + (gradi * 2_000_000 // 180))

while True:
    valore = pot.read_u16()
    angolo = valore * 180 // 65535      # mappatura, come nella guida 08
    vai_a(angolo)
    time.sleep(0.02)
```

Gira la manopola e il servo la segue. Questo e' il tuo primo **sistema di
controllo**: un ingresso analogico che comanda un attuatore.

Noterai che il servo trema un po' quando la manopola e' ferma. E' il rumore
dell'ADC che si traduce in micro-movimenti. Prova a smorzarlo con la media
mobile della guida 10.

## Prova a cambiare

1. **Movimento morbido.** Invece di andare direttamente all'angolo richiesto,
   avvicinati di un grado per volta. Il movimento diventa fluido invece che a
   scatti.

2. **Il barometro meccanico.** Unisci la guida 10: il servo indica la
   temperatura su una scala che disegni su un cartoncino. 15 gradi a sinistra,
   30 a destra.

3. **Comandalo col pulsante.** Un pulsante lo manda a 0 gradi, l'altro a 180.
   Come una sbarra di parcheggio.

4. **Misura la zona morta.** Manda il servo a 90 gradi, poi a 91, 92, 93. A che
   punto vedi il movimento? Sotto un certo angolo minimo il servo non reagisce.
   Quanto vale?

5. **Non dargli corrente inutilmente.** Dopo che il servo e' arrivato in
   posizione, chiama `servo.duty_ns(0)`. Smette di tenere la posizione e smette
   di ronzare e consumare. Provalo: cambia qualcosa se spingi l'aletta con un
   dito?

## Se non funziona

| Sintomo | Causa | Soluzione |
|---|---|---|
| Il servo non si muove per niente | Manca l'alimentazione a 5V | Il filo rosso va su **VBUS**, non su 3V3 |
| Il servo ronza forte ma non si muove | Sta forzando contro un fine corsa | Sei fuori dai 0-180 gradi. Usa il clamping. |
| Il servo trema in continuazione | Rumore sull'ADC, o alimentazione debole | Media mobile. Se persiste, il servo assorbe troppo dall'USB. |
| **Il Pico si riavvia quando il servo parte** | Il servo assorbe uno spunto di corrente che fa crollare la tensione | E' il problema classico. Serve un condensatore da 100-470 uF tra 5V e massa, vicino al servo. Nel kit ce n'e' qualcuno. |
| Si muove a scatti irregolari | La frequenza non e' 50 Hz | Controlla di aver chiamato `servo.freq(50)` |
| Va solo a meta' corsa | Gli impulsi sono fuori scala | Alcuni SG90 vogliono 0,6-2,4 ms invece di 0,5-2,5. Ritara i due estremi. |
| Continua a ronzare a programma finito | Il PWM resta attivo | `servo.deinit()` alla fine, oppure `duty_ns(0)` |

### Sul riavvio del Pico

Merita due righe in piu' perche' e' istruttivo. Un servo che parte assorbe per
qualche millisecondo molta piu' corrente della media. La porta USB non riesce a
starci dietro, la tensione crolla sotto la soglia minima e il Pico si resetta.

La soluzione e' un **condensatore elettrolitico** da qualche centinaio di
microfarad tra 5V e massa, il piu' vicino possibile al servo: funziona come un
piccolo serbatoio che copre il picco.

**Il condensatore elettrolitico ha una polarita'**: la zampa lunga va sul `+`,
e sul corpo c'e' una striscia che indica il `-`. Montato al contrario puo'
scoppiare, e non e' un modo di dire.

## Prossima guida

[12 - I LED NeoPixel](12-neopixel.md): tanti LED colorati con un filo solo.
