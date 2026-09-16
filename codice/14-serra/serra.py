# 14 - Serra automatica
#
# Legge temperatura e luce, decide se aprire la finestrella, comanda servo,
# LED e buzzer, e mostra tutto sul display.
#
# Struttura del ciclo principale:  LEGGI -> DECIDI -> AGISCI -> MOSTRA
#
# Serve lcd1602.py caricato sul Pico (vedi guida 13).

from machine import ADC, Pin, PWM
from lcd1602 import LCD1602
import time
import math

# ----------------------------------------------------------------------
# CONFIGURAZIONE
# Tutti i numeri regolabili stanno qui, non sparsi nel codice.
# ----------------------------------------------------------------------

PIN_NTC = 27
PIN_LDR = 26
PIN_SERVO = 16
PIN_LED_ROSSO = 15
PIN_LED_BIANCO = 14
PIN_BUZZER = 18
PIN_PULSANTE_A = 20
PIN_PULSANTE_B = 21

# Soglie di temperatura in gradi centigradi.
# Tra CHIUDI e APRI c'e' la zona morta che evita l'oscillazione (isteresi).
TEMP_APRI = 26.0
TEMP_CHIUDI = 22.0
TEMP_ALLARME = 32.0

# Soglia di luce. TARALA nella tua stanza con codice/10-sensori/leggi-luce.py
SOGLIA_BUIO = 18000

# Angoli del servo
ANGOLO_CHIUSO = 0
ANGOLO_APERTO = 90
ANGOLO_ALLARME = 180

# Costanti del termistore (vedi guida 10)
R_FISSA = 10000
R0 = 10000
T0 = 298.15
BETA = 3950

# ----------------------------------------------------------------------
# HARDWARE
# ----------------------------------------------------------------------

ntc = ADC(Pin(PIN_NTC))
ldr = ADC(Pin(PIN_LDR))

servo = PWM(Pin(PIN_SERVO))
servo.freq(50)

led_rosso = Pin(PIN_LED_ROSSO, Pin.OUT)
led_bianco = Pin(PIN_LED_BIANCO, Pin.OUT)

buzzer = PWM(Pin(PIN_BUZZER))
buzzer.duty_u16(0)

pulsante_a = Pin(PIN_PULSANTE_A, Pin.IN, Pin.PULL_UP)
pulsante_b = Pin(PIN_PULSANTE_B, Pin.IN, Pin.PULL_UP)

lcd = LCD1602(rs=2, e=3, d4=4, d5=5, d6=6, d7=7)

# ----------------------------------------------------------------------
# STATO
# Il programma ricorda in che situazione si trova. Non lo ricalcola
# da zero ogni giro: e' proprio la memoria dello stato che fa l'isteresi.
# ----------------------------------------------------------------------

stato = "chiusa"          # "chiusa", "aperta", "allarme"
modo_manuale = False
schermata = 0             # 0 = temperatura, 1 = luce, 2 = stato

_a_precedente = 1
_b_precedente = 1

# ----------------------------------------------------------------------
# 1. LEGGI - interroga i sensori. Non decide e non comanda niente.
# ----------------------------------------------------------------------

def leggi_temperatura():
    """Restituisce la temperatura in gradi centigradi."""
    tensione = ntc.read_u16() * 3.3 / 65535
    if tensione <= 0 or tensione >= 3.3:
        return 0.0                      # sensore scollegato: evita la divisione per zero
    resistenza = R_FISSA * (3.3 - tensione) / tensione
    inverso_T = 1 / T0 + (1 / BETA) * math.log(resistenza / R0)
    return 1 / inverso_T - 273.15


def leggi_luce():
    """Restituisce la luce come numero grezzo da 0 a 65535."""
    return ldr.read_u16()


def controlla_pulsanti():
    """Aggiorna schermata e modo manuale in base ai pulsanti."""
    global schermata, modo_manuale, stato, _a_precedente, _b_precedente

    a = pulsante_a.value()
    if a == 0 and _a_precedente == 1:
        schermata = (schermata + 1) % 3
        lcd.pulisci()
        time.sleep(0.05)
    _a_precedente = a

    b = pulsante_b.value()
    if b == 0 and _b_precedente == 1:
        modo_manuale = not modo_manuale
        if modo_manuale:
            # In manuale: se e' chiusa apri, se e' aperta chiudi
            stato = "aperta" if stato == "chiusa" else "chiusa"
        time.sleep(0.05)
    _b_precedente = b

