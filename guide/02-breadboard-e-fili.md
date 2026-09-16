# 02 - Breadboard e fili

## Obiettivo

Capire come sono collegati i fori della breadboard e montarci sopra il Pico.
Alla fine di questa guida hai la base pronta per tutte le guide successive, e
non la smonterai piu'.

## Ti serve

- La breadboard
- Il Pico
- 2 jumper (uno rosso e uno nero, se ce li hai)

## Come funziona

La breadboard serve a collegare componenti **senza saldare**. Sotto ogni fila
di fori c'e' una molletta metallica: quando ci infili un piedino, la molletta
lo stringe e lo collega elettricamente agli altri fori della stessa fila.

Il punto e' capire **quali fori sono collegati tra loro**. Sono due schemi
diversi sulla stessa basetta.

### Le piste di alimentazione (i bordi)

Lungo i due bordi lunghi ci sono due coppie di file marcate `+` (riga rossa) e
`-` (riga blu).

Queste file sono collegate **in orizzontale**, per tutta la lunghezza della
basetta. Tutti i fori della riga rossa sono lo stesso punto elettrico. Idem per
la blu.

Servono a distribuire alimentazione e massa dappertutto senza tirare venti fili
dal Pico.

> **Attenzione:** su molte breadboard da 830 fori le piste laterali sono
> **interrotte a meta'**. Guarda la riga rossa: se vedi uno stacco nella linea
> stampata circa a meta' basetta, sono due tratti separati. Se hai dubbi,
> nella guida 05 ti faccio verificare con un LED.

### Il campo centrale (le colonne)

La parte grossa in mezzo e' divisa da un **canale** (la scanalatura al centro).
Le file sono marcate con le lettere `A`-`E` da un lato e `F`-`J` dall'altro, e
con i numeri `1`-`63` lungo la basetta.

Qui i fori sono collegati **in verticale**, a gruppi di cinque, e **il canale
interrompe il collegamento**.

Quindi, alla riga 12:

- `A12 B12 C12 D12 E12` sono tutti lo stesso punto elettrico
- `F12 G12 H12 I12 J12` sono tutti lo stesso punto elettrico
- ma il gruppo di sinistra e quello di destra **non sono collegati** tra loro

```
          riga 12
             |
   +  -      v
   o  o   o o o o o     <- A B C D E  (collegati tra loro)
   o  o   o o o o o
   o  o  ============   <- il canale separa i due lati
   o  o   o o o o o     <- F G H I J  (collegati tra loro)
   o  o   o o o o o
   ^
   piste di alimentazione (collegate in orizzontale)
```

### Perche' esiste il canale

Perche' i chip come il Pico si montano **a cavallo** del canale. Cosi' la fila
di piedini di sinistra finisce nei gruppi `A-E` e quella di destra nei gruppi
`F-J`, e le due file non si toccano.

Se non ci fosse il canale, ogni piedino sarebbe in corto con quello di fronte e
non funzionerebbe niente.

## Montaggio: il Pico sulla breadboard

**Stacca l'USB** (non e' ancora collegato, ma prendi l'abitudine).

1. Metti la breadboard davanti a te in orizzontale, con i numeri che vanno da
   sinistra a destra.
2. Prendi il Pico dai bordi, con la **presa USB rivolta a sinistra**.
3. Appoggialo a cavallo del canale, allineando i piedini ai fori. Parti dalla
   riga 1 o giu' di li', in modo che tutta la scheda stia sulla basetta.
4. Premi **dritto, deciso e uniforme**, tenendo le dita sui bordi lunghi. Non
   premere sul chip nero. Se senti che un piedino si piega, fermati, solleva e
   riallinea.

Ci vuole piu' forza di quanto immagini la prima volta. E' normale.

Quando e' in sede, controlla di lato che sia parallelo alla basetta e che nessun
piedino sia rimasto fuori o piegato sotto.

> **Da ora in poi lascialo li'.** Si toglie e si rimette parecchie volte prima
> che un piedino ceda.

## La notazione dei collegamenti (importante)

Da qui in avanti tutte le guide indicano i collegamenti cosi':

| Da | A |
|---|---|
| GP15 | riga del GP15, stesso lato |

Cosa vuol dire: **ogni piedino del Pico e' elettricamente unito agli altri
quattro fori della sua stessa riga, sul suo lato del canale.**

Quindi per collegare un filo a GP15 non devi infilarlo dentro il Pico: **lo
infili in un foro libero della riga dove sta GP15**, dallo stesso lato.

Uso questa notazione invece dei numeri assoluti (tipo "foro C12") perche' a
seconda di dove hai appoggiato il Pico i numeri cambiano, ma la riga del GP15
e' sempre la riga del GP15. Cosi' funziona comunque.

Per trovare la riga di un GP: conta i piedini sulla scheda partendo dall'angolo
con l'USB, oppure guarda il [pinout](../riferimenti/pinout.md). Le scritte sono
stampate sul Pico stesso, ma una volta montato sulla breadboard non si leggono
piu' - un motivo in piu' per tenere aperto il pinout.

## Prepara le due piste

Questo lo fai una volta sola e ti serve per sempre.

**Stacca l'USB.** Poi:

| Da | A | Filo |
|---|---|---|
| riga del 3V3 OUT (pin fisico 36) | pista `+` rossa | rosso |
| riga di un GND qualsiasi (es. pin fisico 38) | pista `-` blu | nero |

Adesso hai 3,3V disponibili su tutta la riga rossa e massa su tutta la riga
blu, in qualunque punto della basetta. Quasi ogni circuito delle prossime
guide li usa.

> **Convenzione dei colori:** rosso = positivo, nero = massa, altri colori =
> segnali. Non e' obbligatorio, il rame non sa di che colore e' la plastica.
> Ma quando hai quindici fili sulla basetta e qualcosa non va, essere stato
> ordinato e' l'unica cosa che ti salva.

## Prova a cambiare

1. Guarda la tua breadboard e conta: quanti punti elettrici distinti ci sono in
   tutto il campo centrale? (Suggerimento: 63 righe, due lati.)
2. Se infili due fili in `A5` e `E5`, sono collegati? E in `E5` e `F5`?
3. Perche' le piste di alimentazione sono in orizzontale e le colonne in
   verticale, e non tutte nello stesso verso?

(Risposte: 126. Si' i primi, no i secondi perche' c'e' il canale in mezzo.
Perche' l'alimentazione serve ovunque mentre ogni componente ha bisogno del suo
punto isolato.)

## Se non funziona

| Sintomo | Causa probabile |
|---|---|
| Il Pico non entra, i piedini non si allineano | Non e' centrato sul canale, o e' storto di una riga. Solleva e riprova. |
| Un piedino si e' piegato sotto la scheda | Togli il Pico, raddrizzalo delicatamente con una pinzetta, rimonta. |
| Il Pico entra solo da un lato | Stai premendo storto. Premi al centro dei due bordi lunghi insieme. |
| Un jumper non sta fermo nel foro | Lo spillo e' piegato o il foro e' allargato. Cambia jumper, cambia foro. |

## Prossima guida

[03 - Primo avvio](03-primo-avvio.md): colleghiamo l'USB e installiamo
MicroPython.
