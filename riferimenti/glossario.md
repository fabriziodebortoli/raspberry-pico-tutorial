# Glossario

Le parole che incontri nelle guide, spiegate in una riga o due. In ordine
alfabetico.

## A

**ADC** - *Analog to Digital Converter*. Il circuito che trasforma una tensione
in un numero. Sul Pico legge da 0 a 3,3V e restituisce da 0 a 65535. Solo GP26,
GP27 e GP28 ce l'hanno. (Guida 08)

**Anodo** - Il lato positivo di un componente polarizzato. Su un LED e' la
zampa lunga. (Guida 05)

**Analogico** - Una grandezza che varia con continuita', non a scatti. La luce,
la temperatura, la posizione di una manopola. Il contrario di digitale.

## B

**Bit** - La singola cifra binaria, 0 oppure 1. Otto bit fanno un byte.

**BOOTSEL** - Il pulsantino bianco sul Pico. Tenendolo premuto mentre colleghi
l'USB, la scheda si presenta come una chiavetta e puoi installarci il firmware.
(Guida 03)

**Bouncing** (rimbalzo) - Quando premi un pulsante, i contatti metallici
rimbalzano per qualche millisecondo e il Pico legge piu' pressioni invece di
una. (Guida 06)

**Breadboard** (basetta) - La tavoletta bianca piena di fori, per montare
circuiti senza saldare. (Guida 02)

**Buzzer** - Un dischetto che fa rumore. Quello **passivo** suona la nota che
gli mandi, quello **attivo** ne ha una sola. (Guida 07)

## C

**Catodo** - Il lato negativo di un componente polarizzato. Su un LED e' la
zampa corta, dal lato piatto della capsula. (Guida 05)

**Clamping** - Limitare un valore dentro un intervallo, per non mandare un
comando impossibile all'hardware. (Guida 11)

**Condensatore** - Un componente che accumula una piccola quantita' di carica.
Serve a coprire i picchi di assorbimento. Quelli elettrolitici **hanno una
polarita'**: al contrario possono scoppiare.

**Corto circuito** - Quando il `+` e il `-` si toccano direttamente. La
corrente schizza al massimo e qualcosa si rompe.

## D

**Debounce** (antirimbalzo) - La tecnica per ignorare i rimbalzi dei contatti.
Il modo piu' semplice e' aspettare 50 ms dopo aver rilevato una pressione.
(Guida 06)

**Digitale** - Una grandezza che ha solo due valori, 0 o 1. Un pulsante e'
digitale, una manopola no.

**Duty cycle** - Nel PWM, la percentuale di tempo in cui il segnale resta alto.
Su un LED e' la luminosita', su un servo e' la posizione. (Guida 07)

## F

**Firmware** - Il programma di base che fa funzionare un dispositivo. Sul Pico
e' MicroPython, e si installa una volta sola. (Guida 03)

**Flash** - La memoria che conserva i dati anche senza corrente. Il Pico ne ha
2 MB. Anche il verbo *flashare*: scriverci dentro il firmware.

**Fotoresistenza** (LDR) - Un componente la cui resistenza cambia con la luce:
tanta luce = poca resistenza. (Guida 10)

**Frequenza** - Quante volte al secondo si ripete una cosa. Si misura in hertz
(Hz). Su un buzzer, la frequenza e' la nota.

## G

**Git** - Il sistema che tiene la storia delle modifiche al codice. Ogni
*commit* e' un punto di salvataggio a cui puoi tornare. (Guida 09)

**GND** - *Ground*, massa. Lo zero volt, il riferimento di tutto il circuito.
Ogni circuito ha bisogno di una massa in comune.

**GPIO** - *General Purpose Input/Output*. I piedini programmabili. Ognuno puo'
essere ingresso o uscita, e lo decidi tu nel codice. (Guida 01)

## H

**HD44780** - Il controller dentro il display LCD 1602. Progettato da Hitachi
negli anni Ottanta ed e' ancora lo standard. (Guida 13)

## I

**Isteresi** - Usare due soglie invece di una, per evitare che un sistema
oscilli quando il valore e' proprio sul confine. Il termostato di casa accende
a 19 e spegne a 21. (Guida 10)

## L

**LDR** - *Light Dependent Resistor*, la fotoresistenza.

