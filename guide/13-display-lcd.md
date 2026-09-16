# 13 - Il display LCD

## Obiettivo

Far scrivere al Pico su uno schermo vero. E' la guida piu' difficile del
percorso: undici fili, una libreria da scrivere e un componente che non
perdona gli errori di collegamento.

**Prenditi un pomeriggio intero, non mezz'ora prima di cena.**

## Ti serve

- 1 display LCD 1602 (il rettangolo nero con lo schermo blu)
- 1 potenziometro (serve per il contrasto, e serve **davvero**)
- 1 resistenza da 220 ohm
- Una decina di jumper
- Pazienza

## Perche' e' difficile

I sensori delle guide precedenti avevano 2 o 3 fili. Questo display ne ha
**16**, e ne useremo 11.

Il motivo e' storico. Dentro c'e' un controller che si chiama **HD44780**,
progettato da Hitachi negli anni Ottanta. All'epoca non esistevano i bus
seriali comodi di oggi: i dati si mandavano **in parallelo**, un filo per ogni
bit.

> **Esiste la scorciatoia?** Si': si vende un modulino "backpack I2C" da due
> euro che si salda dietro al display e riduce i fili a 4. Nel tuo kit non c'e',
> e onestamente e' meglio cosi': cablarlo in parallelo una volta ti insegna
> cosa fa quel modulino, e da li' in poi lo apprezzerai.

## Come funziona

### I 16 piedini

Sul bordo del display ci sono 16 contatti, numerati da 1 a 16. Le sigle sono
stampate sulla piastrina:

| # | Sigla | Cos'e' | Lo usiamo? |
|---|---|---|---|
| 1 | `VSS` | massa | si' |
| 2 | `VDD` | alimentazione 5V | si' |
| 3 | `V0` | **contrasto** | si', col potenziometro |
| 4 | `RS` | seleziona comando o carattere | si' |
| 5 | `RW` | lettura o scrittura | si', fisso a massa |
| 6 | `E` | *enable*, il colpo di clock | si' |
| 7-10 | `D0`-`D3` | dati, bit bassi | **no** |
| 11-14 | `D4`-`D7` | dati, bit alti | si' |
| 15 | `A` | anodo retroilluminazione | si' |
| 16 | `K` | catodo retroilluminazione | si' |

### La modalita' a 4 bit

Il controller vuole 8 bit per volta, ma ha una modalita' furba: gli mandi
**mezzo byte alla volta** (si chiama *nibble*), prima i 4 bit alti e poi i 4
bassi. Serve la meta' dei fili e va comunque velocissimo per quello che ci
serve.

Per questo `D0`-`D3` restano scollegati.

### Il contrasto, il pin che frega tutti

Il piedino `V0` regola il contrasto e **vuole una tensione variabile**, non
acceso o spento. Se lo lasci scollegato o lo metti a 5V, lo schermo resta
completamente bianco oppure completamente nero, e tu pensi di aver sbagliato i
collegamenti dati.

Per questo serve il potenziometro. **Non e' opzionale.**

Il primo segnale che il display e' vivo sara' vedere comparire i quadratini
neri sulla prima riga girando il potenziometro. Se li vedi, l'alimentazione e
il contrasto sono a posto, e puoi concentrarti sul resto.

### RS ed E

- **`RS`** (*Register Select*) dice al display se quello che mandi e' un
  **comando** (`RS=0`, tipo "cancella tutto") o un **carattere da stampare**
  (`RS=1`).
- **`E`** (*Enable*) e' il segnale che dice "adesso leggi". Tu prepari i bit
  sui fili dati, poi fai un impulso su `E`, e il display li acquisisce. E'
  esattamente come un colpo di clock.

## Collegamenti

**Stacca l'USB.** Prenditi tempo, controlla due volte, e procedi con ordine.

Il display va alimentato a **5 volt**, quindi usa la pista collegata a VBUS
come nelle guide 11 e 12.

### Alimentazione e contrasto (falli per primi)

| # | Da | A |
|---|---|---|
| 1 | LCD pin 1 `VSS` | pista `-` blu |
| 2 | LCD pin 2 `VDD` | pista 5V (VBUS) |
| 3 | LCD pin 5 `RW` | pista `-` blu (scriviamo e basta) |
| 4 | LCD pin 15 `A` | resistenza 220 ohm, poi pista 5V |
| 5 | LCD pin 16 `K` | pista `-` blu |
| 6 | **potenziometro** estremo 1 | pista 5V |
| 7 | **potenziometro** estremo 2 | pista `-` blu |
| 8 | **potenziometro** centrale | LCD pin 3 `V0` |

**Fermati qui e fai una prova.** Collega l'USB e gira il potenziometro
lentamente da un estremo all'altro. A un certo punto devi vedere **una fila di
quadratini neri** sulla riga superiore. Se li vedi, ottimo: hai finito la parte
che sbaglia il 90% delle persone.

