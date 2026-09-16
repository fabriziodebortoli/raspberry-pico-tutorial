# 01 - Cos'e' un Pico

## Obiettivo

Capire che cosa hai in mano. Non accenderemo ancora niente: questa e' la guida
piu' teorica di tutte, ed e' corta apposta.

## Non e' un computer

Il tuo PC ha Windows. Windows e' un sistema operativo: decide quali programmi
girano, gestisce la memoria, disegna le finestre, parla con la rete.

Il Pico **non ha un sistema operativo**. Quando gli dai corrente, esegue
l'unico programma che ha in memoria, dalla prima riga all'ultima. Poi, se il
programma finisce, si ferma e basta. Non c'e' un desktop, non ci sono finestre,
non c'e' niente da chiudere prima di staccare la spina.

Questa e' la differenza tra un **microprocessore** (il tuo PC) e un
**microcontrollore** (il Pico).

| | PC | Pico |
|---|---|---|
| Sistema operativo | Windows | nessuno |
| Programmi in esecuzione | centinaia | uno |
| RAM | 16 GB | 264 KB |
| Memoria di massa | 1 TB SSD | 2 MB flash |
| Velocita' | ~3 GHz | 133 MHz |
| Accende un LED | no | si' |
| Costo | 800 euro | 5 euro |

Guarda l'ultima riga prima di sentirti in imbarazzo per il Pico. Non e' un PC
scarso: e' una cosa diversa, fatta per un lavoro diverso. Il tuo PC non e' in
grado di accendere un LED, e il Pico si'.

E c'e' una cosa che il Pico fa meglio: **il tempo**. Se dici al Pico di
aspettare esattamente 10 microsecondi, aspetta esattamente 10 microsecondi.
Windows non puo' garantirtelo, perche' nel frattempo deve occuparsi di altre
duecento cose.

## Cosa c'e' dentro

Il chip nero quadrato si chiama **RP2040** ed e' progettato da Raspberry Pi.
Contiene:

- **Due core** ARM Cortex-M0+ a 133 MHz. Due, come un PC dual-core, solo molto
  piu' piccoli. Per un bel po' ne useremo uno solo.
- **264 KB di RAM**. Sembrano pochissimi, e lo sono - ma un programma che
  accende un LED ne usa qualche centinaio di byte.
- **26 pin GPIO** programmabili.

Accanto c'e' un secondo chip: **2 MB di memoria flash**. E' l'equivalente del
disco fisso. Li' dentro ci finiranno MicroPython e i tuoi programmi, e ci
restano anche a corrente staccata.

## GPIO, la parola chiave

**GPIO** sta per *General Purpose Input/Output*, cioe' ingresso/uscita di uso
generale. Sono i piedini lungo i bordi della scheda, e sono il motivo per cui
un microcontrollore esiste.

Ogni GPIO puo' fare due cose, e sei tu a decidere quale:

- **Output (uscita)**: il Pico ci mette sopra una tensione. O 3,3V (acceso,
  che in codice scrivi `1`) o 0V (spento, `0`). Cosi' accendi un LED.
- **Input (ingresso)**: il Pico legge che tensione c'e' su quel pin. Cosi' capisce
  se hai premuto un pulsante.

Il pin non e' ne' l'uno ne' l'altro finche' non glielo dici tu. E' la prima
riga di quasi ogni programma che scriverai.

## GP o pin fisico? (la trappola)

Attenzione, perche' qui sbagliano tutti almeno una volta.

Il Pico ha **40 piedini fisici**, numerati da 1 a 40 girando attorno alla
scheda. Ma i nomi che usi nel codice sono i **numeri GP**, da GP0 a GP28. **I
due numeri non coincidono.**

Esempio: il piedino fisico numero 20 si chiama **GP15**. Nel codice scrivi
sempre `Pin(15)`, mai `Pin(20)`.

> **Regola:** nel codice esiste solo il numero **GP**. Il numero fisico serve
> solo per contare i piedini quando guardi la scheda dall'alto.

Tieni aperto il [pinout](../riferimenti/pinout.md), e' la pagina che
consulterai piu' spesso di tutte.

## I pin che non sono GPIO

Non tutti i 40 piedini sono programmabili. Alcuni servono per l'alimentazione:

| Nome | Pin fisico | Cos'e' |
|---|---|---|
| **GND** | 3, 8, 13, 18, 23, 28, 33, 38 | Massa, lo zero. Ce ne sono 8 perche' servono spesso. |
| **3V3 OUT** | 36 | 3,3 volt in uscita. Alimenta i sensori. Max 300 mA. |
| **VBUS** | 40 | I 5 volt che arrivano dall'USB. Per servo e NeoPixel. |
| **VSYS** | 39 | Alimentazione della scheda, se un giorno userai una batteria. |

**I GPIO lavorano a 3,3 volt.** Se ci arriva di piu', il chip si danneggia. E'
la regola numero 3 della guida 00, e ora sai da dove viene.

## Il tuo Pico non ha il WiFi

Esiste un modello che si chiama **Pico W** con WiFi e Bluetooth integrati. Il
tuo e' il Pico base, quindi niente rete: nessun progetto che manda dati su
Internet o che si comanda dal telefono.

Non e' una limitazione grave per adesso. Tutto quello che c'e' da imparare nelle
prossime 13 guide - leggere sensori, pilotare motori, gestire il tempo - si fa
identico su tutte e due le schede. Il giorno che ti serve il WiFi compri un Pico
W da 7 euro e ci sposti sopra il codice quasi senza toccarlo.

## Come fai a riconoscerlo dalla foto

Se un giorno cerchi un tutorial online, controlla che parli del Pico giusto:

- **Pico** (il tuo): micro-USB, nessun modulo argentato sulla scheda
- **Pico W**: micro-USB, un rettangolino argentato in un angolo (l'antenna)
- **Pico 2** / **Pico 2 W**: chip RP2350, piu' recenti

Un tutorial per Pico W che usa `Pin("LED")` funziona anche da te. Uno che usa
`import network` no.

## Prova a rispondere

Non c'e' codice da scrivere, ma queste tre domande te le devi saper rispondere
prima di andare avanti:

1. Se stacchi l'USB mentre il Pico sta contando fino a un milione e poi lo
   ricolleghi, riprende da dov'era o ricomincia da capo?
2. Perche' un pin GPIO non puo' essere ingresso e uscita nello stesso momento?
3. Il piedino fisico 20 nel codice come si chiama?

(Risposte: ricomincia da capo, perche' il programma riparte da zero e la RAM si
svuota. Perche' o e' il Pico che impone una tensione, o e' il mondo esterno:
tutti e due insieme sarebbe un corto. GP15.)

## Prossima guida

[02 - Breadboard e fili](02-breadboard-e-fili.md), dove finalmente tocchi
qualcosa.
