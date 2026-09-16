# 04 - Il LED interno

## Obiettivo

Far lampeggiare il LED che sta gia' sulla scheda. E' il "ciao mondo"
dell'elettronica: quando lampeggia, sai che tutta la catena funziona - PC,
cavo, firmware, codice.

## Ti serve

Solo il Pico collegato all'USB. **Nessun filo**: il LED e' gia' sulla scheda,
collegato internamente a GP25.

## Come funziona

Un GPIO configurato come **uscita** puo' stare in due stati: 3,3V (che in
codice e' `1`) oppure 0V (`0`). Il LED interno e' collegato tra GP25 e massa,
quindi mettendo GP25 a `1` ci passa corrente e si accende.

Tutto qui. Il resto della guida e' Python.

## Accendilo a mano (REPL)

Prima di scrivere un programma, facciamolo a mano. Scrivi nella Shell, una riga
per volta:

```python
from machine import Pin
led = Pin(25, Pin.OUT)
led.value(1)
```

Il LED sulla scheda **si accende**. Ora:

```python
led.value(0)
```

Si spegne. Ci hai messo tre righe.

Guardiamole:

- `from machine import Pin` - il modulo `machine` contiene tutto quello che
  parla con l'hardware. Da li' prendiamo `Pin`. Questo modulo esiste solo in
  MicroPython: sul PC non c'e', perche' il PC non ha piedini.
- `Pin(25, Pin.OUT)` - crea un oggetto che rappresenta GP25 e lo configura come
  uscita. Da adesso GP25 e' un pin che comanda, non che ascolta.
- `led.value(1)` - mettici sopra 3,3V.

> Nota: `Pin(25)` funziona perche' il tuo e' un Pico base. Sul Pico W il LED e'
> collegato diversamente e serve `Pin("LED")`. Anche da te `Pin("LED")`
> funziona, ma useremo `Pin(25)` perche' rende chiaro che e' un GPIO come tutti
> gli altri.

## Il codice

Ora scriviamolo come programma. In Thonny: **File > Nuovo**, incolla, poi
**Esegui** (il triangolino verde, o `F5`).

Thonny ti chiede dove salvare: scegli **Raspberry Pi Pico** e chiamalo
`04-blink.py`.

```python
# 04-blink.py - fa lampeggiare il LED interno del Pico

from machine import Pin
import time

# GP25 e' il LED saldato sulla scheda. OUT = lo usiamo per comandare.
led = Pin(25, Pin.OUT)

# while True significa "ripeti per sempre".
# Un microcontrollore non "finisce": resta in ascolto finche' ha corrente.
while True:
    led.value(1)      # accendi (3,3V sul pin)
    time.sleep(0.5)   # aspetta mezzo secondo
    led.value(0)      # spegni (0V sul pin)
    time.sleep(0.5)   # aspetta mezzo secondo
```

Il LED lampeggia. **Per fermarlo premi `Ctrl+C` nella Shell**, oppure il
pulsante rosso di stop.

## Le due cose importanti di questo codice

### `while True` non e' un errore

Sul PC un ciclo infinito e' quasi sempre un bug. Qui e' **normale e voluto**.

Il Pico non ha niente altro da fare. Non c'e' un desktop a cui tornare, non c'e'
un altro programma in attesa. Il suo lavoro e' questo, e lo fa finche' ha
corrente.

Quasi ogni programma che scriverai da qui in poi finisce dentro un `while True`.

### `time.sleep()` e' tempo buttato

`time.sleep(0.5)` vuol dire "fermati completamente per mezzo secondo". Durante
quel tempo il Pico **non fa assolutamente nulla**: non legge sensori, non
risponde a pulsanti, sta fermo.

Per far lampeggiare un LED va benissimo. Quando avrai un pulsante da leggere
(guida 06) iniziera' a dare fastidio, e piu' avanti impareremo a farne a meno.
Tienilo a mente: **e' la prima limitazione seria che incontrerai.**

## Prova a cambiare

1. **Velocizza.** Porta i due `sleep` a `0.1`. Poi a `0.01`. Poi a `0.001`. A
   un certo punto il LED smette di sembrare lampeggiante e sembra acceso fisso
   e un po' fioco. Perche'? (La risposta si chiama persistenza della visione, ed
   e' lo stesso motivo per cui un film sembra movimento e non foto. Ti tornera'
   utile nella guida 07.)

2. **Lampeggio asimmetrico.** Fai in modo che stia acceso 0,1 secondi e spento
   2 secondi, come il LED di stand-by di una TV.

3. **SOS in codice Morse.** Tre lampeggi corti, tre lunghi, tre corti, pausa,
   da capo. Corto = 0,2s, lungo = 0,6s, pausa tra lettere = 0,6s.

   Per il punto 3 c'e' un modo stupido e uno intelligente. Quello stupido e'
   scrivere 18 righe di `value()` e `sleep()`. Quello intelligente e' accorgersi
   che stai ripetendo la stessa cosa tre volte e usare un `for`:

   ```python
   for i in range(3):
       led.value(1)
       time.sleep(0.2)
       led.value(0)
       time.sleep(0.2)
   ```

   Prova prima nel modo stupido, cosi' senti la noia di scriverlo. Poi
   riscrivilo col `for`. La noia e' il motivo per cui esistono i cicli.

## Un'alternativa piu' compatta

Esiste anche `led.toggle()`, che inverte lo stato: se e' acceso spegne, se e'
spento accende. Il blink diventa:

```python
while True:
    led.toggle()
    time.sleep(0.5)
```

Quattro righe diventano due. E' piu' corto ma meno esplicito: chi legge deve
sapere cosa fa `toggle()`. Non c'e' una versione giusta, dipende da cosa vuoi
rendere evidente. E' il tipo di scelta che farai continuamente.

## Se non funziona

| Sintomo | Causa | Soluzione |
|---|---|---|
| `ImportError: no module named 'machine'` | Thonny sta eseguendo sul PC, non sul Pico | In basso a destra scegli "MicroPython (Raspberry Pi Pico)" |
| Il LED non si accende ma nessun errore | Stai usando il pin sbagliato | Deve essere `Pin(25)`. Prova `Pin("LED")`. |
| Il programma parte ma non lo fermo piu' | Sei nel `while True` | `Ctrl+C` nella Shell, o il pulsante rosso di stop |
| `SyntaxError` alla riga del `while` | Manca l'indentazione dentro il ciclo | Le righe dentro `while` vanno rientrate di 4 spazi |
| Il LED lampeggia anche dopo lo stop | Il Pico esegue l'ultimo programma salvato | Normale. Se hai salvato come `main.py` parte da solo all'accensione. |

## La cosa di `main.py` (ricordatela)

Se salvi un file sul Pico chiamandolo esattamente **`main.py`**, quel programma
parte **da solo ogni volta che il Pico riceve corrente**, anche senza PC. Col
cavo di un caricabatterie da telefono, il tuo circuito funziona da solo.

Rovescio della medaglia: se `main.py` contiene un `while True` che parte
subito, Thonny a volte fa fatica a riconnettersi. Se ti succede, premi `Ctrl+C`
nella Shell appena colleghi, oppure rifai il BOOTSEL e riflasha il firmware
(perdi i file, ma torni pulito).

Per ora dai ai file il nome della guida (`04-blink.py`). Useremo `main.py` solo
nella guida 14.

## Prossima guida

[05 - LED esterno](05-led-esterno.md): lo stesso lampeggio, ma con un LED vero
sulla breadboard. E' li' che si impara l'elettronica.
