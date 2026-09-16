# 03 - Primo avvio

## Obiettivo

Installare MicroPython sul Pico, installare Thonny sul PC e far scrivere al
Pico la sua prima parola. Alla fine di questa guida il Pico esegue comandi che
gli dai tu, uno alla volta.

## Ti serve

- Il Pico montato sulla breadboard (guida 02)
- Il cavo micro-USB
- Il PC con Windows e una connessione a Internet

## Come funziona

Il Pico appena uscito dalla scatola e' vuoto: non sa cosa sia Python. Ci devi
mettere dentro **MicroPython**, che e' una versione ridotta di Python fatta per
girare in 264 KB di RAM.

Questo si chiama **flashare il firmware** e si fa **una volta sola**. Poi il
Pico parla Python per sempre.

Il modo in cui si flasha e' furbo: il Pico si finge una chiavetta USB, tu ci
copi dentro un file, e lui capisce che e' un firmware e se lo installa da solo.
Niente driver, niente programmi speciali.

## Passo 1 - Scarica MicroPython

Vai su **https://micropython.org/download/RPI_PICO/** e scarica l'ultimo file
`.uf2` dalla sezione in cima alla pagina.

> Controlla l'indirizzo: deve essere `RPI_PICO`. Se scarichi `RPI_PICO_W` o
> `RPI_PICO2` il firmware e' per un'altra scheda e non funziona. Sono errori
> facilissimi da fare e difficili da capire dopo.

Il file si chiama tipo `RPI_PICO-20260xxx-v1.2x.x.uf2` e pesa un paio di
megabyte. Tienitelo da parte nella cartella Download.

## Passo 2 - Metti il Pico in modalita' BOOTSEL

Qui l'ordine delle operazioni conta. Fallo esattamente cosi':

1. **Stacca l'USB** dal Pico, se e' collegato.
2. **Tieni premuto** il pulsantino bianco `BOOTSEL` sulla scheda.
3. **Mentre lo tieni premuto**, collega il cavo USB al PC.
4. Conta fino a due, poi **rilascia** il pulsante.

Se ha funzionato, su Windows compare un **disco rimovibile** chiamato
`RPI-RP2`. Aprilo: dentro ci sono due file, `INDEX.HTM` e `INFO_UF2.TXT`. Non
servono a niente, servivano solo a farti capire che ci sei riuscito.

Se non compare niente, salta alla sezione "Se non funziona" in fondo.

## Passo 3 - Copia il firmware

Trascina il file `.uf2` che hai scaricato dentro il disco `RPI-RP2`.

Guarda bene cosa succede: dopo un secondo il disco **sparisce da solo**. Non e'
un errore. Il Pico ha ricevuto il firmware, si e' riavviato e adesso non e' piu'
una chiavetta - e' un dispositivo che parla Python.

Se Windows ti mostra un avviso tipo "dispositivo rimosso in modo imprevisto",
ignoralo tranquillamente.

**Il firmware e' installato.** Non dovrai rifarlo mai piu', a meno che un
giorno non voglia aggiornarlo.

## Passo 4 - Installa Thonny

Thonny e' un editor Python semplice, pensato per chi impara, e sa parlare con
il Pico senza configurazioni.

Scaricalo da **https://thonny.org** e installalo con le impostazioni di
default.

> Perche' Thonny e non Cursor, visto che Cursor ce l'hai gia'? Perche' per le
> prime guide quello che conta e' che tu scriva ogni riga con le tue mani, e
> Thonny non ha completamento automatico che ti finisce il codice al posto tuo.
> Dalla guida 09 si passa a Cursor, quando i concetti base sono tuoi.

## Passo 5 - Collega Thonny al Pico

Apri Thonny. In basso a destra c'e' una scritta tipo **"Python locale 3.x"** o
**"Local Python 3"**. Cliccaci sopra: si apre un menu con i dispositivi
disponibili.

