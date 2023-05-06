# this code is distributed under the MIT licence.

"""
frambuf2 v209: micropython framebuffer extensions
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

__version__ = "v209"
__repo__ = "https://github.com/peter-l5/framebuf2"

import framebuf

# constants available in MicroPython 1.19.1
MONO_VLSB = framebuf.MONO_VLSB
MONO_HLSB = framebuf.MONO_HLSB
MONO_HMSB = framebuf.MONO_HMSB
RGB565 = framebuf.RGB565
GS2_HMSB = framebuf.GS2_HMSB
GS4_HMSB = framebuf.GS4_HMSB
GS8 = framebuf.GS8


class FrameBuffer(framebuf.FrameBuffer):
    def _reverse(self, s: string) -> string:
        t = ""
        for i in range(0, len(s)):
            t += s[len(s) - 1 - i]
        return t

    def large_text(self, s, x, y, m, c: int = 1, r: int = 0, t=None):
        """
        large text drawing function uses the standard framebuffer font (8x8 pixel characters)
        writes text, s,
        to co-cordinates x, y
        size multiple, m (integer, eg: 1,2,3,4. a value of 2 produces 16x16 pixel characters)
        colour, c [optional parameter, default value c=1]
        optional parameter, r is rotation of the text: 0, 90, 180, or 270 degrees
        optional parameter, t is rotation of each character within the text: 0, 90, 180, or 270 degrees
        """
        colour = c
        smallbuffer = bytearray(8)
        letter = framebuf.FrameBuffer(smallbuffer, 8, 8, framebuf.MONO_HMSB)
        r = r % 360 // 90
        dx = 8 * m if r in (0, 2) else 0
        dy = 8 * m if r in (1, 3) else 0
        if r in (2, 3):
            s = self._reverse(s)
        t = r if t is None else t % 360 // 90
        a, b, c, d = 1, 0, 0, 1
        for i in range(0, t):
            a, b, c, d = c, d, -a, -b
        x0 = 0 if a + c > 0 else 7
        y0 = 0 if b + d > 0 else 7
        for character in s:
            letter.fill(0)
            letter.text(character, 0, 0, 1)
            for i in range(0, 8):
                for j in range(0, 8):
                    if letter.pixel(i, j) == 1:
                        p = x0 + a * i + c * j
                        q = y0 + b * i + d * j
                        if m == 1:
                            self.pixel(x + p, y + q, colour)
                        else:
                            self.fill_rect(x + p * m, y + q * m, m, m, colour)
            x += dx
            y += dy

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
            self.vline(x0, y0 - radius, 2 * radius + 1, c)
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
                self.vline(x0 + x, y0 - y, 2 * y + 1, c)
                self.vline(x0 + y, y0 - x, 2 * x + 1, c)
                self.vline(x0 - x, y0 - y, 2 * y + 1, c)
                self.vline(x0 - y, y0 - x, 2 * x + 1, c)

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
                self.hline(a, y0, b - a + 1, c)
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
            y = y0
            if y0 == y1:
                last = y1 - 1
            else:
                last = y1
            while y <= last:
                a = x0 + sa // dy01
                b = x0 + sb // dy02
                sa += dx01
                sb += dx02
                if a > b:
                    a, b = b, a
                self.hline(a, y, b - a + 1, c)
                y += 1
            sa = dx12 * (y - y1)
            sb = dx02 * (y - y0)
            while y <= y2:
                a = x1 + sa // dy12
                b = x0 + sb // dy02
                sa += dx12
                sb += dx02
                if a > b:
                    a, b = b, a
                self.hline(a, y, b - a + 1, c)
                y += 1
