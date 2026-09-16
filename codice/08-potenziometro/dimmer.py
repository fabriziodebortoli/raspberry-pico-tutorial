# 08 - La manopola regola la luminosita' del LED su GP15

from machine import ADC, Pin, PWM
import time

pot = ADC(Pin(26))
led = PWM(Pin(15))
led.freq(1000)

while True:
    valore = pot.read_u16()
    led.duty_u16(valore)      # read_u16 e duty_u16 hanno la stessa scala
    time.sleep(0.02)
