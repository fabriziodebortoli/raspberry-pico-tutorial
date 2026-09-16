# Raspberry Pi Pico - il percorso di Daniele

Benvenuto. Questo repository e' il tuo laboratorio: da una parte le guide per
imparare, dall'altra lo spazio dove costruisci le tue cose.

Il kit e' il **LAFVIN Basic Starter Kit per Raspberry Pi Pico**. Dentro ci sono
una scheda Raspberry Pi Pico, una breadboard, LED, pulsanti, sensori, un
servomotore, una striscia di LED colorati e un display. Tutto quello che serve
per le 15 guide qui sotto.

## Come si usa questo repo

Le guide vanno fatte **in ordine**. Ognuna costruisce su quella prima: se salti
la 05 non capisci perche' nella 06 c'e' una resistenza. Non c'e' fretta, non e'
una gara, e se una guida ti annoia vuol dire che l'hai capita e puoi passare
avanti.

Ogni guida ha sempre la stessa struttura, cosi' sai dove guardare:

1. **Obiettivo** - cosa vedrai succedere quando funziona
2. **Ti serve** - i pezzi da tirare fuori dalla scatola
3. **Come funziona** - la teoria, tenuta corta
4. **Collegamenti** - dove infilare ogni filo, senza ambiguita'
5. **Il codice** - commentato riga per riga
6. **Prova a cambiare** - tre esercizi per smanettare
7. **Se non funziona** - sintomo per sintomo, cosa controllare

## Il percorso

### Parte 1 - Le basi (con Thonny)

| # | Guida | Cosa impari |
|---|---|---|
| 00 | [Unboxing](guide/00-unboxing.md) | cosa c'e' nella scatola e cosa non fare mai |
| 01 | [Cos'e' un Pico](guide/01-cosa-e-un-pico.md) | perche' non e' un computer |
| 02 | [Breadboard e fili](guide/02-breadboard-e-fili.md) | come sono collegati i fori |
| 03 | [Primo avvio](guide/03-primo-avvio.md) | firmware, Thonny, la REPL |
| 04 | [Il LED interno](guide/04-led-interno.md) | il primo programma che accende qualcosa |
| 05 | [LED esterno](guide/05-led-esterno.md) | resistenze, legge di Ohm, polarita' |
| 06 | [Il pulsante](guide/06-pulsante.md) | input, pull-up, rimbalzo dei contatti |
| 07 | [Il buzzer](guide/07-buzzer.md) | PWM, frequenze, una melodia |
| 08 | [Il potenziometro](guide/08-potenziometro.md) | il mondo analogico e l'ADC |

### Parte 2 - Si fa sul serio (con Cursor)

| # | Guida | Cosa impari |
|---|---|---|
| 09 | [Da Thonny a Cursor](guide/09-da-thonny-a-cursor.md) | l'IDE vero, git, l'AI come tutor |
| 10 | [Luce e temperatura](guide/10-luce-e-temperatura.md) | fotoresistenza, NTC, partitore di tensione |
| 11 | [Il servomotore](guide/11-servomotore.md) | PWM per muovere, non per accendere |
| 12 | [I LED NeoPixel](guide/12-neopixel.md) | un protocollo dati su un filo solo |
| 13 | [Il display LCD](guide/13-display-lcd.md) | la guida piu' difficile, 6 fili di dati |
| 14 | [Progetto finale](guide/14-progetto-finale.md) | tutto insieme: senti, decidi, agisci |

## Le altre cartelle

- **[codice/](codice/)** - il programma finito di ogni guida, gia' pronto.
  Usalo per confrontare, non per copiare: se copi prima di aver provato, hai
  perso il pomeriggio.
- **[riferimenti/](riferimenti/)** - roba da consultare al volo: il
  [pinout](riferimenti/pinout.md), il [codice colori delle
  resistenze](riferimenti/resistenze.md), il [glossario](riferimenti/glossario.md)
  e i [problemi comuni](riferimenti/problemi-comuni.md).
- **[progetti-daniele/](progetti-daniele/)** - tuo. Qui dentro fai quello che
  vuoi.

## Regola numero uno

**Stacca sempre l'USB prima di cambiare i fili.** Non e' una precauzione da
paranoici: e' il modo piu' facile per non bruciare niente. Il Pico costa poco,
ma restare senza nel mezzo di un progetto e' una scocciatura.

## Regola numero due

Quando qualcosa non funziona, non ricominciare da capo. Leggi
[problemi-comuni.md](riferimenti/problemi-comuni.md), poi la sezione "Se non
funziona" della guida. Nel 90% dei casi e' un filo nella riga sbagliata o un LED
girato. Capire **perche'** non funzionava vale piu' di dieci programmi che
funzionano al primo colpo.
