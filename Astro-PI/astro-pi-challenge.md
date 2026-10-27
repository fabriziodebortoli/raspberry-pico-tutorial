# Astro Pi - il tuo codice sulla Stazione Spaziale

Ogni anno l'**ESA** (l'Agenzia Spaziale Europea) e la **Raspberry Pi
Foundation** organizzano la **European Astro Pi Challenge**. E' una gara per
ragazzi fino a 19 anni. L'idea e' semplice: tu scrivi un programma in Python,
e se rispetta le regole **gira davvero a bordo della ISS**, la Stazione
Spaziale Internazionale, a 400 km sopra la tua testa.

Non e' una simulazione. Il programma lo carica l'ESA su un computer che sta
fisicamente sulla stazione, e poi ti rimanda i dati raccolti.

## Cos'e' un Astro Pi

Sulla ISS ci sono due computer chiamati **Astro Pi**. Dentro c'e' un Raspberry
Pi, non un Pico. La differenza la conosci gia' dalla [guida 01](../guide/01-cosa-e-un-pico.md):
il Pico e' un microcontrollore, il Raspberry Pi e' un computer vero con un
sistema operativo. Quindi sull'Astro Pi si usa **Python normale**, non
MicroPython. La sintassi e' la stessa che usi tu, cambiano solo le librerie.

Sopra il Raspberry Pi c'e' una scheda chiamata **Sense HAT**, con:

- una matrice di **8x8 LED colorati** (64 pixel, come la tua striscia NeoPixel
  ma a quadrato)
- sensori di **temperatura, umidita' e pressione**
- un **accelerometro**, un **giroscopio** e un **magnetometro** (una bussola)
- un **sensore di colore**, che misura il colore della luce intorno
- un joystick

In piu' c'e' una **fotocamera** puntata verso la Terra da un oblo'.

## Le due missioni

### Mission Zero - arte in orbita

E' la missione facile, pensata per chi inizia. Scrivi un programma che
disegna un'immagine sulla matrice 8x8. Quest'anno il tema e' la **natura**.
Il disegno deve usare il **sensore di colore**: il programma legge il colore
della luce nella stazione e cambia l'immagine di conseguenza. Gli astronauti
lo vedono mentre lavorano.

Si fa in un pomeriggio, anche da solo. Il programma lo scrivi e lo provi nel
browser, senza hardware. Tutti i programmi validi vengono fatti girare sulla
ISS e ricevi un certificato.

### Mission Space Lab - scienza vera

Qui si fa sul serio. Serve una **squadra da 2 a 6 ragazzi**. Dovete inventare
un esperimento scientifico, oppure seguire una delle guide pronte, e scrivere
un programma che **registra dati** dai sensori o dalla fotocamera in un file.

Ogni programma che passa i controlli ha diritto a **10 minuti di volo** sulla
ISS. A giugno vi arrivano i dati veri raccolti in orbita, e li potete
analizzare.

Per provare il codice c'e' **Astro Pi Replay**: uno strumento online che fa
girare il programma con dati storici veri della ISS (foto, letture dei
sensori). C'e' anche un plugin per **Thonny**, che conosci gia'.

## Le date da ricordare

| Quando | Cosa |
|---|---|
| 14 settembre 2026 | apertura iscrizioni per entrambe le missioni |
| 1 ottobre 2026, 15:00 | livestream "Getting started with Mission Space Lab" |
| 22 febbraio 2027, 12:00 | chiusura consegne Mission Space Lab |
| 22 marzo 2027 | chiusura consegne Mission Zero |
| aprile - maggio 2027 | i programmi girano sulla ISS |
| giugno 2027 | arrivano dati e certificati, Q&A con un esperto ESA |

