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

NUM_TOUCH_PINS = 11

NOTES = [261.63,277.18,293.66,311.13,329.63,349.23,369.99,392.0,415.3,440.0,446.16,493.88]
for i in range(0,len(NOTES)):
    NOTES.append(NOTES[i] * 2)
    
NOTES = NOTES[0:22]

RANGE = "LOW" #LOW for one ESP32, HIGH for the other

if RANGE == "LOW":
    NOTES = NOTES[0:11]
else:
    NOTES = NOTES[11:22]

while True:
    for i in range (0, NUM_TOUCH_PINS):
        if (pins[i].read()) > (lows[i]):
            print(i, " pressed")
        print(i, ": ", (pins[i]).read())
    time.sleep(0.1)
