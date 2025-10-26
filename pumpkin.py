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
low0 = t0.read() + 500
low1 = t1.read() + 500
low2 = t2.read() + 500
low3 = t3.read() + 500
low4 = t4.read() + 500
low5 = t5.read() + 500
low6 = t6.read() + 500
low7 = t7.read() + 500
low8 = t8.read() + 500
low9 = t9.read() + 500
low10 = t10.read() + 500

pins = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]
lows = [low0, low1, low2, low3, low4, low5, low6, low7, low8, low9, low10]
while True:
    for i in range (0,11):
        if (pins[i].read() > (lows[i]):
            print(i, " pressed")
        print(i, ": ", (pins[i]).read())
    time.sleep(1)
