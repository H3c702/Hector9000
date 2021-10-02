from Hector9000.utils.LEDStripAPI import LEDStripAPI
import time
import board
import neopixel
import random


class LEDStripConnector(LEDStripAPI):

    def __init__(self):
        self.PORT = board.D18
        self.NUM = 15
        self.NUMBASE = 5
        self.pixels = neopixel.NeoPixel(self.PORT, self.NUM)
        self.cols = [
            (255, 0, 0),
            (255, 63, 0),
            (255, 120, 0),
            (0, 255, 0),
            (0, 255, 255),
            (0, 0, 255),
            (255, 0, 255)
        ]
        self.col_neutral = (80, 80, 30)
        self.NUMCOLS = len(self.cols)
        self.mode = 1
        self.ORDER = neopixel.GRB
        self.num_pixels = self.NUM
        self.pixels.fill(self.col_neutral)
        self.drinkcolor = (0, 0, 0)

    def standart(self, color=(80, 80, 30), type=0):
        if type == 0:
            self.pixels.fill(color)
            self.mode = 0
        elif type == 1:
            self.mode = 1
        elif type == 2:
            self.mode = 2
        elif type == 3:
            self.mode = 3
        elif type == 4:
            self.mode = 4
        else:
            self.pixels.fill(color)
            self.mode = 0

    def standby(self, color=(80, 80, 30), type=0):
        if type == 0:
            self.pixels.fill(color)
        else:
            self.pixels.fill((0, 0, 0))

    def dosedrink(self, color=(0, 0, 255), type=0):
        self.mode = 99
        self.drinkcolor = color

    def drinkfinish(self, color=(255, 255, 255), type=0):
        self.finish(color, type)

    def finish(self, color=(255, 255, 255), type=0):
        for i in range(self.NUMBASE):
            self.pixels[i] = (0, 0, 0)
        self.pixels.show()
        for i in range(10):
            time.sleep(0.05)
            self.pixels[14 - i] = color
            self.pixels.show()
        for i in range(3):
            for j in range(self.NUMBASE):
                self.pixels[j] = color
            self.pixels.show()
            time.sleep(0.05)
            for j in range(self.NUMBASE):
                self.pixels[j] = (0, 0, 0)
            self.pixels.show()
            time.sleep(0.05)
        self.mode = 3

    def drinkloop(self):
        print("drinkloop")
        for i in range(self.NUMBASE):
            self.pixels[i] = self.drinkcolor
            self.pixels.show()
        for i in range(5):
            start = random.randrange(9, 14)
            print(start)
            for j in range(3):
                start = start - j
                for index in range(10):
                    index = index + 5
                    if index is start:
                        self.pixels[index] = self.drinkcolor
                    else:
                        self.pixels[index] = (0, 0, 0)
                if self.mode == 99:
                    self.pixels.show()
                    time.sleep(0.3)
                else:
                    return

    # mode 1: Farben einzeln durchgehen
    # mode 2: Strobo
    # mode 3:
    def led_loop(self):
        if self.mode == 1:
            self.mode1()
        elif self.mode == 2:
            self.mode2()
        elif self.mode == 3:
            self.mode3()
        elif self.mode == 4:
            self.mode4()
        elif self.mode == 99:
            # dosedrink
            self.drinkloop()

    def loop(self):
        self.led_loop()

    def mode1(self):
        for i in range(self.NUMCOLS):
            self.pixels.fill(self.cols[i])
            for j in range(4):
                if self.mode == 1:
                    time.sleep(1)
                else:
                    return

    def mode2(self):
        self.pixels.fill((0, 0, 0))
        time.sleep(.05)
        self.pixels.fill((255, 255, 255))
        time.sleep(.05)

    def mode3(self):
        for i in range(self.NUMBASE):
            self.pixels[i] = (0, 0, 255)
        for c in range(self.NUMCOLS):
            for i in range(self.NUM - self.NUMBASE):
                self.pixels[self.NUMBASE + i] = self.cols[c]
                time.sleep(.1)
            for i in range(self.NUMBASE):
                self.pixels[i] = (0, 0, 255)

    def wheel(self, pos):
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
        return (
            r,
            g,
            b) if self.ORDER == neopixel.RGB or self.ORDER == neopixel.GRB else (
            r,
            g,
            b,
            0)

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.NUM - self.NUMBASE):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[self.NUMBASE + i] = self.wheel(pixel_index & 255)
            for j in range(self.NUMBASE):
                self.pixels[j] = self.pixels[self.NUMBASE]
            self.pixels.show()
            time.sleep(wait)

    def mode4(self):
        for i in range(4):
            self.rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step


if __name__ == "__main__":
    test = LEDStripConnector()
    test.finish()
    test.dosedrink()
    time.sleep(10)
    test.standart()
