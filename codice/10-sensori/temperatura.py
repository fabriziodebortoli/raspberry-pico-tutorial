# 10 - Il termistore NTC convertito in gradi centigradi

from machine import ADC, Pin
import time
import math

ntc = ADC(Pin(27))

R_FISSA = 10000       # la resistenza fissa del partitore
R0 = 10000            # resistenza dell'NTC a 25 gradi
T0 = 298.15           # 25 gradi in kelvin
BETA = 3950           # parametro del componente

while True:
    lettura = ntc.read_u16()
    tensione = lettura * 3.3 / 65535
    resistenza = R_FISSA * (3.3 - tensione) / tensione
    inverso_T = 1 / T0 + (1 / BETA) * math.log(resistenza / R0)
    celsius = 1 / inverso_T - 273.15
    print(round(celsius, 1), "gradi  (R =", int(resistenza), "ohm)")
    time.sleep(1)
