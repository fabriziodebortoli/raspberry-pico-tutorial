# 04 - SOS in codice Morse sul LED interno

from machine import Pin
import time

led = Pin(25, Pin.OUT)

CORTO = 0.2
LUNGO = 0.6

def lampeggia(durata, quante):
    for i in range(quante):
        led.value(1)
        time.sleep(durata)
        led.value(0)
        time.sleep(CORTO)

while True:
    lampeggia(CORTO, 3)     # S
    time.sleep(0.4)
    lampeggia(LUNGO, 3)     # O
    time.sleep(0.4)
    lampeggia(CORTO, 3)     # S
    time.sleep(2)
