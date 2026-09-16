# 06 - Il pulsante

## Obiettivo

Far reagire il Pico a qualcosa che fai tu. Finora comandava lui: adesso
ascolta.

## Ti serve

- 1 pulsante (tastino quadrato a 4 zampe)
- Il LED su GP15 con la sua resistenza (resta montato dalla guida 05)
- 2 jumper

## Come funziona

### Il pulsante ha quattro zampe ma due contatti

Il tastino ha 4 piedini, ma non sono 4 contatti indipendenti. **Sono collegati
a coppie**: due sono sempre uniti tra loro, e premendo il tasto le due coppie
si uniscono.

Il problema e' capire quali sono accoppiate. La regola:

```
      1 o-----------o 2         1 e 2 sono SEMPRE collegati
        |           |
        |  [ TASTO ]|           premendo, si uniscono le due coppie
        |           |
      3 o-----------o 4         3 e 4 sono SEMPRE collegati
```

Montato sulla breadboard a cavallo del canale, i piedini dello **stesso lato**
sono quelli sempre collegati.

> **In pratica:** monta il pulsante a cavallo del canale centrale e usa **una
> zampa a sinistra e una a destra** (in diagonale, per essere sicuro). Se usi
> due zampe dello stesso lato, il circuito e' sempre chiuso e il pulsante non
> fa niente.

### Il problema del pin che fluttua

Qui c'e' la parte concettuale importante, e vale la pena capirla bene.

Un pin configurato come **ingresso** legge la tensione che trova. Ma se lo
colleghi solo al pulsante, quando il pulsante e' **rilasciato** quel pin non e'
collegato a niente. Non e' a 0V: e' **scollegato**, e si dice che "fluttua".

Un pin che fluttua legge valori casuali, perche' raccoglie il rumore elettrico
dell'ambiente come una minuscola antenna. Il tuo programma vedra' il pulsante
premersi da solo a caso.

La soluzione si chiama **resistenza di pull-up**: una resistenza che collega il
pin a 3,3V, tenendolo a un valore noto quando non succede niente.

```
        3,3V
          |
         [R]  pull-up (dentro il Pico, non la monti tu)
          |
  GP16 ---+
          |
       [TASTO]
          |
         GND
```

- **Pulsante rilasciato**: il circuito e' aperto, la resistenza tira il pin a
  3,3V, il Pico legge **1**
- **Pulsante premuto**: il pin viene collegato direttamente a massa, e vince,
  quindi il Pico legge **0**

**Attenzione alla logica invertita:** con il pull-up, `0` significa premuto e
`1` significa rilasciato. E' controintuitivo la prima volta e fa sbagliare
tutti. Ricordalo: **premuto = 0**.

La cosa comoda e' che il Pico ha le resistenze di pull-up **gia' dentro il
chip**. Non devi montarle: le attivi da codice con `Pin.PULL_UP`.

## Collegamenti

**Stacca l'USB.** Il LED della guida 05 resta dov'e'.

| # | Da | A |
|---|---|---|
| 1 | **pulsante** | a cavallo del canale, es. righe 30-32 |
| 2 | riga del **GP16** (pin fisico 21) | una zampa del pulsante (lato A-E) |
| 3 | altra zampa del pulsante, **lato opposto** (F-J) | pista `-` blu (massa) |

```
  GP16 ---[filo]--- [ TASTO ] ---[filo]--- pista blu (-)
                    a cavallo
                   del canale
```

Solo due fili. Nessuna resistenza esterna: quella e' dentro il Pico.

## Il codice

Partiamo dal piu' semplice possibile: leggere e stampare.

```python
# 06a-leggi-pulsante.py - stampa lo stato del pulsante

from machine import Pin
import time

# IN = ingresso. PULL_UP attiva la resistenza interna verso 3,3V.
pulsante = Pin(16, Pin.IN, Pin.PULL_UP)

while True:
    print(pulsante.value())
    time.sleep(0.2)
```

Eseguilo e guarda la Shell: scorre una colonna di `1`. Tieni premuto il
pulsante: diventano `0`.

**Fallo davvero prima di andare avanti.** Vedere con i tuoi occhi che premuto =
0 vale piu' di dieci righe di spiegazione.

### Adesso accendiamo il LED

```python
# 06b-pulsante-led.py - il LED e' acceso mentre tieni premuto

from machine import Pin

led = Pin(15, Pin.OUT)
pulsante = Pin(16, Pin.IN, Pin.PULL_UP)

while True:
    if pulsante.value() == 0:   # 0 = premuto (logica invertita del pull-up)
        led.value(1)
    else:
        led.value(0)
```

