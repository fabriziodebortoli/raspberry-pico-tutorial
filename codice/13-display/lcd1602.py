# lcd1602.py - libreria per display LCD 16x2 con controller HD44780
#
# Collegamento a 4 bit: servono 6 pin GPIO (RS, E, D4, D5, D6, D7).
# Il pin RW del display va collegato FISSO A MASSA: questa libreria
# scrive soltanto, non legge mai.
#
# Uso:
#     from lcd1602 import LCD1602
#     lcd = LCD1602(rs=2, e=3, d4=4, d5=5, d6=6, d7=7)
#     lcd.pulisci()
#     lcd.vai_a(0, 0)
#     lcd.scrivi("Ciao")

from machine import Pin
import time


class LCD1602:

    def __init__(self, rs, e, d4, d5, d6, d7):
        self.rs = Pin(rs, Pin.OUT)
        self.e = Pin(e, Pin.OUT)
        # I quattro pin dati, in ordine dal bit meno significativo
        self.dati = [
            Pin(d4, Pin.OUT),
            Pin(d5, Pin.OUT),
            Pin(d6, Pin.OUT),
            Pin(d7, Pin.OUT),
        ]

        self.rs.value(0)
        self.e.value(0)

        # Il display appena alimentato ha bisogno di tempo per svegliarsi.
        time.sleep_ms(50)

        # Sequenza di risveglio dal manuale Hitachi HD44780.
        # I tempi NON sono decorativi: sono i minimi richiesti dal chip.
        # Se li togli funziona a volte si' e a volte no, che e' peggio.
        self._nibble(0x03)
        time.sleep_ms(5)
        self._nibble(0x03)
        time.sleep_us(150)
        self._nibble(0x03)
        time.sleep_us(150)
        self._nibble(0x02)        # da qui in poi si parla a 4 bit
        time.sleep_us(150)

        self._comando(0x28)       # 4 bit, 2 righe, caratteri 5x8
        self._comando(0x08)       # display spento
        self._comando(0x01)       # pulisci
        time.sleep_ms(2)          # il comando "pulisci" e' lento: 1,52 ms
        self._comando(0x06)       # il cursore avanza da solo dopo ogni carattere
        self._comando(0x0C)       # display acceso, cursore nascosto

    def _nibble(self, valore):
        """Mette 4 bit sui pin dati e da' l'impulso di enable."""
        for i in range(4):
            self.dati[i].value((valore >> i) & 1)
        self.e.value(1)
        time.sleep_us(1)
        self.e.value(0)
        time.sleep_us(100)

    def _comando(self, valore):
        """Manda un byte di comando (RS=0), in due nibble."""
        self.rs.value(0)
        self._nibble(valore >> 4)
        self._nibble(valore & 0x0F)
        time.sleep_us(50)

    def _carattere(self, valore):
        """Manda un byte da stampare (RS=1), in due nibble."""
        self.rs.value(1)
        self._nibble(valore >> 4)
        self._nibble(valore & 0x0F)
        time.sleep_us(50)

    # ---- metodi pubblici ----

    def pulisci(self):
        """Cancella lo schermo e riporta il cursore in alto a sinistra."""
        self._comando(0x01)
        time.sleep_ms(2)

    def vai_a(self, colonna, riga):
        """Sposta il cursore. Colonne 0-15, righe 0-1."""
        # La riga 0 comincia all'indirizzo 0x00, la riga 1 a 0x40.
        # Non sono consecutive: e' una stranezza dell'HD44780.
        inizio = [0x00, 0x40]
        self._comando(0x80 | (inizio[riga] + colonna))

    def scrivi(self, testo):
        """Scrive una stringa a partire dalla posizione del cursore."""
        for carattere in testo:
            self._carattere(ord(carattere))

    def display(self, acceso):
        """Accende o spegne la scritta (non la retroilluminazione)."""
        self._comando(0x0C if acceso else 0x08)
