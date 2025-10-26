from machine import TouchPad, Pin
import time

t0 = TouchPad(Pin(11))
t1 = TouchPad(Pin(12))
t2 = TouchPad(Pin(13))
t3 = TouchPad(Pin(14))
t4 = TouchPad(Pin(1))
t5 = TouchPad(Pin(2))
t6 = TouchPad(Pin(3))
t7 = TouchPad(Pin(4))
t8 = TouchPad(Pin(5))
t9 = TouchPad(Pin(6))
t10 = TouchPad(Pin(7))

pins = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]
while True:
    for i in range (0,11):
        print(i, ": ", (pins[i]).read())
    time.sleep(1)