# ----------------------------------------------------------------------
# 2. DECIDI - guarda i numeri e aggiorna lo stato. Non tocca l'hardware.
# ----------------------------------------------------------------------

def aggiorna_stato(temperatura):
    """Decide il nuovo stato in base alla temperatura."""
    global stato

    if modo_manuale:
        return                          # in manuale comanda l'utente

    if temperatura > TEMP_ALLARME:
        stato = "allarme"
    elif stato == "allarme" and temperatura < TEMP_ALLARME - 2:
        stato = "aperta"                # isteresi anche sull'allarme
    elif stato == "chiusa" and temperatura > TEMP_APRI:
        stato = "aperta"
    elif stato == "aperta" and temperatura < TEMP_CHIUDI:
        stato = "chiusa"

# ----------------------------------------------------------------------
# 3. AGISCI - comanda l'hardware in base allo stato. Non decide niente.
# ----------------------------------------------------------------------

def servo_vai_a(gradi):
    """Muove il servo, con protezione sui limiti meccanici."""
    if gradi < 0:
        gradi = 0
    if gradi > 180:
        gradi = 180
    servo.duty_ns(500_000 + (gradi * 2_000_000 // 180))


def applica_stato():
    """Traduce lo stato in comandi verso servo, LED e buzzer."""
    if stato == "chiusa":
        servo_vai_a(ANGOLO_CHIUSO)
        led_rosso.value(0)
        buzzer.duty_u16(0)
    elif stato == "aperta":
        servo_vai_a(ANGOLO_APERTO)
        led_rosso.value(1)
        buzzer.duty_u16(0)
    elif stato == "allarme":
        servo_vai_a(ANGOLO_ALLARME)
        led_rosso.toggle()              # lampeggia
        buzzer.freq(880)
        buzzer.duty_u16(20000)

# ----------------------------------------------------------------------
# 4. MOSTRA - scrive sul display. Non tocca nient'altro.
# ----------------------------------------------------------------------

def aggiorna_display(temperatura, luce):
    """Disegna la schermata corrente."""
    if schermata == 0:
        lcd.vai_a(0, 0)
        lcd.scrivi("Temperatura     ")
        lcd.vai_a(0, 1)
        lcd.scrivi("{:5.1f} gradi    ".format(temperatura))
    elif schermata == 1:
        lcd.vai_a(0, 0)
        lcd.scrivi("Luce            ")
        lcd.vai_a(0, 1)
        buio = "BUIO " if luce < SOGLIA_BUIO else "CHIARO"
        lcd.scrivi("{:5d} {:6s}   ".format(luce, buio))
    else:
        lcd.vai_a(0, 0)
        lcd.scrivi("Stato: {:8s}".format(stato.upper()))
        lcd.vai_a(0, 1)
        lcd.scrivi("Modo: {:10s}".format("MANUALE" if modo_manuale else "AUTO"))

# ----------------------------------------------------------------------
# CICLO PRINCIPALE
# Resterebbe di queste dimensioni anche con il triplo dei sensori,
# perche' la complessita' sta dentro le funzioni.
# ----------------------------------------------------------------------

lcd.pulisci()
lcd.vai_a(0, 0)
lcd.scrivi("Serra di Daniele")
lcd.vai_a(0, 1)
lcd.scrivi("avvio...")
time.sleep(2)
lcd.pulisci()

try:
    while True:
        # 1. LEGGI
        temperatura = leggi_temperatura()
        luce = leggi_luce()
        controlla_pulsanti()

        # 2. DECIDI
        aggiorna_stato(temperatura)

        # 3. AGISCI
        applica_stato()
        led_bianco.value(1 if luce < SOGLIA_BUIO else 0)

        # 4. MOSTRA
        aggiorna_display(temperatura, luce)

        time.sleep(0.1)

except KeyboardInterrupt:
    # Ctrl+C: spegni tutto per bene invece di lasciare il buzzer acceso
    buzzer.duty_u16(0)
    buzzer.deinit()
    servo.duty_ns(0)
    servo.deinit()
    led_rosso.value(0)
    led_bianco.value(0)
    lcd.pulisci()
    lcd.vai_a(0, 0)
    lcd.scrivi("Fermato.")
    print("Serra fermata, tutto spento.")