Se non li vedi, vai direttamente alla sezione "Se non funziona" - inutile
collegare i dati.

### I dati

**Stacca di nuovo l'USB.**

| # | Da | A |
|---|---|---|
| 9 | LCD pin 4 `RS` | riga del **GP2** (pin fisico 4) |
| 10 | LCD pin 6 `E` | riga del **GP3** (pin fisico 5) |
| 11 | LCD pin 11 `D4` | riga del **GP4** (pin fisico 6) |
| 12 | LCD pin 12 `D5` | riga del **GP5** (pin fisico 7) |
| 13 | LCD pin 13 `D6` | riga del **GP6** (pin fisico 9) |
| 14 | LCD pin 14 `D7` | riga del **GP7** (pin fisico 10) |

I pin 7, 8, 9, 10 (`D0`-`D3`) restano **scollegati**.

> **Consiglio pratico:** usa fili dello stesso colore per i quattro dati, e un
> colore diverso per `RS` ed `E`. Quando qualcosa non va, riconoscere a colpo
> d'occhio quale gruppo stai guardando ti fa risparmiare mezz'ora.

## La libreria

Qui c'e' la parte nuova: il codice non entra in un file solo.

Copia il file `codice/13-display/lcd1602.py` sul Pico (con MicroPico: **Upload
current file to Pico**). Quel file contiene la classe che parla con l'HD44780,
e i tuoi programmi la importano.

Questo e' il momento in cui il tuo codice smette di essere uno script e inizia
a essere un **progetto**: un file che contiene il "come" e un altro che
contiene il "cosa".

Vale la pena aprire `lcd1602.py` e leggerlo, anche se non capisci tutto. Le
cose da notare:

- **`_nibble()`** mette i 4 bit sui pin e da' un impulso su `E`
- **`_comando()`** manda un byte in due nibble con `RS=0`
- **`_carattere()`** fa lo stesso con `RS=1`
- L'**`__init__`** contiene una sequenza di risveglio con tempi precisi presa
  dal manuale Hitachi. Quei `sleep_ms(5)` e `sleep_us(150)` non sono a caso:
  sono i tempi minimi che il chip richiede. Se li togli, a volte funziona e a
  volte no - che e' peggio che non funzionare mai.

Il trattino basso davanti a `_nibble` e' una convenzione Python: vuol dire
"questo e' un dettaglio interno, non chiamarlo da fuori".

## Il codice

### Ciao mondo

```python
# 13a-ciao.py - il primo testo sul display

from lcd1602 import LCD1602
import time

lcd = LCD1602(rs=2, e=3, d4=4, d5=5, d6=6, d7=7)

lcd.pulisci()
lcd.vai_a(0, 0)              # colonna 0, riga 0
lcd.scrivi("Ciao Daniele!")

lcd.vai_a(0, 1)              # colonna 0, riga 1
lcd.scrivi("Funziona :)")
```

Se compare il testo, hai superato la guida piu' difficile del percorso.

Il display e' **16 colonne per 2 righe** - da qui il nome 1602. Se scrivi piu'
di 16 caratteri, quelli in eccesso non vanno a capo: finiscono in una zona di
memoria non visibile e spariscono.

### Un orologio

```python
# 13b-cronometro.py - conta i secondi dall'accensione

from lcd1602 import LCD1602
import time

lcd = LCD1602(rs=2, e=3, d4=4, d5=5, d6=6, d7=7)

lcd.pulisci()
lcd.vai_a(0, 0)
lcd.scrivi("Acceso da:")

secondi = 0
while True:
    minuti = secondi // 60
    resto = secondi % 60

    lcd.vai_a(0, 1)
    # :02d significa "due cifre, con lo zero davanti se serve"
    lcd.scrivi("{:02d}:{:02d}".format(minuti, resto))

    time.sleep(1)
    secondi = secondi + 1
```

Nota che **non chiamo `pulisci()` a ogni giro**. Cancellare tutto e riscrivere
fa sfarfallare il display in modo fastidioso. Meglio riposizionare il cursore e
sovrascrivere solo quello che cambia.

Attenzione pero': se il testo nuovo e' piu' corto del precedente, i caratteri
vecchi restano. Per questo si scrive `05` e non `5`: la lunghezza resta sempre
la stessa.

### Termometro con display

