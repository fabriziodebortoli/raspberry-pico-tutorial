# Problemi comuni

**Leggi questa pagina prima di smontare tutto e ricominciare.**

Nel 90% dei casi il problema e' in questa lista, e nel 90% di quei casi e' un
filo nella riga sbagliata o un componente girato.

## Il metodo, prima dei sintomi

Quando qualcosa non va, la tentazione e' di ricontrollare tutto a caso. Non
funziona: ci metti un'ora e spesso non trovi niente.

Il metodo che funziona e' **dimezzare**:

1. **E' il codice o e' il circuito?** Aggiungi una riga che fa lampeggiare il
   LED interno (`Pin(25)`). Se quello lampeggia, il codice gira e il problema
   e' nei fili.
2. **Arriva corrente?** Metti un LED con la sua resistenza tra il punto che
   sospetti e massa. Se si accende, la corrente c'e'.
3. **Il sensore legge?** Stampa il valore grezzo con `print()` prima di
   elaborarlo. Meta' dei problemi "di logica" sono in realta' un sensore che
   legge zero.
4. **Torna all'ultima cosa che funzionava.** Cosa hai cambiato da allora?
   Rimettilo com'era e riprova.

Ogni passo elimina meta' delle possibilita'. Quattro passi e hai ristretto il
campo a un sedicesimo.

## Il Pico non si collega

| Sintomo | Causa | Soluzione |
|---|---|---|
| Windows non vede niente | Cavo solo da ricarica | Usa il cavo del kit, o un altro cavo **dati** |
| Il disco `RPI-RP2` non compare | BOOTSEL premuto nel momento sbagliato | Premi **prima**, collega **dopo**, rilascia dopo 2 secondi |
| Thonny non elenca il Pico | Firmware mancante | Rifai il flash del `.uf2` (guida 03) |
| `could not open port COM3` | La porta e' gia' occupata | Chiudi Thonny se usi Cursor, o viceversa. Ne puo' usare uno solo per volta. |
| La REPL non risponde | Un programma e' in loop | `Ctrl+C` nella Shell |
| Non si connette dopo aver caricato `main.py` | Il programma parte subito e occupa la scheda | `Ctrl+C` appena colleghi l'USB. In casi disperati: BOOTSEL e riflash. |

## Il Pico si riavvia da solo

Quasi sempre e' un problema di **corrente**, non di software.

| Quando succede | Causa | Soluzione |
|---|---|---|
| Quando parte il servo | Spunto di corrente all'avvio | Condensatore 100-470 uF tra 5V e GND, vicino al servo |
| Con tanti NeoPixel accesi | Ogni LED bianco assorbe 60 mA | Abbassa la luminosita', non superare 50 su 255 |
| A caso, sotto carico | La porta USB non regge | Prova un'altra porta, o un alimentatore da almeno 1 A |
| Toccando i fili | Corto circuito intermittente | Controlla che nessuna zampa nuda tocchi un'altra |

## Il circuito non fa niente

| Controllo | Come si verifica |
|---|---|
| L'USB e' collegato? | Sembra stupido. Non lo e'. |
| Il programma sta girando? | Aggiungi un `print()` all'inizio del ciclo |
| I fili sono nella riga giusta? | Ricorda: il canale centrale **separa** i due lati |
| Le due zampe di un componente sono in righe diverse? | Se stanno nella stessa riga, il componente e' cortocircuitato |
| La pista di massa arriva davvero? | Su molte breadboard le piste laterali sono **interrotte a meta'** |
| Il LED e' nel verso giusto? | Zampa lunga verso il GPIO, corta verso massa |

## Errori Python ricorrenti

| Errore | Cosa vuol dire | Soluzione |
|---|---|---|
| `ImportError: no module named 'machine'` | Stai eseguendo sul PC, non sul Pico | In basso a destra scegli MicroPython |
| `ImportError: no module named 'lcd1602'` | La libreria non e' sulla scheda | Carica `lcd1602.py` sul Pico |
| `ValueError: invalid pin` | Quel pin non sa fare quella cosa | L'ADC funziona solo su GP26, GP27, GP28 |
| `IndentationError` | Rientri sbagliati | Dentro un `if` o un `while` servono 4 spazi. Non mescolare spazi e tabulazioni. |
| `NameError: name 'x' isn't defined` | Variabile usata prima di crearla, o scritta male | Controlla maiuscole e minuscole |
| `TypeError: can't convert str to int` | Stai sommando un numero e una stringa | Serve `int()` o `str()` |
| `OSError: [Errno 5] EIO` | La comunicazione con la scheda si e' persa | Stacca e ricollega l'USB |
| `MemoryError` | Finita la RAM | Programma troppo grande. Togli i commenti lunghi, o `gc.collect()`. |
| `math domain error` | `log()` di zero o di un negativo | Il partitore non e' collegato: la tensione letta e' 0 o 3,3 |

