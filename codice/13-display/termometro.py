# 13 - Termometro con display: unisce la guida 10 e la 13

from machine import ADC, Pin
from lcd1602 import LCD1602
import time
import math

ntc = ADC(Pin(27))
lcd = LCD1602(rs=2, e=3, d4=4, d5=5, d6=6, d7=7)

R_FISSA = 10000
R0 = 10000
T0 = 298.15
BETA = 3950

def leggi_temperatura():
    tensione = ntc.read_u16() * 3.3 / 65535
    resistenza = R_FISSA * (3.3 - tensione) / tensione
    inverso_T = 1 / T0 + (1 / BETA) * math.log(resistenza / R0)
    return 1 / inverso_T - 273.15

lcd.pulisci()
lcd.vai_a(0, 0)
lcd.scrivi("Temperatura:")

while True:
    lcd.vai_a(0, 1)
    # Gli spazi in fondo cancellano i caratteri di una scritta piu' lunga
    lcd.scrivi("{:5.1f} gradi   ".format(leggi_temperatura()))
    time.sleep(1)
