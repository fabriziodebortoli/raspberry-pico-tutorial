# 12 - Un puntino luminoso che scorre avanti e indietro

from machine import Pin
import neopixel
import time

NUM_LED = 8
np = neopixel.NeoPixel(Pin(17), NUM_LED)

def spegni_tutti():
    for i in range(NUM_LED):
        np[i] = (0, 0, 0)

while True:
    for posizione in range(NUM_LED):
        spegni_tutti()
        np[posizione] = (0, 30, 0)
        np.write()
        time.sleep(0.08)
    for posizione in range(NUM_LED - 2, 0, -1):
        spegni_tutti()
        np[posizione] = (0, 30, 0)
        np.write()
        time.sleep(0.08)