```python
# 13c-termometro.py - la guida 10 con uno schermo vero

from machine import ADC, Pin
from lcd1602 import LCD1602
import time
import math

ntc = ADC(Pin(27))
lcd = LCD1602(rs=2, e=3, d4=4, d5=5, d6=6, d7=7)

R_FISSA = 10000
R0 = 10000
T0 = 298.15
BETA = 3950

def leggi_temperatura():
    tensione = ntc.read_u16() * 3.3 / 65535
    resistenza = R_FISSA * (3.3 - tensione) / tensione
    inverso_T = 1 / T0 + (1 / BETA) * math.log(resistenza / R0)
    return 1 / inverso_T - 273.15

lcd.pulisci()
lcd.vai_a(0, 0)
lcd.scrivi("Temperatura:")

while True:
    gradi = leggi_temperatura()
    lcd.vai_a(0, 1)
    lcd.scrivi("{:5.1f} gradi   ".format(gradi))
    time.sleep(1)
```

Gli spazi in fondo a `"{:5.1f} gradi   "` servono a cancellare eventuali
caratteri rimasti da una scritta precedente piu' lunga. E' un trucco brutto ma
universale.

## Prova a cambiare

1. **Testo scorrevole.** Un messaggio piu' lungo di 16 caratteri che scorre da
   destra a sinistra. Suggerimento: usa lo slicing delle stringhe,
   `testo[i:i+16]`.

2. **Menu con pulsanti.** Due pulsanti per scorrere tra tre schermate:
   temperatura, luce, stato del servo.

3. **Barra di caricamento.** Riempi la seconda riga di caratteri a mano a mano,
   in base al potenziometro. Con 16 caratteri hai 16 livelli.

4. **Caratteri personalizzati.** L'HD44780 ti lascia definire fino a 8 simboli
   tuoi, disegnandoli in una griglia 5x8. Cerca `createChar HD44780` e prova a
   fare un cuoricino o il simbolo dei gradi. E' un bel salto di livello: stai
   programmando la memoria del controller.

## Se non funziona

### Se non vedi i quadratini neri

E' il primo scoglio. Nell'ordine:

| Causa | Verifica |
|---|---|
| Contrasto non regolato | Gira il potenziometro **lentamente** per tutta la corsa. I quadratini compaiono solo in una porzione stretta. |
| `V0` non collegato al cursore | Il filo va sul piedino **centrale** del potenziometro |
| Alimentazione a 3,3V invece che 5V | `VDD` deve stare su **VBUS** |
| `VSS` e `VDD` scambiati | Pin 1 = massa, pin 2 = 5V. Invertiti, il display non si accende. |
| Retroilluminazione non collegata | I quadratini si vedono anche senza, ma al buio e' dura. Collega `A` e `K`. |
| Contatti non saldati | Se il display ha i fori vuoti senza striscia di pin, va saldato. |

### Se vedi i quadratini ma non il testo

Buona notizia: alimentazione e contrasto sono a posto, il problema e' nei dati.

| Causa | Verifica |
|---|---|
| `RW` non a massa | Se `RW` fluttua o e' a 5V, il display non accetta scritture. Pin 5 a massa, sempre. |
| Un filo dati nella riga sbagliata | Ricontrolla `D4`→GP4, `D5`→GP5, `D6`→GP6, `D7`→GP7 |
| `D4`-`D7` collegati a `D0`-`D3` | Sono i pin 11-14, non 7-10. Errore facilissimo. |
| `RS` ed `E` scambiati | `RS` = pin 4, `E` = pin 6. C'e' il pin 5 in mezzo. |
| `lcd1602.py` non caricato sul Pico | Fai **Upload current file to Pico** su quel file |

### Altri sintomi

| Sintomo | Causa | Soluzione |
|---|---|---|
| `ImportError: no module named 'lcd1602'` | Il file non e' sul Pico | Upload di `lcd1602.py` |
| Caratteri strani e casuali | Un filo dati fa contatto male | Premi i jumper a fondo, uno per uno |
| Scrive solo la prima meta' dei caratteri | Un nibble su due si perde: timing | Aumenta i `sleep_us` nella libreria |
| Funziona, ma a volte parte vuoto | La sequenza di inizializzazione e' andata storta | Aggiungi `time.sleep(1)` prima di creare l'oggetto LCD |
| Il testo compare sulla riga sbagliata | Le righe sono 0 e 1, non 1 e 2 | `vai_a(0, 0)` e' la prima riga |
| Scrive la seconda riga in mezzo alla prima | Indirizzi interni | La riga 1 comincia a 0x40, gia' gestito da `vai_a()` |

### Il consiglio generale

Quando hai undici fili e non funziona, **non ricontrollarli a caso**. Procedi
per blocchi:

1. Funziona l'alimentazione? (quadratini neri)
2. Funziona `RW`? (deve essere a massa, misurabile a occhio dal filo)
3. Funzionano i dati? (se i quadratini ci sono e il testo no, e' qui)

Ogni domanda dimezza lo spazio del problema. E' lo stesso metodo del LED
interno nella guida 05: dividi, non indovinare.

## Prossima guida

[14 - Progetto finale](14-progetto-finale.md): tutto quello che hai imparato,
in un colpo solo.
