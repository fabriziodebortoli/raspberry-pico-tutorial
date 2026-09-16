# 10 - Lampione automatico con isteresi: accende il LED quando c'e' buio

from machine import ADC, Pin
import time

ldr = ADC(Pin(26))
led = Pin(15, Pin.OUT)

# TARA QUESTI DUE NUMERI nella tua stanza, usando leggi-luce.py
SOGLIA_ACCENDI = 18000
SOGLIA_SPEGNI = 25000

acceso = False

while True:
    luce = ldr.read_u16()
    if not acceso and luce < SOGLIA_ACCENDI:
        acceso = True
    elif acceso and luce > SOGLIA_SPEGNI:
        acceso = False
    led.value(1 if acceso else 0)
    print(luce, "acceso" if acceso else "spento")
    time.sleep(0.05)
