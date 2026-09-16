# Pinout del Raspberry Pi Pico

La pagina che consulterai piu' spesso. Tienila aperta in una scheda.

## Come si legge

Tieni il Pico con la **presa USB in alto**. I piedini fisici si numerano
partendo dall'angolo **in alto a sinistra** (pin 1), scendendo lungo il lato
sinistro fino al pin 20, poi si risale dal basso a destra (pin 21) fino al pin
40 in alto a destra.

**Nel codice usi sempre il numero `GP`, mai il numero fisico.**

```
                      +-----------+
                      |    USB    |
          +-----------+-----------+-----------+
   GP0  1 | o                             o | 40  VBUS  (5V)
   GP1  2 | o                             o | 39  VSYS
   GND  3 | o                             o | 38  GND
   GP2  4 | o                             o | 37  3V3_EN
   GP3  5 | o                             o | 36  3V3 OUT  (3,3V)
   GP4  6 | o                             o | 35  ADC_VREF
   GP5  7 | o         RP2040              o | 34  GP28 / ADC2
   GND  8 | o                             o | 33  AGND
   GP6  9 | o                             o | 32  GP27 / ADC1
   GP7 10 | o                             o | 31  GP26 / ADC0
   GP8 11 | o                             o | 30  RUN
   GP9 12 | o                             o | 29  GP22
   GND 13 | o                             o | 28  GND
  GP10 14 | o                             o | 27  GP21
  GP11 15 | o                             o | 26  GP20
  GP12 16 | o                             o | 25  GP19
  GP13 17 | o                             o | 24  GP18
   GND 18 | o                             o | 23  GND
  GP14 19 | o                             o | 22  GP17
  GP15 20 | o                             o | 21  GP16
          +-------------------------------+
```

## Alimentazione

| Nome | Pin fisico | Cos'e' | Quando lo usi |
|---|---|---|---|
| **3V3 OUT** | 36 | 3,3V in uscita | sensori, potenziometri, partitori. **Max 300 mA.** |
| **VBUS** | 40 | 5V dall'USB | servo, NeoPixel, display LCD |
| **VSYS** | 39 | alimentazione della scheda | se un giorno userai una batteria |
| **GND** | 3, 8, 13, 18, 23, 28, 33, 38 | massa | dappertutto |
| **RUN** | 30 | reset | portandolo a massa il Pico si riavvia |

**I GPIO lavorano a 3,3V.** Non collegare mai VBUS o un segnale a 5V su un
pin GP: il chip si danneggia.

## I pin analogici

Solo tre pin sanno leggere tensioni analogiche:

| Pin GP | Pin fisico | Canale |
|---|---|---|
| GP26 | 31 | ADC0 |
| GP27 | 32 | ADC1 |
| GP28 | 34 | ADC2 |
| *(interno)* | - | ADC4 = sensore di temperatura del chip |

Su tutti gli altri pin `ADC(Pin(n))` da' errore.

## I pin che non ci sono

GP23, GP24 e GP25 **non sono sui connettori**. Sono usati internamente:

| | A cosa serve |
|---|---|
| GP23 | controllo del regolatore di alimentazione |
| GP24 | rileva se l'USB e' collegato |
| **GP25** | **il LED sulla scheda** (guida 04) |

## Chi usa cosa nelle guide

Lo schema che seguono le guide, cosi' puoi montare tutto insieme senza
conflitti:

| Pin GP | Pin fisico | Componente | Guida |
|---|---|---|---|
| GP2 | 4 | LCD `RS` | 13 |
| GP3 | 5 | LCD `E` | 13 |
| GP4 | 6 | LCD `D4` | 13 |
| GP5 | 7 | LCD `D5` | 13 |
| GP6 | 9 | LCD `D6` | 13 |
| GP7 | 10 | LCD `D7` | 13 |
| GP14 | 19 | LED bianco | 05, 14 |
| GP15 | 20 | LED rosso | 05, 14 |
| GP16 | 21 | pulsante / servo | 06, 11 |
| GP17 | 22 | NeoPixel `DIN` | 12 |
| GP18 | 24 | buzzer | 07 |
| GP20 | 26 | pulsante A | 14 |
| GP21 | 27 | pulsante B | 14 |
| GP25 | *interno* | LED della scheda | 04 |
| GP26 | 31 | potenziometro / fotoresistenza | 08, 10 |
| GP27 | 32 | termistore NTC | 10 |

Nota che GP16 compare due volte: nella guida 06 e' il pulsante, nella 11 e' il
servo. Nel progetto finale (guida 14) i pulsanti si spostano su GP20 e GP21
proprio per liberarlo.

## Limiti da rispettare

| Limite | Valore |
|---|---|
| Tensione su un GPIO | **3,3V massimi** |
| Corrente da un singolo GPIO | ~12 mA (assoluto massimo 16) |
| Corrente totale da tutti i GPIO | ~50 mA |
| Corrente dal pin 3V3 OUT | **300 mA** |
| Corrente da VBUS | quella che regge la porta USB, circa 500 mA |

Se un progetto ha bisogno di piu' corrente (motori, tanti NeoPixel), serve
un'alimentazione esterna.

## Link utili

- Pinout ufficiale: <https://pico.raspberrypi.com/>
- Datasheet del Pico: <https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf>
- Documentazione MicroPython per RP2: <https://docs.micropython.org/en/latest/rp2/quickref.html>
