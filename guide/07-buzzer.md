# 07 - Il buzzer

## Obiettivo

Far suonare il Pico, e imparare il **PWM** - la tecnica che userai poi per
regolare la luminosita' dei LED, muovere il servo e mille altre cose. E' la
guida piu' importante della prima parte.

## Ti serve

- 1 buzzer **passivo** (vedi sotto come distinguerlo)
- 2 jumper
- Il LED su GP15 con la resistenza, se vuoi fare l'esercizio 3

## Attivo o passivo?

Nel kit ci sono due dischetti neri che sembrano identici. Non lo sono.

| | Buzzer **attivo** | Buzzer **passivo** |
|---|---|---|
| Cosa contiene | un oscillatore dentro | solo una membrana |
| Se gli dai 3,3V fissi | suona a una nota fissa | fa un `click` e basta |
| Suona note diverse? | no, una sola | si', quella che gli mandi tu |
| Aspetto | spesso chiuso sopra con un adesivo | spesso si vede la membrana |

**A noi serve quello passivo**, perche' vogliamo scegliere noi la nota.

Come li distingui in pratica: collega un dischetto tra `3V3` e `GND` sulla
breadboard (senza Pico, direttamente sulle piste). Se fa un suono continuo e'
attivo. Se fa solo un `tic` e' passivo. Segnati quale e'.

## Come funziona il PWM

Questa parte leggila con calma, perche' e' il concetto che ti porti dietro per
tutto il resto.

Un pin GPIO sa fare solo due cose: 0V o 3,3V. Non sa fare 1,5V. Allora come si
fa a ottenere una luminosita' intermedia, o una nota musicale?

**Si accende e si spegne velocissimo.**

PWM sta per *Pulse Width Modulation*, modulazione della larghezza dell'impulso.
L'idea: il pin si accende e si spegne molte volte al secondo, e tu controlli
**per quanta parte del tempo resta acceso**.

```
  duty 50%    ____      ____      ____
             |    |    |    |    |    |
           __|    |____|    |____|    |____

  duty 25%    __        __        __
             |  |      |  |      |  |
           __|  |______|  |______|  |______

  duty 90%    ________  ________  ________
             |        ||        ||        |
           __|        ||        ||        |
```

Due numeri controllano tutto:

- **Frequenza**: quante volte al secondo si ripete il ciclo. Si misura in hertz
  (Hz). Con il buzzer, la frequenza **e' la nota**.
- **Duty cycle**: la percentuale di tempo in cui sta acceso. Con un LED, il
  duty cycle **e' la luminosita'**. Con il buzzer, grosso modo il volume.

In MicroPython il duty si imposta con `duty_u16()`, che vuole un numero da `0`
(sempre spento) a `65535` (sempre acceso). Il numero strano viene da 16 bit:
2 elevato alla 16 fa 65536, e si conta da zero.

| duty_u16 | Percentuale |
|---|---|
| 0 | 0% |
| 16384 | 25% |
| 32768 | 50% |
| 65535 | 100% |

## Collegamenti

**Stacca l'USB.**

Il buzzer passivo non ha polarita' critica per il nostro uso, ma se vedi un `+`
stampato sopra, quel piedino va verso il GPIO.

| # | Da | A |
|---|---|---|
| 1 | **buzzer**, un piedino | riga libera, es. riga 40 |
| 2 | **buzzer**, altro piedino | riga libera, es. riga 42 |
| 3 | riga del **GP18** (pin fisico 24) | riga 40 |
| 4 | riga 42 | pista `-` blu (massa) |

```
  GP18 ---[filo]--- riga40 [ BUZZER ] riga42 ---[filo]--- pista blu (-)
```

## Il codice

### Una nota sola

```python
# 07a-nota.py - suona un LA per due secondi

from machine import Pin, PWM
import time

buzzer = PWM(Pin(18))

buzzer.freq(440)            # 440 Hz = nota LA
buzzer.duty_u16(32768)      # 50% = volume medio
time.sleep(2)

buzzer.duty_u16(0)          # duty a zero = silenzio
buzzer.deinit()             # libera il pin
```

**`buzzer.deinit()` alla fine e' importante.** Se il programma termina senza
spegnere il PWM, il buzzer continua a suonare fino a che non stacchi l'USB. E
dopo dieci secondi di nota fissa ti viene voglia di lanciare il Pico dalla
finestra.

Se ti succede, nella Shell scrivi:

```python
from machine import Pin, PWM
PWM(Pin(18)).deinit()
```

### Una scala

```python
# 07b-scala.py - suona una scala di DO maggiore

from machine import Pin, PWM
import time

buzzer = PWM(Pin(18))

# Frequenze in hertz delle sette note, dal DO centrale
note = [262, 294, 330, 349, 392, 440, 494, 523]
nomi = ["DO", "RE", "MI", "FA", "SOL", "LA", "SI", "DO"]

for i in range(len(note)):
    print(nomi[i], note[i], "Hz")
    buzzer.freq(note[i])
    buzzer.duty_u16(32768)
    time.sleep(0.4)

buzzer.duty_u16(0)
buzzer.deinit()
```

