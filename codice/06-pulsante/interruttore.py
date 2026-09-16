# 06 - Una pressione accende, la successiva spegne

from machine import Pin
import time

led = Pin(15, Pin.OUT)
pulsante = Pin(16, Pin.IN, Pin.PULL_UP)
stato_precedente = 1

while True:
    stato = pulsante.value()
    if stato == 0 and stato_precedente == 1:
        led.toggle()
        time.sleep(0.05)
    stato_precedente = stato
