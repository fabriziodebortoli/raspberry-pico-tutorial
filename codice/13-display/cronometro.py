# 13 - Conta i secondi dall'accensione

from lcd1602 import LCD1602
import time

lcd = LCD1602(rs=2, e=3, d4=4, d5=5, d6=6, d7=7)

lcd.pulisci()
lcd.vai_a(0, 0)
lcd.scrivi("Acceso da:")

secondi = 0
while True:
    # Non chiamo pulisci() a ogni giro: farebbe sfarfallare il display.
    # Riposiziono il cursore e sovrascrivo.
    lcd.vai_a(0, 1)
    lcd.scrivi("{:02d}:{:02d}".format(secondi // 60, secondi % 60))
    time.sleep(1)
    secondi = secondi + 1
