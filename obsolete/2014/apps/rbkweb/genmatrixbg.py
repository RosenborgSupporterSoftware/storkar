#!/usr/bin/python

# vim:sw=4

from math import cos
import colorsys
import Image


def clamp_value(val):
    if val < 0.0: return 0.0
    if val > 1.0: return 1.0
    return val


def color_adjust(touple, factors):
    r, g, b, a = touple
    hf, sf, vf = factors
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    h = clamp_value(h * hf)
    s = clamp_value(s * sf)
    v = clamp_value(v * vf)
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    a = 255
    return (int(r*255), int(g*255), int(b*255), a)


def clamp_byte(val):
    if val < 0: return 0
    if val > 255: return 255
    return val


def run():
    W = 150
    H = 150
    data = ""

    fadesteps = 30
    fadestart = 10

    for y in range(0, H):
        for x in range(0, W):
            r, g, b = 0, 0, 0
            # use sine curve to smooth the gradient, and don't keep the
            # mid section totally flat yellow
            if x > (y + fadestart):
                idx = x - y - fadestart
                g = 240
                if idx <= fadesteps:
                    f = (cos(3.1415926 * float(fadesteps - idx) / float(fadesteps)) + 1.0) / 2.0
                    r = int(240.0 - 240.0 * f)
                else:
                    r = 0
            elif x < (y - fadestart):
                idx = y - x - fadestart
                r = 240
                if idx <= fadesteps:
                    f = (cos(3.1415926 * float(fadesteps - idx) / float(fadesteps)) + 1.0) / 2.0
                    g = int(240.0 - 240.0 * f)
                else:
                    g = 0
            else:
                r = 240
                g = 240
            data += '%c%c%c%c' % (r, g, b, 255)

    assert len(data) == (W*H*4), "invalid buffer length"

    im = Image.frombuffer("RGBA", (W, H), data, 'raw', "RGBA", 0, 1)
    im.save("grad.png", "PNG")

    w = 30
    h = 30
    for py, px in ((0,2),(0,1),(0,0),(1,0),(2,0)):
        img = im.crop((px*w, py*h, (px+1)*w, (py+1)*h))
        pix = img.load()
        d = 80
        adjustment = (1.0, 0.6, 1.3)
        for x in range(0, w):
            pix[x,0] = color_adjust(pix[x,0], adjustment)
        for x in range(1, w):
            pix[x,1] = color_adjust(pix[x,1], adjustment)
        adjustment = (1.0, 0.4, 1.3)
        for y in range(1, h):
            pix[0,y] = color_adjust(pix[0,y], adjustment)
        for y in range(2, h):
            pix[1,y] = color_adjust(pix[1,y], adjustment)
        img.save('b%d%d.png' % (px, py), 'png')

    img = im.crop((0, 0, w, h))
    pix = img.load()
    for y in range(0, 30):
        for x in range(0, 30):
            pix[x, y] = (220, 220, 220, 255)
    adjustment = (1.0, 0.6, 1.3)
    for x in range(0, w):
        pix[x,0] = color_adjust(pix[x,0], adjustment)
    for x in range(1, w):
        pix[x,1] = color_adjust(pix[x,1], adjustment)
    adjustment = (1.0, 0.4, 1.3)
    for y in range(1, h):
        pix[0,y] = color_adjust(pix[0,y], adjustment)
    for y in range(2, h):
        pix[1,y] = color_adjust(pix[1,y], adjustment)
    img.save('xxx.png', 'png')



if __name__ == "__main__":
    run()
