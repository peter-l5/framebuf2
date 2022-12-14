# framebuf2

## MicroPython FrameBuffer larger font extension

This module extends MicroPython's [framebuf module](https://docs.micropython.org/en/latest/library/framebuf.html "MicroPython documentation"). It provides double, triple and quadruple size rendering of text using the built-in font provided in the framebuf module. 
The module has been tested on a Raspberry Pi Pico with a SH1107 display.

## Methods

The module adds the large_text() method, `FrameBuffer.large_text(s, x, y, m [, c])` to the FrameBuffer class.

Write text, s, to a FrameBuffer using the the x and y coordinates as the upper-left corner of the text. The colour of the text can be defined by the optional argument, c, but is otherwise a default value of 1. The parameter m sets the size multiple for the text. The normal size for text with the 'FrameBuffer.text()' method is 8x8. This would be a multiple of 1. To obtain larger text output, with 16x16 pixel characters, for example, use 2 for the m parameter.

Example use:
```
    # display is a framebuffer object
    display.large_text('double', 0, 0, 2, 1)  # double size text
    display.large_text('size!', 0, 16, 2, 1)
    display.large_text('HUGE', 0, 32, 4, 1)   # quadruple size text
```

## Loading the module

Use the following to import the module and extend the FrameBuffer class.  
`import framebuf2 as framebuf`

## Requirements

Works with MicroPython version 1.18. Will also work with other versions. 
