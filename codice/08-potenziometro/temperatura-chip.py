# 08 - Il sensore di temperatura nascosto dentro l'RP2040 (canale ADC 4)

from machine import ADC
import time

sensore = ADC(4)

while True:
    lettura = sensore.read_u16() * 3.3 / 65535
    temperatura = 27 - (lettura - 0.706) / 0.001721
    print(round(temperatura, 1), "gradi (temperatura del CHIP, non dell'aria)")
    time.sleep(1)
