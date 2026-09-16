# 08 - Legge il potenziometro e lo stampa in percentuale

from machine import ADC, Pin
import time

pot = ADC(Pin(26))

while True:
    valore = pot.read_u16()
    percento = valore * 100 // 65535
    print(valore, "->", percento, "%")
    time.sleep(0.2)
