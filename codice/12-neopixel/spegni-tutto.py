# 12 - Spegne tutti i NeoPixel. Utile quando restano accesi.

from machine import Pin
import neopixel

NUM_LED = 8
np = neopixel.NeoPixel(Pin(17), NUM_LED)

for i in range(NUM_LED):
    np[i] = (0, 0, 0)
np.write()
print("NeoPixel spenti")
