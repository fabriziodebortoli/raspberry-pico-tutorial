# 07 - Fra Martino sul buzzer passivo

from machine import Pin, PWM
import time

buzzer = PWM(Pin(18))

DO = 262
RE = 294
MI = 330
FA = 349
SOL = 392
PAUSA = 0

melodia = [
    (DO, 0.4), (RE, 0.4), (MI, 0.4), (DO, 0.4),
    (DO, 0.4), (RE, 0.4), (MI, 0.4), (DO, 0.4),
    (MI, 0.4), (FA, 0.4), (SOL, 0.8),
    (MI, 0.4), (FA, 0.4), (SOL, 0.8),
]

def suona(frequenza, durata):
    if frequenza == PAUSA:
        buzzer.duty_u16(0)
    else:
        buzzer.freq(frequenza)
        buzzer.duty_u16(32768)
    time.sleep(durata)
    buzzer.duty_u16(0)
    time.sleep(0.05)

for nota, durata in melodia:
    suona(nota, durata)

buzzer.deinit()
