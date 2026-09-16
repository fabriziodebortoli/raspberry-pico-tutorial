# 05 - LED esterno

## Obiettivo

Accendere un LED vero sulla breadboard. Il codice e' quasi identico alla guida
04: quello che cambia, e che conta, e' l'elettronica.

## Ti serve

- 1 LED (rosso, e' il piu' luminoso a parita' di corrente)
- 1 resistenza da **220 ohm** (rosso-rosso-marrone-oro) o **330 ohm**
  (arancione-arancione-marrone-oro)
- 2 jumper
- Il Pico sulla breadboard, con le piste gia' preparate (guida 02)

Non sai leggere le righe colorate? Vedi
[resistenze.md](../riferimenti/resistenze.md).

## Come funziona

### Il LED ha un verso

LED sta per *Light Emitting Diode*, diodo che emette luce. La parola chiave e'
**diodo**: lascia passare la corrente in una direzione sola. Montato al
contrario non si rompe, semplicemente non si accende - il che e' molto piu'
insidioso, perche' pensi di avere un problema nel codice.

Come capisci il verso:

- La **zampetta lunga** e' l'**anodo** (+), va verso il pin del Pico
- La **zampetta corta** e' il **catodo** (-), va verso massa
- Se le zampette sono state tagliate, guarda il bordo della capsula: c'e' un
  **lato piatto**, e quello e' il catodo

```
      ___
     /   \
    |     |     <- capsula trasparente
    |     |
    \_____/
     |   |
     |   |_____ lato PIATTO = catodo (-) = zampetta CORTA = verso GND
     |
     |_________ zampetta LUNGA = anodo (+) = verso il GPIO
```

### Perche' serve la resistenza

Un LED, una volta acceso, si comporta in modo scomodo: **non limita la corrente
che lo attraversa**. Se gli dai 3,3V diretti, assorbe tutta la corrente che
riesce a passare, si scalda e si distrugge in pochi secondi. E rischia di
portarsi dietro il pin del Pico, che regge al massimo circa 12 mA.

La resistenza serve a **limitare la corrente**. Quanta ne serve lo dice la
**legge di Ohm**:

```
V = R x I        ->        R = V / I
```

Nel nostro caso:

- Il Pico fornisce **3,3V**
- Un LED rosso "consuma" circa **2V** (si chiama tensione di soglia, e dipende
  dal colore: rosso ~2V, verde ~2,1V, blu e bianco ~3V)
- Sulla resistenza cade quindi `3,3 - 2 = 1,3V`
- Vogliamo far passare circa **10 mA**, cioe' 0,01 A

```
R = 1,3 / 0,01 = 130 ohm
```

Con 220 ohm passano circa 6 mA: un po' meno luminoso, molto piu' sicuro per il
pin. Nel dubbio si sceglie la resistenza **piu' grande**: al massimo il LED e'
fioco, ma non si brucia niente.

> **Il valore esatto non e' critico.** Qualsiasi cosa tra 150 e 1000 ohm
> funziona. Sotto i 100 ohm inizi a stressare il pin.

## Collegamenti

**Stacca l'USB.**

Il circuito e': GP15 → resistenza → anodo LED → catodo LED → massa.

| # | Da | A |
|---|---|---|
| 1 | riga del **GP15** (pin fisico 20) | una riga libera, es. riga 10 lato A-E |
| 2 | **resistenza**, una zampa | riga 10 (stessa del filo 1) |
| 3 | **resistenza**, altra zampa | riga 15 |
| 4 | **LED anodo** (zampa lunga) | riga 15 (stessa della resistenza) |
| 5 | **LED catodo** (zampa corta) | riga 20 |
| 6 | riga 20 | pista `-` blu (massa) |

```
  GP15 ---[filo]--- riga10 ---[ resistenza ]--- riga15
                                                  |
                                              anodo (lungo)
                                                 LED
                                              catodo (corto)
                                                  |
                                               riga20 ---[filo]--- pista blu (-)
```

Controlla prima di collegare l'USB:

- La zampa lunga del LED e' dal lato della resistenza? 
- Le due zampe del LED sono in **righe diverse**? (se sono nella stessa riga il
  LED e' cortocircuitato e non si accende)
- Il filo nero arriva alla pista blu, e la pista blu e' collegata a un GND del
  Pico?

Adesso collega l'USB.

## Il codice

```python
# 05-led-esterno.py - lampeggia un LED collegato a GP15

from machine import Pin
import time

# Unica differenza rispetto alla guida 04: il numero del pin.
led = Pin(15, Pin.OUT)

while True:
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)
```

E' il codice della guida 04 con `25` diventato `15`. **Questo e' il punto della
guida**: per il Pico, accendere il LED sulla scheda o uno sulla breadboard e'
la stessa identica operazione. Cambia il mondo fuori, non il programma.

## Prova a cambiare

1. **Due LED che si alternano.** Aggiungi un secondo LED su GP14, con la sua
   resistenza (ogni LED ha la sua, sempre). Fai in modo che quando uno e' acceso
   l'altro sia spento, come le frecce di un'auto.

2. **Semaforo.** Tre LED - rosso, giallo, verde - su GP13, GP14, GP15. Ciclo:
   verde 3 secondi, giallo 1 secondo, rosso 3 secondi. Quando lo scrivi, guarda
   quante volte ripeti `value()` e `sleep()`: e' lo stesso segnale della guida
   04 che ti dice che c'e' un modo migliore.

3. **Cambia la resistenza.** Se hai una resistenza da 1000 ohm (marrone-nero-
   rosso), montala al posto di quella da 220 e guarda la differenza di
   luminosita'. Poi calcola quanta corrente passa: `I = 1,3 / 1000`. Quanti
   milliampere sono?

## Se non funziona

| Sintomo | Causa | Come verifichi |
|---|---|---|
| Il LED non si accende mai | E' montato al contrario | Giralo. E' la causa nel 70% dei casi. |
| Il LED non si accende mai | Le due zampe sono nella stessa riga | Devono stare in righe diverse |
| Il LED non si accende mai | Il filo di massa non arriva | Il LED interno (`Pin(25)`) lampeggia? Se si', il codice e' a posto ed e' un problema di fili |
| Il LED non si accende mai | Pista laterale interrotta a meta' | Collega il filo nero direttamente alla riga del GND invece che alla pista |
| Il LED e' fioco | Resistenza troppo grande | Normale con 1k. Con 220 ohm deve essere ben visibile. |
| Il LED e' acceso fisso | Il filo e' su 3V3 invece che su GP15 | Ricontrolla il [pinout](../riferimenti/pinout.md) |
| Il LED si e' spento per sempre e sa di bruciato | Manca la resistenza | Il LED e' andato. Prendine un altro e **metti la resistenza**. |

**Il trucco della diagnosi:** quando qualcosa non va, chiediti sempre "e' il
codice o e' il circuito?". Fai lampeggiare il LED interno insieme a quello
esterno: se quello interno lampeggia e l'altro no, il codice e' giusto e il
problema e' nei fili. Hai dimezzato lo spazio di ricerca con una riga.

## Prossima guida

[06 - Il pulsante](06-pulsante.md): finora il Pico ha solo parlato. Adesso
impara ad ascoltare.
