# 06 - Il LED e' acceso mentre tieni premuto il pulsante

from machine import Pin

led = Pin(15, Pin.OUT)
pulsante = Pin(16, Pin.IN, Pin.PULL_UP)

while True:
    if pulsante.value() == 0:      # 0 = premuto (logica invertita del pull-up)
        led.value(1)
    else:
        led.value(0)
