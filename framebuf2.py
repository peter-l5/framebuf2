# this code is distributed under the MIT licence.
# frambuf2 v006
# (c) 2022 Peter Lumb (peter-l5) 



import framebuf, gc
#from micropython import const

MONO_HMSB=framebuf.MONO_HMSB
MONO_VLSB=framebuf.MONO_VLSB


print('framebuf2 module dir: ' , dir() )

print('framebuf module dir: ' , dir(framebuf) )


class FrameBuffer(framebuf.FrameBuffer):
    print('FrameBuffer override class define: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
    print('FrameBuffer override class dir: ' , dir() )
#     for name in super().__dict__:
#         print('FB2 ',name)
#     cls.FrameBuffer = framebuf.FrameBuffer
#     print(MONO_HMSB)
    def large_text(self, s, x, y, m, c=1):
        
        smallbuffer=bytearray(8)
        letter=framebuf.FrameBuffer(smallbuffer,8,8,framebuf.MONO_HMSB)
        for element in s:
            letter.fill(0)
            letter.text(element,0,0,c)
            for i in range (0, 8):
                for j in range (0, 8):
                    if letter.pixel(i, j) == 1:
                        for k in range (x+i*m, x+(i+1)*m):
                            for l in range (y+j*m, y+(j+1)*m):
                                #print(element, i, j, k, l)
                                self.pixel(k, l, c)
            x=x+8*m
            
        pass # do later
    
    print('FrameBuffer override class created: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
    print('FrameBuffer override class dir: ' , dir() )

    pass # do later
