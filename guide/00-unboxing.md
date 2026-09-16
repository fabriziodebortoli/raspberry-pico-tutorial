# 00 - Unboxing

## Obiettivo

Aprire la scatola, capire cosa hai in mano e non rompere niente nei primi
cinque minuti. Alla fine di questa guida non avrai ancora collegato nulla, e va
benissimo cosi'.

## Cosa c'e' nella scatola

Svuota tutto su un tavolo, possibilmente non di vetro e non su un tappeto.
Dovresti trovare:

**La scheda**

- 1 **Raspberry Pi Pico** con i piedini gia' saldati. E' il rettangolino verde
  con il chip nero quadrato al centro e la presa micro-USB su un lato.
- 1 cavo **micro-USB**. Attenzione: micro, non USB-C. Se ne hai in giro di
  vecchi, molti sono solo da ricarica e non passano dati - usa quello del kit.

**Dove si monta tutto**

- 1 **breadboard** (basetta) da 830 fori, quella bianca piena di buchi
- 1 mazzetto di **jumper** maschio-maschio, i fili colorati con gli spilli alle
  due estremita'

**Cose che si accendono**

- LED rossi, gialli e verdi (quelli piccoli e trasparenti con due zampette)
- 1 **striscia NeoPixel** con LED RGB indirizzabili
- 1 **display LCD 1602**, il rettangolo nero con lo schermo blu

**Cose che sentono**

- 2 **fotoresistenze** (LDR), tondine con una serpentina sopra
- 1 **termistore NTC**, sembra una perlina
- 1 **sensore di fiamma** (il modulo blu con il LED scuro)
- 1 **sensore di movimento PIR**, la cupoletta bianca
- 1 **potenziometro**, la manopolina blu

**Cose che si muovono o fanno rumore**

- 1 **servomotore SG90**, il cubetto blu con le alette di plastica
- 2 **buzzer**, i dischetti neri

**Componenti passivi**

- Un sacchetto di **resistenze**, con le righe colorate
- Qualche **condensatore** e un paio di **transistor**
- 8 **pulsanti** (tastini quadrati) con i cappucci colorati

Se manca qualcosa, non e' un dramma: le prime dieci guide usano LED,
resistenze, pulsanti, buzzer e potenziometro.

## Le tre cose da non fare mai

Queste tre regole valgono da qui alla fine. Impararle adesso ti risparmia un
Pico bruciato.

### 1. Mai cambiare i fili con l'USB collegato

Stacca sempre il cavo prima di toccare la breadboard. Se sposti un filo mentre
la scheda e' alimentata e per sbaglio tocchi il pin sbagliato, il danno e'
istantaneo e irreversibile.

### 2. Mai un LED senza resistenza

Un LED collegato direttamente assorbe tutta la corrente che riesce, si scalda e
muore. Con lui rischia anche il pin del Pico. Vedremo nella guida 05 come
calcolare quella giusta, per ora sappi solo che ci vuole **sempre**.

### 3. Mai collegare il pin 5V a un pin GPIO

Il Pico lavora a **3,3 volt**. Il pin VBUS porta i 5 volt che arrivano
dall'USB. Se quei 5V finiscono su un piedino GPIO, il chip si danneggia. Nelle
guide dove serve il 5V (servo e NeoPixel) ti diro' esattamente dove metterlo.

## Un minuto sull'elettricita' statica

Quando cammini sul tappeto e poi tocchi una maniglia e senti la scossa, quella
e' elettricita' statica. Sono migliaia di volt, e a un chip non fanno bene.

Non serve diventare paranoici. Basta che **prima di prendere in mano il Pico
tocchi qualcosa di metallo collegato a terra** - un termosifone, la scocca di
un PC acceso. E prendi la scheda dai bordi, non dai piedini.

## Guarda bene il tuo Pico

Prendilo in mano (bordi!) e cercagli sopra queste cose:

- Il **chip quadrato nero** al centro con scritto `RP2040`. E' il cervello.
- Il **chip piu' piccolo** rettangolare vicino: e' la memoria flash, dove
  finiranno i tuoi programmi.
- Un **pulsantino bianco** in alto con scritto `BOOTSEL`. Lo useremo nella
  guida 03 e mai piu'.
- Un **LED minuscolo** vicino alla presa USB. E' il LED interno, il
  protagonista della guida 04.
- I **numeri stampati** lungo entrambi i bordi. Sono i nomi dei piedini, ci
  torniamo nella guida 01.

Nota che sul Pico **non c'e' un interruttore di accensione**. Si accende quando
colleghi l'USB e si spegne quando lo stacchi. Non c'e' un "arresta il sistema":
e' normale, e la guida 01 spiega perche'.

## Se non funziona

Qui non c'e' ancora niente che possa non funzionare. Ma due controlli sensati:

| Problema | Cosa fare |
|---|---|
| I piedini del Pico non sono saldati | Se sono in una striscia a parte, serve un saldatore. Chiedi a tuo padre prima di procedere. |
| Il cavo micro-USB non entra bene | Guarda il verso: il connettore micro-USB e' trapezoidale, entra in un solo modo. Non forzare. |
| La breadboard ha la pellicola adesiva sotto | Lasciala. Non attaccarla a niente per ora. |

## Prossima guida

[01 - Cos'e' un Pico](01-cosa-e-un-pico.md), dove scopri perche' questa cosa
non e' un computer e perche' e' proprio questo il bello.
