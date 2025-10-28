from machine import TouchPad, Pin
import time
from machine import Pin, I2S
import math
import struct
from time import sleep

SAMPLE_RATE = 12000 #8000
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

NOTES = [262,277,294,311,330,349,370,392,415,440,466,494]
for i in range(0,len(NOTES)):
    NOTES.append(NOTES[i] * 2)
    
NOTES = NOTES[0:22]

RANGE = "HIGH" #LOW for one ESP32, HIGH for the other

if RANGE == "LOW":
    NOTES = NOTES[0:11]
else:
    NOTES = NOTES[11:22]

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

n_samples = []
buffer_sizes = []
bufs = []
arrs = []

for i in range(NUM_TOUCH_PINS):
    tone_freq = NOTES[i]
    n = SAMPLE_RATE // tone_freq
    size = n * BYTES_PER_SAMPLE
    n_samples.append(n)
    buffer_sizes.append(size)
    bufs.append(bytearray(size))
    arr = []
    arrs.append(arr)

for i in range(NUM_TOUCH_PINS):
    n_samples = SAMPLE_RATE // NOTES[i]
    buffer_size = n_samples * BYTES_PER_SAMPLE
    bufs[i] = bytearray(buffer_size)
    for j in range(n_samples):
        sample = int(AMPLITUDE * math.sin(2 * math.pi * j / n_samples))
        struct.pack_into("<h", bufs[i], j * BYTES_PER_SAMPLE, sample)
        arrs[i].append(sample)

def make_buf(keys_pressed):
    indices = [] # the indices of the pressed keys
    component_arrs = [] # the bufs of the individual notes
    for i in range(0,len(keys_pressed)):
        if keys_pressed[i]:
            indices.append(i) # populates indices
    for i in indices:
        component_arrs.append(arrs[i]) # populates component_bufs
    lens = [] # list of n_samples of each component buf
    for b in component_arrs:
        lens.append(len(b))
    max_len = max(lens)
    buffer_size = int(max_len * 2 * BYTES_PER_SAMPLE)
    buf = bytearray(buffer_size)
    #print(buffer_size, len(component_arrs[0]))
    print(len(component_arrs))
    for i in range(0, max_len * 2):
        sample = 0
        for j in range(0,len(component_arrs)):
        #sample = arrs[0][i % len(arrs[0])] + arrs[1][i % len(arrs[1])]
#             if i >= len(arrs[j]):
              sample += component_arrs[j][i % len(component_arrs[j])]
        
        print(sample, component_arrs[0][i % len(component_arrs[0])], component_arrs[1][i % len(component_arrs[1])])
        sample = int(sample / len(indices))
        struct.pack_into("<h", buf, int(i * BYTES_PER_SAMPLE), sample)
        #for j in range(0, len(component_bufs)):
    #print(arrs[0])
    #print(component_bufs[0])
    #print(buf)
    return buf
#     print(component_bufs[0])
#     for i in range(0,len(component_bufs[0])):
#         print(component_bufs[0][i])
    

test_buf = make_buf([1,0,0,0,0,0,0,1])

play = False
keys_pressed = []

while True:
    play = False
    keys_pressed = []
    for i in range (0, NUM_TOUCH_PINS):
        if (pins[i].read()) > (lows[i]):
            play = True
            keys_pressed.append(i)
            #tone_feq = NOTES[i]
            print(i, " pressed")
    if play and 0 in keys_pressed:
        audio.write(bufs[0])
        #print(i, ": ", (pins[i]).read())
    if play and 1 in keys_pressed:
        audio.write(bufs[7])
    if play and 2 in keys_pressed:
        audio.write(test_buf)
audio.deinit()