Per iscriversi serve un adulto che fa da **mentore** e registra la squadra
sul Mission Hub del sito [astro-pi.org](https://astro-pi.org). Le regole
precise (quanto puo' durare il programma, quanti file puo' scrivere, quali
librerie sono ammesse) stanno sul sito e cambiano un po' ogni anno. Leggile
prima di iniziare, non dopo.

## Cosa ti porti dietro dal Pico

Piu' di quanto pensi. Hai gia' acceso LED con tuple RGB nella [guida 12](../guide/12-neopixel.md),
hai letto sensori e convertito valori grezzi in numeri sensati nella
[guida 10](../guide/10-luce-e-temperatura.md), e hai strutturato un programma
lungo nella [guida 14](../guide/14-progetto-finale.md). L'Astro Pi e' la
stessa cosa, solo che il laboratorio e' in orbita.

---

## Tre esempi di progetto

Sono idee per capire cosa si puo' fare, non soluzioni da copiare. Il codice
e' uno schizzo: mostra le librerie e la forma del programma, il resto e'
lavoro tuo.

### Esempio 1 - Una foglia che segue la luce (Mission Zero)

**L'idea.** Sulla matrice disegni una foglia 8x8. Il colore dello sfondo
dipende dalla luce che il sensore misura nella stazione. Se la luce e'
calda, lo sfondo diventa arancione come un tramonto. Se e' fredda, diventa
azzurro come il cielo. Per un tocco in piu', la foglia puo' "crescere" di un
pixel alla volta.

**Cosa impari.** Liste di 64 elementi, tuple RGB, lettura di un sensore.
E' quasi la [guida 12](../guide/12-neopixel.md) disposta a quadrato.

```python
from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

# Il sensore di colore va "tarato" prima di leggerlo
sense.color.gain = 60
sense.color.integration_cycles = 64

# Leggo il colore della luce nella stazione
luce = sense.color
sfondo = (luce.red, luce.green, luce.blue)

v = (0, 150, 0)   # verde foglia
s = sfondo        # sfondo che cambia

# 64 pixel, riga per riga dall'alto in basso
foglia = [
    s, s, s, s, s, s, s, s,
    s, s, s, v, v, s, s, s,
    # ... le altre 6 righe le disegni tu
]

sense.set_pixels(foglia)
```

**Domande da farti.** Cosa succede se la luce e' quasi buia e tutti e tre i
valori sono vicini a zero? Lo sfondo si vedrebbe ancora? Come faresti a
schiarirlo senza perdere la sfumatura?

### Esempio 2 - Quanto va veloce la ISS? (Mission Space Lab)

**L'idea.** E' la sfida classica degli ultimi anni. La fotocamera scatta due
foto della Terra a pochi secondi di distanza. Nelle due foto si trovano gli
stessi punti (una costa, un'isola, una nuvola). Si misura di quanti pixel si
sono spostati. Sapendo quanti metri di terreno corrispondono a un pixel, e
quanti secondi sono passati tra le foto, si calcola la velocita'.

```
velocita' = distanza percorsa / tempo trascorso
```

Il valore vero e' circa **7,66 km/s**, cioe' oltre 27.000 km/h. Il bello e'
vedere quanto ci arrivi vicino con due foto e un po' di matematica.

**Cosa impari.** Elaborazione di immagini con la libreria **OpenCV**, che
trova da sola i "punti notevoli" in due foto e li accoppia. Poi media dei
risultati e scarto dei valori assurdi, cioe' un po' di statistica vera.

```python
from picamzero import Camera
from time import sleep

camera = Camera()

# Due foto a 5 secondi di distanza
camera.take_photo("foto1.jpg")
sleep(5)
camera.take_photo("foto2.jpg")

# Da qui in poi:
# 1. OpenCV trova i punti in comune tra foto1 e foto2
# 2. calcoli lo spostamento medio in pixel
# 3. pixel -> metri -> km/s
```

**Domande da farti.** Se una nuvola si muove per conto suo mentre la ISS
passa sopra, cosa succede al calcolo? E se la foto e' tutta mare, senza
niente di riconoscibile? Come te ne accorgi dal programma?

### Esempio 3 - La bussola in orbita (Mission Space Lab)

**L'idea.** Il magnetometro misura il campo magnetico terrestre. Sulla
Terra lo usi come bussola, ma in orbita la ISS fa un giro completo del
pianeta ogni 90 minuti circa. In 10 minuti percorre piu' di 4.500 km.
Registrando il campo magnetico insieme alla **posizione** della stazione,
potete vedere come cambia sopra l'oceano, sopra l'equatore o vicino ai poli.

**Cosa impari.** Registrare dati in un file **CSV** (un file di testo con i
valori separati da virgole, che poi apri in Excel). Gestire il tempo: il
programma deve fermarsi da solo prima che scadano i 10 minuti, altrimenti
viene interrotto. E' una macchina a stati come nella
[guida 14](../guide/14-progetto-finale.md), con uno stato "registra" e uno
stato "ho finito".

```python
from sense_hat import SenseHat
from orbit import ISS
from datetime import datetime, timedelta
from time import sleep

sense = SenseHat()
inizio = datetime.now()
durata = timedelta(minutes=9)   # margine di sicurezza sui 10 minuti

with open("dati.csv", "w") as file:
    file.write("ora,latitudine,longitudine,x,y,z\n")

    while datetime.now() < inizio + durata:
        posizione = ISS.coordinates()
        campo = sense.get_compass_raw()
        # ... scrivi una riga nel file con questi valori
        sleep(10)
```

**Domande da farti.** Ogni quanti secondi conviene leggere il sensore?
Troppo spesso e il file diventa enorme, troppo di rado e vi perdete i
cambiamenti. E cosa succede ai valori se un astronauta passa vicino con un
attrezzo di metallo?

---

## Da dove partire

Se e' la prima volta, fai **Mission Zero**: e' breve, la fai da solo e ti
serve per prendere confidenza con il Sense HAT. Se ti piace, per **Mission
Space Lab** cerca uno o due compagni di classe con cui fare squadra. Il
livestream del **1 ottobre** e' un buon modo per capire come funziona senza
leggere tutto il regolamento in inglese.

Tutto parte da [astro-pi.org](https://astro-pi.org).
