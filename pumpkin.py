from machine import TouchPad, Pin
import time
from machine import Pin, I2S
import math
import struct
from time import sleep

SAMPLE_RATE = 8000
BYTES_PER_SAMPLE = 2

sck_pin = Pin(15) # Serial clock (BCLK on breakout)
ws_pin = Pin(16) # Word select (LRCLK on breakout)
sd_pin = Pin(17) # Serial data (DIN on breakout)

t0 = TouchPad(Pin(1))
t1 = TouchPad(Pin(2))
t2 = TouchPad(Pin(3))
t3 = TouchPad(Pin(4))
t4 = TouchPad(Pin(5))
t5 = TouchPad(Pin(6))
t6 = TouchPad(Pin(7))
t7 = TouchPad(Pin(11))
t8 = TouchPad(Pin(12))
t9 = TouchPad(Pin(13))
t10 = TouchPad(Pin(14))

add_to_low = 5000
low0 = t0.read() + add_to_low
low1 = t1.read() + add_to_low
low2 = t2.read() + add_to_low
low3 = t3.read() + add_to_low
low4 = t4.read() + add_to_low
low5 = t5.read() + add_to_low
low6 = t6.read() + add_to_low
low7 = t7.read() + add_to_low
low8 = t8.read() + add_to_low
low9 = t9.read() + add_to_low
low10 = t10.read() + add_to_low

pins = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]
lows = [low0, low1, low2, low3, low4, low5, low6, low7, low8, low9, low10]

NUM_TOUCH_PINS = 11

NOTES = [262,277,294,311,330,349,370,392,415,440,466,493]
for i in range(0,len(NOTES)):
    NOTES.append(NOTES[i] * 2)
    
NOTES = NOTES[0:22]

RANGE = "HIGH" #LOW for one ESP32, HIGH for the other

if RANGE == "LOW":
    NOTES = NOTES[0:11]
else:
    NOTES = NOTES[11:22]

print(NOTES)

audio = I2S(0, # This must be either 0 or 1 for ESP32
            sck=sck_pin, ws=ws_pin, sd=sd_pin,
            mode=I2S.TX,
            bits=8*BYTES_PER_SAMPLE,
            format=I2S.MONO,
            rate=8000,
            ibuf=10000)

tone_feq0 = NOTES[0]
tone_feq1 = NOTES[1]
tone_feq2 = NOTES[2]
tone_feq3 = NOTES[3]
tone_feq4 = NOTES[4]
tone_feq5 = NOTES[5]
tone_feq6 = NOTES[6]
tone_feq7 = NOTES[7]
tone_feq8 = NOTES[8]
tone_feq9 = NOTES[9]
tone_feq10 = NOTES[10]
AMPLITUDE = 3000

n_samples0 = SAMPLE_RATE // tone_feq0
buffer_size0 = n_samples0 * BYTES_PER_SAMPLE
n_samples1 = SAMPLE_RATE // tone_feq1
buffer_size1 = n_samples1 * BYTES_PER_SAMPLE
n_samples2 = SAMPLE_RATE // tone_feq2
buffer_size2 = n_samples2 * BYTES_PER_SAMPLE
n_samples3 = SAMPLE_RATE // tone_feq3
buffer_size3 = n_samples3 * BYTES_PER_SAMPLE
n_samples4 = SAMPLE_RATE // tone_feq4
buffer_size4 = n_samples4 * BYTES_PER_SAMPLE
n_samples5 = SAMPLE_RATE // tone_feq5
buffer_size5 = n_samples5 * BYTES_PER_SAMPLE
n_samples6 = SAMPLE_RATE // tone_feq6
buffer_size6 = n_samples6 * BYTES_PER_SAMPLE
n_samples7 = SAMPLE_RATE // tone_feq7
buffer_size7 = n_samples7 * BYTES_PER_SAMPLE
n_samples8 = SAMPLE_RATE // tone_feq8
buffer_size8 = n_samples8 * BYTES_PER_SAMPLE
n_samples9 = SAMPLE_RATE // tone_feq9
buffer_size9 = n_samples9 * BYTES_PER_SAMPLE
n_samples10 = SAMPLE_RATE // tone_feq10
buffer_size10 = n_samples10 * BYTES_PER_SAMPLE

buf0 = bytearray(buffer_size0)
buf1 = bytearray(buffer_size1)
buf2 = bytearray(buffer_size2)
buf3 = bytearray(buffer_size3)
buf4 = bytearray(buffer_size4)
buf5 = bytearray(buffer_size5)
buf6 = bytearray(buffer_size6)
buf7 = bytearray(buffer_size7)
buf8 = bytearray(buffer_size8)
buf9 = bytearray(buffer_size9)
buf10 = bytearray(buffer_size10)

buf = [buf0, buf1, buf2, buf3, buf4, buf5, buf6, buf7, buf8, buf9, buf10]

for i in range(NUM_TOUCH_PINS):
    n_samples = SAMPLE_RATE // NOTES[i]
    buffer_size = n_samples * BYTES_PER_SAMPLE
    buf[i] = bytearray(buffer_size)
    for j in range(n_samples):
        sample = int(AMPLITUDE * math.sin(2 * math.pi * j / n_samples))
        struct.pack_into("<h", buf[i], j * BYTES_PER_SAMPLE, sample)

while True:
    for i in range (0, NUM_TOUCH_PINS):
        if (pins[i].read()) > (lows[i]):
            #tone_feq = NOTES[i]
            print(i, " pressed")
            audio.write(buf[i])
        #print(i, ": ", (pins[i]).read())
audio.deinit()