## Valori dei sensori che non tornano

| Sintomo | Causa |
|---|---|
| L'ADC legge sempre 0 | Manca il 3,3V, o il filo e' sul punto sbagliato del partitore |
| L'ADC legge sempre 65535 | Manca la massa, o manca la resistenza fissa |
| L'ADC legge un valore fisso a meta' | Il pin e' scollegato e sta fluttuando |
| Il valore balla di 200-300 unita' | Normale. Fai la media di 10 letture. |
| Il valore balla di 10.000 unita' | Contatto ballerino. Premi i jumper a fondo. |
| La temperatura e' sbagliata di 3-4 gradi | Normale: `BETA` e le tolleranze. Per misure relative va bene. |
| La temperatura e' assurda (200 gradi, o negativa) | Sensore e resistenza invertiti nel partitore |

## Un attuatore si comporta male

| Sintomo | Causa |
|---|---|
| Il buzzer non si spegne piu' | Manca `duty_u16(0)` o `deinit()` |
| Il buzzer fa solo `tic` | Stai usando il buzzer **attivo** invece del passivo |
| Il servo ronza senza muoversi | Sta forzando fuori corsa. Limita l'angolo tra 0 e 180. |
| Il servo trema | Rumore dell'ADC che si traduce in micro-comandi |
| I NeoPixel non si accendono | Manca `np.write()` (la causa piu' frequente in assoluto) |
| I NeoPixel hanno i colori scambiati | La striscia usa l'ordine GRB: scambia i primi due valori |
| Il LED non si accende | Montato al contrario, o manca la resistenza (e allora e' bruciato) |

## Il display non scrive

Ha una pagina sua nella [guida 13](../guide/13-display-lcd.md), ma il riassunto
e' questo:

1. **Non vedi i quadratini neri?** Problema di alimentazione o contrasto. Gira
   il potenziometro **lentamente** per tutta la corsa.
2. **Vedi i quadratini ma non il testo?** Problema di dati. Controlla che `RW`
   sia a massa e che `D4`-`D7` siano sui pin 11-14 del display, non sui 7-10.

## Comandi di emergenza

Da incollare nella REPL quando qualcosa e' rimasto acceso:

```python
# Spegni il buzzer
from machine import Pin, PWM
PWM(Pin(18)).deinit()
```

```python
# Spegni i NeoPixel
from machine import Pin
import neopixel
np = neopixel.NeoPixel(Pin(17), 8)
for i in range(8):
    np[i] = (0, 0, 0)
np.write()
```

```python
# Spegni il servo (smette di ronzare)
from machine import Pin, PWM
PWM(Pin(16)).deinit()
```

```python
# Vedi quali file ci sono sul Pico
import os
os.listdir()
```

```python
# Cancella un file dal Pico
import os
os.remove("main.py")
```

```python
# Quanta RAM e' libera
import gc
gc.collect()
print(gc.mem_free(), "byte liberi")
```

## Il reset totale

Quando hai perso il controllo della scheda e non riesci piu' a collegarti:

1. Metti il Pico in **BOOTSEL** (tieni premuto, collega l'USB, rilascia)
2. Scarica il file `flash_nuke.uf2` da
   <https://datasheets.raspberrypi.com/soft/flash_nuke.uf2>
3. Trascinalo sul disco `RPI-RP2`: cancella tutta la flash
4. Rifai il BOOTSEL e ricarica MicroPython (guida 03)

**Perdi tutti i file che erano sul Pico.** Non e' un problema se hai fatto i
commit su git, ed e' esattamente il motivo per cui si usa git.

## Quando chiedere aiuto

Prima di chiedere, prepara queste tre cose. Ti servono comunque per spiegare il
problema, e spesso mentre le scrivi ti accorgi da solo di dov'e' l'errore:

1. **Cosa ti aspettavi che succedesse**
2. **Cosa e' successo invece** (il messaggio di errore esatto, copiato)
3. **Cosa hai gia' provato**

Questo si chiama fare una buona domanda, e vale per tutta la vita.
