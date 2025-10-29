from machine import TouchPad, Pin
import time
from machine import Pin, I2S
import math
import struct

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
            rate=SAMPLE_RATE,#8000,
            ibuf=10000)

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
        
# returns the least common multiple of a list of integers
def lcm(nums):
    if len(nums) == 0:
        return 0
    if len(nums) == 1:
        return nums[0]
    if len(nums) == 2:
        a = nums[0]
        b = nums[1]
        while b:
            a, b = b, a % b
        return abs(nums[0] * nums[1]) // a
    return lcm([lcm(nums[:len(nums) - 1]), nums[len(nums)-1]])

def make_buf(keys_pressed):
    if len(keys_pressed) == 0:
        buf = bytearray(1 * BYTES_PER_SAMPLE)
        struct.pack_into("<h", buf, 0, 0)
        return buf
    
    component_arrs = [] # the arrays of the individual notes
    for i in keys_pressed:
        component_arrs.append(arrs[i]) # populates component_arrs
    lens = [] # list of length of each component_arr
    for b in component_arrs:
        lens.append(len(b))
    new_len = lcm(lens) #length of array is least common multiple of lengths of component arrays
    buffer_size = int(new_len * BYTES_PER_SAMPLE)
    buf = bytearray(buffer_size)
    for i in range(0, new_len):
        sample = 0
        for j in range(0,len(component_arrs)):
            sample += component_arrs[j][i % len(component_arrs[j])]
        sample = int(sample / len(keys_pressed))
        struct.pack_into("<h", buf, int(i * BYTES_PER_SAMPLE), sample)
    return buf
    

buf = make_buf([])

play = False
keys_pressed = []
prev_keys_pressed = []

while True:
    play = False
    keys_pressed = []
    for i in range (0, NUM_TOUCH_PINS):
        if (pins[i].read()) > (lows[i]):
            play = True
            keys_pressed.append(i)
    if keys_pressed != prev_keys_pressed:
        buf = make_buf(keys_pressed)
    audio.write(buf)
    prev_keys_pressed = keys_pressed

audio.deinit()