Guarda le frequenze: il primo DO e' 262 Hz, l'ultimo e' 523. **Il doppio.**
Un'ottava sopra vuol dire esattamente frequenza doppia. Non e' una convenzione
inventata dai musicisti, e' fisica.

### Una melodia

```python
# 07c-melodia.py - Fra Martino

from machine import Pin, PWM
import time

buzzer = PWM(Pin(18))

DO = 262
RE = 294
MI = 330
FA = 349
SOL = 392
PAUSA = 0

# Ogni elemento e' una coppia (nota, durata in secondi)
melodia = [
    (DO, 0.4), (RE, 0.4), (MI, 0.4), (DO, 0.4),
    (DO, 0.4), (RE, 0.4), (MI, 0.4), (DO, 0.4),
    (MI, 0.4), (FA, 0.4), (SOL, 0.8),
    (MI, 0.4), (FA, 0.4), (SOL, 0.8),
]

def suona(frequenza, durata):
    if frequenza == PAUSA:
        buzzer.duty_u16(0)
    else:
        buzzer.freq(frequenza)
        buzzer.duty_u16(32768)
    time.sleep(durata)
    buzzer.duty_u16(0)
    time.sleep(0.05)   # stacco tra una nota e l'altra

for nota, durata in melodia:
    suona(nota, durata)

buzzer.deinit()
```

Qui compaiono due cose nuove che vale la pena notare.

**La funzione `suona()`**: invece di ripetere cinque righe per ogni nota, le
scrivi una volta e le richiami. E' lo stesso ragionamento del `for` nella guida
04, portato piu' avanti: quando ti accorgi di ripeterti, c'e' uno strumento per
smettere.

**La lista di coppie**: la melodia e' separata dal codice che la suona. Se vuoi
cambiare canzone, tocchi solo la lista. Questa separazione tra **dati** e
**logica** e' una delle idee piu' importanti della programmazione, e qui la
vedi in dieci righe.

## Prova a cambiare

1. **PWM sul LED.** Stacca il buzzer, collega il PWM a GP15 dove c'e' il LED, e
   fai variare il duty da 0 a 65535 e ritorno con un ciclo. Il LED "respira".
   Che frequenza usi? Provane una bassa tipo 10 Hz e una alta tipo 1000 Hz: con
   quella bassa vedi lo sfarfallio, con quella alta no.

   ```python
   for d in range(0, 65535, 500):
       led.duty_u16(d)
       time.sleep(0.005)
   ```

2. **Sirena.** Fai salire la frequenza da 400 a 1200 Hz e ritorno, in loop.

3. **Il campanello.** Unisci la guida 06: quando premi il pulsante suona una
   melodia. Occhio che mentre suona il Pico non legge il pulsante - e' di nuovo
   il problema di `sleep()`.

4. **Tua canzone.** Cerca online le frequenze delle note e trascrivi qualcosa
   che ti piace. Nota che `A4 = 440 Hz` e che ogni semitono si ottiene
   moltiplicando per 1,0595 (cioe' la radice dodicesima di 2).

## Se non funziona

| Sintomo | Causa | Soluzione |
|---|---|---|
| Fa solo `tic` a ogni nota | Stai usando il buzzer **attivo** | Prova l'altro dischetto |
| Non suona niente | Duty a 0, o `freq()` non impostata | Servono tutti e due: prima `freq()`, poi `duty_u16()` |
| Suona ma non si ferma piu' | Manca `deinit()` o `duty_u16(0)` | Esegui `PWM(Pin(18)).deinit()` nella Shell |
| Il volume e' bassissimo | Normale | Questi buzzer sono piccoli. Prova `duty_u16(32768)`, che e' il massimo volume utile: piu' su il suono peggiora. |
| `ValueError: freq too low` | Frequenza sotto ~8 Hz | Il PWM del Pico non scende sotto circa 8 Hz |
| Suono sporco o stonato | Duty troppo alto o troppo basso | Il 50% e' il valore migliore per un'onda quadra |

## Cosa ti porti dietro

Il PWM ti servira' in tre guide su cinque da qui in avanti:

- **Guida 11**: il servo si comanda con impulsi PWM di larghezza precisa
- Luminosita' dei LED, velocita' dei motori, regolazioni di ogni tipo

Se c'e' una cosa da aver capito bene di questa guida, e' che **frequenza e
duty cycle sono due manopole indipendenti**, e che cosa significano cambia a
seconda di cosa hai attaccato al pin.

## Prossima guida

[08 - Il potenziometro](08-potenziometro.md): finora il mondo era acceso o
spento. Adesso scopri le vie di mezzo.
