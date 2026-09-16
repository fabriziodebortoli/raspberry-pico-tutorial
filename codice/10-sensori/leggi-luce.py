# 10 - Lettura grezza della fotoresistenza. Serve per tarare le soglie.

from machine import ADC, Pin
import time

ldr = ADC(Pin(26))

while True:
    print("Luce:", ldr.read_u16())
    time.sleep(0.3)
