import time, board, neopixel

PORT = board.D18
NUM = 15
NUMBASE = 5

pixels = neopixel.NeoPixel(PORT, NUM)

cols = [
    (255, 0, 0),
    (255, 63, 0),
    (255, 120, 0),
    (0, 255, 0),
    (0, 255, 255),
    (0, 0, 255),
    (255, 0, 255)
]
col_neutral = (80, 80, 30)

NUMCOLS = len(cols)


def mode1():
    while True:
        for i in range(NUMCOLS):
            pixels.fill(cols[i])
            time.sleep(4)


def mode2():
    while True:
        pixels.fill((0, 0, 0))
        time.sleep(.05)
        pixels.fill((255, 255, 255))
        time.sleep(.05)


def modeClean():
    while True:
        pixels.fill((255, 255, 255))
        time.sleep(.5)
        pixels.fill((255, 255, 0))
        time.sleep(.5)


def mode3():
    for i in range(NUMBASE):
        pixels[i] = (0, 0, 255)
    while True:
        for c in range(NUMCOLS):
            for i in range(NUM - NUMBASE):
                pixels[NUMBASE + i] = cols[c]
                # pixels[(NUMBASE+i-1) % NUM] = (0,0,0)
                time.sleep(.1)
            for i in range(NUMBASE):
                pixels[i] = (0, 0, 255)


# The number of NeoPixels
num_pixels = NUM

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB


# pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM - NUMBASE):
            pixel_index = (i * 256 // num_pixels) + j
            # pixels[NUMBASE+i] = wheel((int(-pixel_index * 20 / 256) + 55) & 255)
            pixels[NUMBASE + i] = wheel(int(pixel_index) & 255)
        for j in range(NUMBASE):
            pixels[j] = pixels[NUMBASE]
        pixels.show()
        time.sleep(wait)


def mode4():
    while True:
        if False:
            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((255, 0, 0))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((255, 0, 0, 0))
            pixels.show()
            time.sleep(1)

            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((0, 255, 0))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((0, 255, 0, 0))
            pixels.show()
            time.sleep(1)

            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((0, 0, 255))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((0, 0, 255, 0))
            pixels.show()
            time.sleep(1)

        rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step


modeClean()