Scegli **"MicroPython (Raspberry Pi Pico)"**.

Nel riquadro in basso, che si chiama **Shell**, deve comparire qualcosa del
genere:

```
MicroPython v1.2x.x on 2026-xx-xx; Raspberry Pi Pico with RP2040
Type "help()" for more information.
>>>
```

Quel `>>>` e' la cosa piu' importante di tutta la guida.

## Cos'e' la REPL

Quel `>>>` e' il prompt della **REPL**, che sta per *Read-Eval-Print Loop*:
legge quello che scrivi, lo esegue, stampa il risultato, e torna in attesa.

E' una riga di comando, ma verso il Pico. Quello che scrivi li' **viene
eseguito subito sulla scheda**, senza salvare niente.

E' lo strumento piu' utile che hai per capire cosa sta succedendo. Quando un
programma non funziona, la REPL ti fa provare un pezzetto alla volta.

## Il primo comando

Clicca nella Shell, accanto a `>>>`, scrivi questo e premi Invio:

```python
print("Ciao Daniele")
```

Il Pico risponde:

```
Ciao Daniele
```

Piccolo momento da notare: quel testo non l'ha scritto il tuo PC. L'ha scritto
un chip da 5 euro grande come una moneta, che ha eseguito Python e ha rimandato
indietro il risultato sul cavo USB.

## Prova a cambiare

Rimani nella REPL e prova questi, uno alla volta:

1. Usa il Pico come calcolatrice: `2 + 2`, poi `17 / 5`, poi `17 // 5`. Che
   differenza c'e' tra le ultime due?

2. Scrivi `help()` e premi Invio. Ti si apre un aiuto interattivo. Per uscire,
   scrivi `q` oppure premi `Ctrl+D`.

3. Chiedigli quanta memoria gli e' rimasta:

   ```python
   import gc
   gc.mem_free()
   ```

   Ti risponde con un numero di byte liberi. Dividilo per 1024 per avere i KB.
   Confrontalo con i 16 GB del tuo PC.

4. Prova a rompere qualcosa di proposito: scrivi `print("ciao"` senza chiudere
   la parentesi. Leggi il messaggio di errore. Imparare a leggere gli errori
   adesso, quando sai gia' qual e' il problema, e' un investimento.

## Se non funziona

| Sintomo | Causa | Soluzione |
|---|---|---|
| Il disco `RPI-RP2` non compare | Non hai tenuto BOOTSEL abbastanza, o l'hai premuto dopo aver collegato l'USB | Stacca tutto. Tieni premuto **prima**, collega **dopo**. |
| Il disco non compare comunque | Il cavo e' solo da ricarica | Prova un altro cavo micro-USB. Deve essere un cavo dati. |
| Thonny non elenca il Pico | Il firmware non e' stato installato | Rifai i passi 2 e 3. Se il disco `RPI-RP2` ricompare, il firmware non c'era. |
| Thonny non elenca il Pico ma il firmware c'e' | Porta COM occupata | Chiudi altri programmi che usano la seriale. In casi ostinati, riavvia Thonny. |
| La Shell resta vuota, nessun `>>>` | La connessione si e' persa | Nel menu di Thonny: **Esegui > Interrompi/Riavvia backend**, oppure `Ctrl+F2`. |
| Compaiono caratteri strampalati | Interferenza sulla seriale | Stacca e ricollega l'USB, poi riavvia il backend. |
| `>>>` c'e' ma non risponde ai comandi | Un programma precedente e' rimasto in loop | Premi `Ctrl+C` nella Shell per fermarlo. |

**`Ctrl+C` nella Shell ferma qualsiasi programma in esecuzione sul Pico.**
Segnatelo, ti servira' spessissimo dalla guida 04 in poi.

## Prossima guida

[04 - Il LED interno](04-led-interno.md). Adesso che il Pico esegue comandi,
facciamogli accendere qualcosa.
