# this code is distributed under the MIT licence.
# frambuf2 v008
# (c) 2022 Peter Lumb (peter-l5) 

import framebuf

# constants available in MicroPython 1.19.1
MONO_HMSB=framebuf.MONO_HMSB
MONO_VLSB=framebuf.MONO_VLSB
MONO_HMSB=framebuf.MONO_HMSB
RGB565=framebuf.RGB565
GS2_HMSB=framebuf.GS2_HMSB
GS4_HMSB=framebuf.GS4_HMSB
GS8=framebuf.GS8


class FrameBuffer(framebuf.FrameBuffer):

    def large_text(self, s, x, y, m, c=1):
        
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
