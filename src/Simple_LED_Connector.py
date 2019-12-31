from LEDStripAPI import LEDStripAPI
import time, board, neopixel


class Simple_LED_Connector(LEDStripAPI):

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
        self.drinkcolor = (0,0,0)

    def standart(self, color=(80,80,30), type=0):
        return

    def standby(self, color=(80,80,30), type=0):
        return

    def dosedrink(self, color=(0,0,255), type=0):
        return

    def drinkfinish(self, color=(255,255,255), type=0):
        self.mode = 2
        self.finish(color, type)
        self.mode = 1

    def finish(self, color=(255,255,255), type=0):
        self.pixels.fill((0,0,0))
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
                self.pixels[j] = (0,0,0)
            self.pixels.show()
            time.sleep(0.05)

    # mode 1: Farben Rad
    # mode 2: Drinkfinish

    def loop(self):
        self.mode3()

    def mode3(self):
        if not self.mode == 1:
            return
        for i in range(self.NUMBASE):
            self.pixels[i] = (0, 0, 255)
        for c in range(self.NUMCOLS):
            for i in range(self.NUM - self.NUMBASE):
                self.pixels[self.NUMBASE + i] = self.cols[c]
                if self.mode == 1:
                    time.sleep(.1)
                else:
                    return
