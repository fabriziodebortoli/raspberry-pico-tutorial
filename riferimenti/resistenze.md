# Leggere le resistenze

Le resistenze non hanno il valore scritto sopra: sono troppo piccole. Il valore
si legge dalle **righe colorate**.

## Da che parte si legge

La riga **oro** (o argento) e' la tolleranza e sta **a destra**. Gira la
resistenza in modo da avere l'oro dalla tua parte destra, e leggi da sinistra.

Se non c'e' l'oro, guarda quale estremo ha la riga piu' vicina al bordo: si
parte da li'.

## Il codice a 4 righe

```
   ||||
   ||||___ 4a riga: TOLLERANZA (oro = 5%)
   |||____ 3a riga: MOLTIPLICATORE (quanti zeri aggiungere)
   ||_____ 2a riga: seconda CIFRA
   |______ 1a riga: prima CIFRA
```

| Colore | Cifra | Moltiplicatore |
|---|---|---|
| Nero | 0 | x1 |
| Marrone | 1 | x10 |
| Rosso | 2 | x100 |
| Arancione | 3 | x1.000 |
| Giallo | 4 | x10.000 |
| Verde | 5 | x100.000 |
| Blu | 6 | x1.000.000 |
| Viola | 7 | - |
| Grigio | 8 | - |
| Bianco | 9 | - |
| **Oro** | - | tolleranza 5% |
| **Argento** | - | tolleranza 10% |

## Come si fa in pratica

**Rosso, rosso, marrone, oro:**

- rosso = 2
- rosso = 2
- marrone = x10
- quindi `22 x 10 = 220 ohm`

**Marrone, nero, arancione, oro:**

- marrone = 1
- nero = 0
- arancione = x1.000
- quindi `10 x 1000 = 10.000 ohm = 10 kohm`

## Le quattro che ti servono davvero

Nelle guide ne usi solo queste. Impara a riconoscere queste e stai a posto.

| Valore | Colori | Dove la usi |
|---|---|---|
| **220 ohm** | rosso, rosso, marrone, oro | LED (guida 05), retroilluminazione LCD (13) |
| **330 ohm** | arancione, arancione, marrone, oro | LED, alternativa ai 220 |
| **1 kohm** | marrone, nero, rosso, oro | LED molto fioco, prove |
| **10 kohm** | marrone, nero, arancione, oro | partitori di tensione (guida 10) |

> **Trucco per non confondersi:** 220 ohm e 10 kohm sono le uniche due che usi
> spesso, e si distinguono a colpo d'occhio. La 220 comincia con **due righe
> rosse**, la 10k comincia con **marrone e nero**. Se le tieni in due bustine
> separate fin dall'inizio, ti risparmi un sacco di tempo.

## Le resistenze a 5 righe

Alcune resistenze di precisione hanno cinque righe: le prime **tre** sono
cifre, la quarta e' il moltiplicatore, la quinta la tolleranza.

Come le distingui: se ci sono cinque righe e l'ultima e' marrone o rossa
(invece di oro), e' una a 5 righe.

Esempio: marrone, nero, nero, rosso, marrone = `100 x 100 = 10.000 ohm`, sempre
10 kohm.

## Se non riesci a leggerle

Capita a tutti, specie con le resistenze piccole dove i colori sono sbiaditi o
il marrone sembra rosso sotto la luce artificiale. Due soluzioni:

1. **Guardale alla luce del giorno**, vicino a una finestra. La luce calda
   delle lampadine falsa il rosso e l'arancione.
2. **Usa un multimetro**, se ce l'hai in casa. Metti la manopola sul simbolo
   dell'ohm, tocca le due zampe con i puntali, leggi il numero. E' il modo piu'
   veloce e non sbaglia mai.

## La resistenza non ha polarita'

Al contrario del LED, la resistenza puoi montarla in qualunque verso. Non c'e'
un `+` e un `-`.

## Perche' proprio questi valori

I valori non sono arbitrari: esiste una serie standard, la **E12**, con dodici
valori per decade:

```
10  12  15  18  22  27  33  39  47  56  68  82
```

Poi si moltiplica per 10, 100, 1000... Per questo esistono resistenze da 220 e
da 330 ma non da 250 o da 300. Quando in un progetto leggi "servono 275 ohm",
in pratica ci metti 270 o 330 e funziona uguale.
