# 07 - Suona una scala di DO maggiore

from machine import Pin, PWM
import time

buzzer = PWM(Pin(18))

note = [262, 294, 330, 349, 392, 440, 494, 523]
nomi = ["DO", "RE", "MI", "FA", "SOL", "LA", "SI", "DO"]

for i in range(len(note)):
    print(nomi[i], note[i], "Hz")
    buzzer.freq(note[i])
    buzzer.duty_u16(32768)
    time.sleep(0.4)

buzzer.duty_u16(0)
buzzer.deinit()
