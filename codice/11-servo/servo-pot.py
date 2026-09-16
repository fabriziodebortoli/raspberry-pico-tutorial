# 11 - Il potenziometro comanda l'angolo del servo

from machine import ADC, Pin, PWM
import time

pot = ADC(Pin(26))
servo = PWM(Pin(16))
servo.freq(50)

def vai_a(gradi):
    if gradi < 0:
        gradi = 0
    if gradi > 180:
        gradi = 180
    servo.duty_ns(500_000 + (gradi * 2_000_000 // 180))

while True:
    valore = pot.read_u16()
    angolo = valore * 180 // 65535
    vai_a(angolo)
    time.sleep(0.02)
