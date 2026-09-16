# 13 - Il primo testo sul display
# Ricordati di caricare PRIMA lcd1602.py sul Pico!

from lcd1602 import LCD1602

lcd = LCD1602(rs=2, e=3, d4=4, d5=5, d6=6, d7=7)

lcd.pulisci()
lcd.vai_a(0, 0)
lcd.scrivi("Ciao Daniele!")
lcd.vai_a(0, 1)
lcd.scrivi("Funziona :)")
