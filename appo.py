import math
from datetime import datetime

import moviepy.editor as mp
from PIL import Image, ImageDraw, ImageFont

# geometry
PI = math.pi
COS30 = math.sqrt(3) / 2
WIGGLE_MAGNITUDE = 0.03
WIGGLE_PERIOD_Y = 2
WIGGLE_PERIOD_X1 = 3
WIGGLE_PERIOD_X2 = 5

# canvas
CANVAS_WIDTH = 1000

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# iteration/timing
NUM_LEVELS = 8
DDELTA = 0.1

class AppoFactory:
    def __init__(self):
        self.dy = 0
        self.dx1 = 0
        self.dx2 = 0

    def set_deltas(self, delta):
        self.dy = WIGGLE_MAGNITUDE * math.sin(2 * PI * delta / WIGGLE_PERIOD_Y)
        self.dx1 = WIGGLE_MAGNITUDE * math.sin(2 * PI * delta / WIGGLE_PERIOD_X1)
        self.dx2 = WIGGLE_MAGNITUDE * math.sin(2 * PI * delta / WIGGLE_PERIOD_X2)

    def appo(self, image_draw, level, R, x, y):
        #print(f"enter appo: level={level} R={R}, x={x} y={y}")

        if level <= 0:
            return

        image_draw.ellipse(
            (x-R, y-R, x+R, y+R),  # bounding box of circle,
            fill=None, outline=WHITE
        )
        
        d = R / (1 + COS30)
        r = R - d
        rcenter = d - r
        level -= 1

        self.appo(
            image_draw, level, r,
            x, 
            y + (1 + self.dy) * d
        )
        self.appo(
            image_draw, level, r, 
            x + (1 + self.dx1) * (d * COS30), 
            y - (1 + self.dx1) * d/2
        )
        self.appo(
            image_draw, level, r,
            x - (1 + self.dx2) * d * COS30, 
            y - (1 + self.dx2) * d/2
        )
        self.appo(image_draw, level-1, rcenter, x, y)

def main():
    print("START")

    images = []

    af = AppoFactory()

    delta = 0
    while delta < 30:
        print(f"{datetime.now()} delta={delta}")
        im = Image.new('RGB', (CANVAS_WIDTH, CANVAS_WIDTH), BLACK)
        d = ImageDraw.Draw(im)

        af.set_deltas(delta)
        af.appo(d, NUM_LEVELS, 0.9 * CANVAS_WIDTH/2, CANVAS_WIDTH/2, CANVAS_WIDTH/2)

        images.append(im)

        delta += DDELTA

    file_base = f"appo_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    gif = f"{file_base}.gif"
    print(f"writing to ./{gif}")
    images[0].save(gif, save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)

    mp4 = f"{file_base}.mp4"
    print(f"converting to mp4: ./{mp4}")
    video = mp.VideoFileClip(gif)
    video.write_videofile(mp4)

if __name__ == "__main__":
    main()