**LED** - *Light Emitting Diode*. Emette luce e **ha un verso**. Vuole sempre
una resistenza in serie. (Guida 05)

## M

**Macchina a stati** - Un modo di organizzare un programma: poche situazioni
possibili e regole precise per passare dall'una all'altra. (Guida 14)

**main.py** - Se un file sul Pico si chiama cosi', parte da solo a ogni
accensione, anche senza PC. (Guida 04)

**Mappatura** - Riportare un numero da un intervallo a un altro. Per esempio da
0-65535 a 0-180 gradi. (Guida 08)

**MicroPython** - Una versione di Python ridotta, fatta per girare su
microcontrollori con pochissima memoria.

**Microcontrollore** - Un chip che contiene processore, memoria e piedini di
ingresso/uscita, tutto insieme. Non ha sistema operativo. Il Pico e' questo.
(Guida 01)

**mpremote** - Lo strumento ufficiale da riga di comando per parlare col Pico.
(Guida 09)

## N

**NeoPixel** - LED RGB con il controller integrato, collegati in catena e
comandati da un filo solo. Il chip si chiama WS2812B. (Guida 12)

**Nibble** - Mezzo byte, quattro bit. Il display LCD ne riceve due per volta.
(Guida 13)

**NTC** - *Negative Temperature Coefficient*. Un termistore la cui resistenza
**scende** quando la temperatura sale. (Guida 10)

## P

**Partitore di tensione** - Due resistenze in serie: nel punto in mezzo c'e'
una tensione che dipende dal loro rapporto. Il modo standard di leggere un
sensore resistivo. (Guida 10)

**PIO** - *Programmable Input/Output*. Piccole macchine a stati dentro l'RP2040
che generano segnali con tempi precisissimi. Fanno funzionare i NeoPixel.
(Guida 12)

**PIR** - Sensore di movimento a infrarossi, la cupoletta bianca. Uscita
digitale: si legge come un pulsante.

**Polarita'** - Il fatto che un componente abbia un verso. LED, condensatori
elettrolitici e diodi ce l'hanno. Resistenze e pulsanti no.

**Potenziometro** - Una resistenza variabile con la manopola. E' un partitore
di tensione regolabile. Il piedino centrale e' sempre il cursore. (Guida 08)

**Pull-up** - Una resistenza che tiene un pin a 3,3V quando non succede niente,
per evitare che fluttui. Il Pico ne ha di interne: si attivano con
`Pin.PULL_UP`. (Guida 06)

**PWM** - *Pulse Width Modulation*. Accendere e spegnere velocissimo per
ottenere valori intermedi. La tecnica piu' utile del percorso. (Guida 07)

## R

**REPL** - *Read-Eval-Print Loop*. Il prompt `>>>` dove scrivi comandi che il
Pico esegue subito. Lo strumento migliore per capire cosa sta succedendo.
(Guida 03)

**Resistenza** - Un componente che limita la corrente. Si legge dalle righe
colorate. Non ha polarita'. (Guida 05, [resistenze.md](resistenze.md))

**RP2040** - Il chip dentro il Pico. Due core ARM a 133 MHz, 264 KB di RAM.

## S

**Servomotore** - Un motore che va a un angolo preciso e ci resta. Si comanda
con impulsi PWM a 50 Hz. L'SG90 fa 0-180 gradi. (Guida 11)

**Soglia** - Il valore oltre il quale il programma cambia comportamento. Va
sempre **tarata** nell'ambiente reale, non copiata da Internet. (Guida 10)

## T

**Termistore** - Una resistenza che cambia con la temperatura. Vedi NTC.

**Thonny** - L'editor Python semplice usato nelle prime guide. (Guida 03)

**Tolleranza** - Di quanto il valore vero di un componente puo' scostarsi da
quello dichiarato. Le resistenze del kit sono al 5%.

## U

**uf2** - Il formato dei file di firmware per il Pico. Si installa
trascinandolo sul disco `RPI-RP2`. (Guida 03)

## V

**VBUS** - Il pin 40, porta i 5V che arrivano dall'USB. Per servo, NeoPixel e
display. **Mai su un GPIO.**

**VSYS** - Il pin 39, l'alimentazione della scheda. Serve per le batterie.

## W

**WS2812B** - Il nome tecnico dei NeoPixel.
