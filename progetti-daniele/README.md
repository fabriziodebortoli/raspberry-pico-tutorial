# I progetti di Daniele

Questa cartella e' tua. Le guide sono materiale da leggere, questo e' lo spazio
dove costruisci.

## Come organizzarti

Una cartella per progetto, con dentro il codice e un `README.md` che spiega
cos'e'. Copia `_template/` quando ne inizi uno nuovo.

```
progetti-daniele/
  antifurto-camera/
    README.md
    main.py
  timer-pomodoro/
    README.md
    timer.py
```

Il `README.md` non e' burocrazia: fra tre mesi non ti ricorderai come avevi
collegato i fili, e quel file e' l'unica cosa che te lo dira'.

## Le regole (poche)

**Fai un commit ogni volta che qualcosa funziona.** Non alla fine della serata:
ogni volta che una cosa comincia a girare.

```bash
git add progetti-daniele/
git commit -m "L'antifurto ora suona quando passa qualcuno"
git push
```

Scrivi **cosa hai fatto** nel messaggio, non "modifiche" o "prova". Tra due
mesi la differenza si vede.

**Se un progetto non funziona, committalo lo stesso.** Un progetto rotto con
scritto `README.md` "il servo trema, non ho capito perche'" vale piu' di un
progetto cancellato.

**Non serve che i progetti siano finiti.** Meta' delle cose che si iniziano si
abbandonano, ed e' normale. Anche quelle abbandonate ti hanno insegnato
qualcosa.

## Se non sai cosa fare

Qualche idea, in ordine di difficolta':

| Progetto | Cosa serve | Guide |
|---|---|---|
| Dado elettronico | 7 LED, 1 pulsante | 05, 06 |
| Timer da cucina | display, 2 pulsanti, buzzer | 06, 07, 13 |
| Antifurto per la camera | PIR, buzzer, LED | 06, 07 |
| Termometro da scrivania | NTC, display | 10, 13 |
| Luce notturna automatica | LDR, NeoPixel | 10, 12 |
| Gioco dei riflessi | LED, pulsante, display | 06, 13 |
| Metronomo regolabile | potenziometro, buzzer | 07, 08 |
| Barra VU per la musica | NeoPixel, potenziometro | 08, 12 |
| Sbarra automatica | PIR, servo, LED | 10, 11 |
| Simon (gioco di memoria) | 4 LED, 4 pulsanti, buzzer | 05, 06, 07 |

Il gioco dei riflessi e' un ottimo primo progetto: e' semplice, ma ti obbliga a
misurare il tempo davvero, ed e' divertente da far provare agli altri.

## Chiedere aiuto

In questo repository c'e' un file `AGENTS.md` che dice all'AI di Cursor di
farti da tutor invece che da risolutore: ti fa domande, non ti scrive il
codice.

Se vuoi che ti dia la risposta e basta, glielo puoi chiedere, e lo fara'. Ma
pensaci un secondo prima: nei **tuoi** progetti la differenza tra aver capito e
aver copiato la senti eccome.