Nota che qui **non c'e' nessun `sleep`**. Il ciclo gira a piena velocita',
decine di migliaia di volte al secondo, e per questo il LED risponde
istantaneamente. Se ci mettessi un `sleep(0.5)`, il pulsante sembrerebbe
rotto: premendo e rilasciando in fretta, il Pico starebbe dormendo proprio nel
momento del clic.

**Questo e' il vero costo di `sleep()`** di cui parlava la guida 04. Adesso lo
vedi.

## Il rimbalzo dei contatti

Prova questo, che sembra ovvio e invece no:

```python
# 06c-conta.py - conta le pressioni. O almeno ci prova.

from machine import Pin

pulsante = Pin(16, Pin.IN, Pin.PULL_UP)
conteggio = 0
stato_precedente = 1

while True:
    stato = pulsante.value()
    # Ci interessa il MOMENTO in cui passa da rilasciato (1) a premuto (0)
    if stato == 0 and stato_precedente == 1:
        conteggio = conteggio + 1
        print("Premuto", conteggio, "volte")
    stato_precedente = stato
```

Premi il pulsante una volta. Quasi sicuramente il conteggio salta di 2, 3 o 5.

Non e' un bug del codice: e' **fisica**. Dentro il pulsante ci sono due
lamelle metalliche, e quando si toccano **rimbalzano** per qualche millisecondo
prima di fermarsi. Il Pico, che controlla decine di migliaia di volte al
secondo, vede ogni singolo rimbalzo come una pressione distinta.

Si chiama **bouncing** (rimbalzo), e la soluzione si chiama **debounce**.

### Il debounce piu' semplice

Dopo aver rilevato una pressione, aspetta un attimo prima di dare retta di
nuovo al pulsante. I rimbalzi durano meno di 20 millisecondi, quindi 50 sono
abbondanti:

```python
# 06d-conta-debounce.py - conta le pressioni, sul serio

from machine import Pin
import time

pulsante = Pin(16, Pin.IN, Pin.PULL_UP)
conteggio = 0
stato_precedente = 1

while True:
    stato = pulsante.value()
    if stato == 0 and stato_precedente == 1:
        conteggio = conteggio + 1
        print("Premuto", conteggio, "volte")
        time.sleep(0.05)   # 50 ms: i rimbalzi finiscono, tu non te ne accorgi
    stato_precedente = stato
```

Adesso conta giusto.

Questo `sleep(0.05)` e' un compromesso: e' abbastanza corto da essere
impercettibile e abbastanza lungo da coprire i rimbalzi. Non e' la soluzione
piu' elegante che esista, ma e' quella che si usa nel 90% dei casi.

## Prova a cambiare

1. **Interruttore invece di pulsante.** Fai in modo che una pressione accenda
   il LED e lo lasci acceso, e la pressione successiva lo spenga. Suggerimento:
   parti da `06d` e sostituisci il conteggio con `led.toggle()`.

2. **Pressione lunga.** Se tieni premuto piu' di 2 secondi, il LED lampeggia
   veloce. Se premi e rilasci subito, si accende e basta. Suggerimento:
   `time.ticks_ms()` ti da' i millisecondi da quando il Pico e' acceso, e
   `time.ticks_diff(dopo, prima)` la differenza tra due istanti.

3. **Due pulsanti.** Aggiungine uno su GP17: uno accende, l'altro spegne. Piu'
   facile del punto 1, ma con il doppio dei fili.

## Se non funziona

| Sintomo | Causa | Soluzione |
|---|---|---|
| Legge sempre `0`, anche non premendo | Stai usando due zampe dello stesso lato: e' sempre chiuso | Usa due zampe in diagonale, a cavallo del canale |
| Legge sempre `1`, anche premendo | Un filo non fa contatto, o il pulsante e' montato di traverso | Il tastino entra bene solo in un verso. Ruotalo di 90 gradi e riprova. |
| Legge valori casuali che cambiano da soli | Manca `Pin.PULL_UP` | E' esattamente il pin che fluttua. Aggiungilo. |
| Il conteggio salta di 3-4 per pressione | Rimbalzo | Aggiungi il debounce (`06d`) |
| Il LED reagisce in ritardo | C'e' un `sleep` lungo nel ciclo | Toglilo, o riducilo |
| Il pulsante non entra nella breadboard | E' ruotato di 90 gradi | Le zampe sono in rettangolo, non in quadrato. Giralo. |

## Prossima guida

[07 - Il buzzer](07-buzzer.md): il Pico impara a fare rumore, e tu impari il
PWM - la tecnica piu' utile di tutto il percorso.
