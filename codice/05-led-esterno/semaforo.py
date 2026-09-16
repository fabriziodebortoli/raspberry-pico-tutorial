# 05 - Semaforo con tre LED su GP13, GP14, GP15

from machine import Pin
import time

rosso = Pin(13, Pin.OUT)
giallo = Pin(14, Pin.OUT)
verde = Pin(15, Pin.OUT)

def solo(acceso, durata):
    rosso.value(1 if acceso == "rosso" else 0)
    giallo.value(1 if acceso == "giallo" else 0)
    verde.value(1 if acceso == "verde" else 0)
    time.sleep(durata)

while True:
    solo("verde", 3)
    solo("giallo", 1)
    solo("rosso", 3)
