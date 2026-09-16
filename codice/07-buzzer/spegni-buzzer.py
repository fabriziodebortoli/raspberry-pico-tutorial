# 07 - Da eseguire quando il buzzer e' rimasto acceso e non la smette

from machine import Pin, PWM

PWM(Pin(18)).deinit()
print("Buzzer spento")
