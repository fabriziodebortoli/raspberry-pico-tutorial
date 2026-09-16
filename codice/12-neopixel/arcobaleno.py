# 12 - Arcobaleno che scorre sulla striscia NeoPixel

from machine import Pin
import neopixel
import time

NUM_LED = 8
LUMINOSITA = 0.12          # NON alzare troppo: assorbe corrente e abbaglia

np = neopixel.NeoPixel(Pin(17), NUM_LED)

def ruota(posizione):
    """Da un numero 0-255 restituisce un colore dell'arcobaleno."""
    posizione = posizione % 255
    if posizione < 85:
        return (255 - posizione * 3, posizione * 3, 0)
    elif posizione < 170:
        posizione = posizione - 85
        return (0, 255 - posizione * 3, posizione * 3)
    else:
        posizione = posizione - 170
        return (posizione * 3, 0, 255 - posizione * 3)

def attenua(colore, fattore):
    r, g, b = colore
    return (int(r * fattore), int(g * fattore), int(b * fattore))

offset = 0
while True:
    for i in range(NUM_LED):
        np[i] = attenua(ruota(i * 255 // NUM_LED + offset), LUMINOSITA)
    np.write()             # senza questa riga non succede NIENTE
    offset = offset + 3
    time.sleep(0.03)
