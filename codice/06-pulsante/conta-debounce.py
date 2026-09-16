# 06 - Conta le pressioni, con antirimbalzo

from machine import Pin
import time

pulsante = Pin(16, Pin.IN, Pin.PULL_UP)
conteggio = 0
stato_precedente = 1

while True:
    stato = pulsante.value()
    if stato == 0 and stato_precedente == 1:
        conteggio = conteggio + 1
        print("Premuto", conteggio, "volte")
        time.sleep(0.05)           # 50 ms: copre i rimbalzi dei contatti
    stato_precedente = stato
