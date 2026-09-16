# 11 - Comanda il servo in gradi, con spazzata avanti e indietro

from machine import Pin, PWM
import time

servo = PWM(Pin(16))
servo.freq(50)               # 50 Hz FISSI: il servo vuole questa frequenza

def vai_a(gradi):
    """Muove il servo all'angolo indicato, da 0 a 180 gradi."""
    if gradi < 0:
        gradi = 0
    if gradi > 180:
        gradi = 180
    # 0 gradi -> impulso da 0,5 ms; 180 gradi -> impulso da 2,5 ms
    servo.duty_ns(500_000 + (gradi * 2_000_000 // 180))

while True:
    for angolo in range(0, 181, 5):
        vai_a(angolo)
        time.sleep(0.02)
    for angolo in range(180, -1, -5):
        vai_a(angolo)
        time.sleep(0.02)
