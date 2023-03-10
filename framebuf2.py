# this code is distributed under the MIT licence.

"""
frambuf2 v202: micropython framebuffer extensions
(c) 2022-2023 Peter Lumb (peter-l5)

acknowledgement
the methods: circle() and triangle() are based on the
adafruit micropython gfx library:
See repository: https://github.com/adafruit/micropython-adafruit-gfx
that library was: 
Port of Adafruit GFX Arduino library to MicroPython
Based on: https://github.com/adafruit/Adafruit-GFX-Library
Author: Tony DiCola (original GFX author Phil Burgess)
License: MIT License (https://opensource.org/licenses/MIT)
"""

__version__ = "v202"
__repo__ = "https://github.com/peter-l5/framebuf2"

import framebuf

# constants available in MicroPython 1.19.1
MONO_VLSB=framebuf.MONO_VLSB
MONO_HLSB=framebuf.MONO_HLSB
MONO_HMSB=framebuf.MONO_HMSB
RGB565=framebuf.RGB565
GS2_HMSB=framebuf.GS2_HMSB
GS4_HMSB=framebuf.GS4_HMSB
GS8=framebuf.GS8

class FrameBuffer(framebuf.FrameBuffer):
    
    def large_text(self, s, x, y, m, c=1):
        """
        large text drawing function uses the standard framebuffer font (8x8 pixel characters)
        writes text, s,
        to co-cordinates x, y
        size multiple, m (integer, eg: 1,2,3,4. a value of 2 produces 16x16 pixel characters)
        colour, c [optional parameter, default value c=1]
        """
        smallbuffer=bytearray(8)
        letter=framebuf.FrameBuffer(smallbuffer,8,8,framebuf.MONO_HMSB)
        for character in s:
            letter.fill(0)
            letter.text(character,0,0,1)
            for i in range (0, 8):
                for j in range (0, 8):
                    if letter.pixel(i, j) == 1:
                        for k in range (x+i*m, x+(i+1)*m):
                            for l in range (y+j*m, y+(j+1)*m):
                                self.pixel(k, l, c)
            x=x+8*m

    def circle(self, x0, y0, radius, c, f: bool = None):
        """
        Circle drawing function.  Will draw a single pixel wide circle with
        center at x0, y0 and the specified radius
        colour c
        fill if f is True 
        """
        if f is None or f != True:
            g = 1 - radius
            ddG_x = 1
            ddG_y = -2 * radius
            x = 0
            y = radius
            self.pixel(x0, y0 + radius, c)
            self.pixel(x0, y0 - radius, c)
            self.pixel(x0 + radius, y0, c)
            self.pixel(x0 - radius, y0, c)
            while x < y:
                if g >= 0:
                    y -= 1
                    ddG_y += 2
                    g += ddG_y
                x += 1
                ddG_x += 2
                g += ddG_x
                self.pixel(x0 + x, y0 + y, c)
                self.pixel(x0 - x, y0 + y, c)
                self.pixel(x0 + x, y0 - y, c)
                self.pixel(x0 - x, y0 - y, c)
                self.pixel(x0 + y, y0 + x, c)
                self.pixel(x0 - y, y0 + x, c)
                self.pixel(x0 + y, y0 - x, c)
                self.pixel(x0 - y, y0 - x, c)
        else:
            self.vline(x0, y0 - radius, 2*radius + 1, c)
            g = 1 - radius
            ddG_x = 1
            ddG_y = -2 * radius
            x = 0
            y = radius
            while x < y:
                if g >= 0:
                    y -= 1
                    ddG_y += 2
                    g += ddG_y
                x += 1
                ddG_x += 2
                g += ddG_x
                self.vline(x0 + x, y0 - y, 2*y + 1, c)
                self.vline(x0 + y, y0 - x, 2*x + 1, c)
                self.vline(x0 - x, y0 - y, 2*y + 1, c)
                self.vline(x0 - y, y0 - x, 2*x + 1, c)

    def triangle(self, x0, y0, x1, y1, x2, y2, c, f: bool = None):
        """
        Triangle drawing function.  Will draw a single pixel wide triangle
        around the points (x0, y0), (x1, y1), and (x2, y2)
        colour c
        fill if f is True 
        """
        if f is None or f != True:
            self.line(x0, y0, x1, y1, c)
            self.line(x1, y1, x2, y2, c)
            self.line(x2, y2, x0, y0, c)
        else: 
            if y0 > y1:
                y0, y1 = y1, y0
                x0, x1 = x1, x0
            if y1 > y2:
                y2, y1 = y1, y2
                x2, x1 = x1, x2
            if y0 > y1:
                y0, y1 = y1, y0
                x0, x1 = x1, x0
            a = 0
            b = 0
            y = 0
            last = 0
            if y0 == y2:
                a = x0
                b = x0
                if x1 < a:
                    a = x1
                elif x1 > b:
                    b = x1
                if x2 < a:
                    a = x2
                elif x2 > b:
                    b = x2
                self.hline(a, y0, b-a+1, c)
                return
            dx01 = x1 - x0
            dy01 = y1 - y0
            dx02 = x2 - x0
            dy02 = y2 - y0
            dx12 = x2 - x1
            dy12 = y2 - y1
            if dy01 == 0:
                dy01 = 1
            if dy02 == 0:
                dy02 = 1
            if dy12 == 0:
                dy12 = 1
            sa = 0
            sb = 0
            if y1 == y2:
                last = y1
            else:
                last = y1-1
            for y in range(y0, last+1):
                a = x0 + sa // dy01
                b = x0 + sb // dy02
                sa += dx01
                sb += dx02
                if a > b:
                    a, b = b, a
                self.hline(a, y, b-a+1, c)
            sa = dx12 * (y - y1)
            sb = dx02 * (y - y0)
            while y <= y2:
                a = x1 + sa // dy12
                b = x0 + sb // dy02
                sa += dx12
                sb += dx02
                if a > b:
                    a, b = b, a
                self.hline(a, y, b-a+1, c)
                y += 1
