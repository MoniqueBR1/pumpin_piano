from machine import TouchPad, Pin
from machine import Pin, I2S
import math
import struct

SAMPLE_RATE = 12000
BYTES_PER_SAMPLE = 2
AMPLITUDE = 3000
NUM_TOUCH_PINS = 11
RANGE = "HIGH" #LOW for one ESP32, HIGH for the other

NOTES = [262,277,294,311,330,349,370,392,415,440,466,494]
for i in range(0, len(NOTES)):
    NOTES.append(NOTES[i] * 2)

if RANGE == "LOW":
    NOTES = NOTES[0:NUM_TOUCH_PINS]
else:
    NOTES = NOTES[NUM_TOUCH_PINS:NUM_TOUCH_PINS * 2]

sck_pin = Pin(15) # Serial clock (BCLK on breakout)
ws_pin = Pin(16) # Word select (LRCLK on breakout)
sd_pin = Pin(17) # Serial data (DIN on breakout)

audio = I2S(0, # This must be either 0 or 1 for ESP32
            sck=sck_pin, ws=ws_pin, sd=sd_pin,
            mode=I2S.TX,
            bits=8*BYTES_PER_SAMPLE,
            format=I2S.MONO,
            rate=SAMPLE_RATE,
            ibuf=10000)

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

pins = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]

add_to_low = 5000
lows = [] # low values of the touch pins
for i in range(0, NUM_TOUCH_PINS):
    lows.append(pins[i].read() + add_to_low)

arrs = []
for i in range(NUM_TOUCH_PINS):
    arrs.append([])
    n_samples = SAMPLE_RATE // NOTES[i]
    for j in range(n_samples):
        sample = int(AMPLITUDE * math.sin(2 * math.pi * j / n_samples))
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

# returns a buf based on the keys that are being pressed
def make_buf(keys_pressed):
    if len(keys_pressed) == 0:
        buf = bytearray(1 * BYTES_PER_SAMPLE)
        struct.pack_into("<h", buf, 0, 0)
        return buf
    
    component_arrs = [] # the arrays of the individual notes
    for i in keys_pressed:
        component_arrs.append(arrs[i]) # populates component_arrs
        
    lens = [len(a) for a in component_arrs] # list of length of each component_arr
    new_len = lcm(lens) # length of resultant array is least common multiple of lengths of component arrays (for smooth sound)
    len_cutoff = 10000 # maximum number of samples (to prevent lag)
    if new_len > len_cutoff:
        new_len = len_cutoff
    buffer_size = int(new_len * BYTES_PER_SAMPLE)
    buf = bytearray(buffer_size)

    for i in range(0, new_len):
        sample = 0
        for j in range(0,len(component_arrs)):
            sample += component_arrs[j][i % len(component_arrs[j])] # add the waves
        sample = sample // len(keys_pressed)
        struct.pack_into("<h", buf, i * BYTES_PER_SAMPLE, sample)
    return buf

buf = make_buf([])
keys_pressed = []
prev_keys_pressed = []

while True:
    keys_pressed = []
    for i in range (0, NUM_TOUCH_PINS):
        if pins[i].read() > lows[i]:
            keys_pressed.append(i)
    if keys_pressed != prev_keys_pressed:
        buf = make_buf(keys_pressed)
    audio.write(buf)
    prev_keys_pressed = keys_pressed

audio.deinit()
