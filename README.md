# framebuf2

## MicroPython FrameBuffer larger font, triangle and circle extension

This module extends the `FrameBuffer` class in MicroPython's [framebuf module](https://docs.micropython.org/en/latest/library/framebuf.html "MicroPython documentation"). It enables drawing of double, triple, quadruple, and larger size text to FrameBuffer objects using the built-in font provided in the framebuf module.<br> 
Also included are methods to draw triangles and circles. These can be outlines only or filled.<br>
The module has been tested on a Raspberry Pi Pico with a 128x128 pixel SH1107 display. It should work with all MicroPython FrameBuffer objects.

## Methods

`large_text(s, x, y, m [, c=1] [, r=0 [, t=None]])` 

Write text, `s`, to a FrameBuffer using the the `x` and `y` coordinates as the upper-left corner of the text. The colour of the text can be defined by the optional argument, `c`, but is otherwise a default value of 1. The parameter `m` sets the size multiple for the text. The normal size for text with the 'FrameBuffer.text()' method is 8x8 pixels. This would be a multiple of 1. To obtain larger text output, with 16x16 pixel characters, for example, use 2 for the m parameter. The optional parameter r controls the rotation of the text, 0 degrees is the default, 90, 180 and 270 degrees are possible. In addition the t parameter enables individual characters within a string to be independently rotated to 0, 90, 180 or 270 degrees. 

`circle(x0, y0, radius, c [, f:bool] )` 

Draw a circle centred on `x0, y0` with the specified `radius` and border colour, `c` (integer). Optionally fill the circle by adding `f=True`.

`triangle(x0, y0, x1, y1, x2, y2, c [, f:bool] )` 

Draw a triangle with vertices at points `x0,y0` , `x1,y1` and `x2,y2` and border colour, `c` (integer). Optionally fill the circle by adding `f=True`.


## Usage

Example use:
```
    # display is a framebuffer object
    display.large_text('double', 0, 0, 2, 1)  # double size text
    display.large_text('size!', 0, 16, 2, 1)
    display.large_text('HUGE', 0, 32, 4, 1)   # quadruple size text

    # draw a circle centred at point (x=64, y=64) with radius 56 and colour 1.
    display.circle(64, 64, 56 , c=1)
    display.circle(64, 64, 48 , c=1, f=True) # filled circle

    # draw a filled triangle with corners at (x=0, y=0), (x=0, y=127) and (x=127, y=127)
    # filled with colour 1.
    display.triangle(0, 0, 0, 127, 127, 127, c=1, f=True)
```
Additional examples are included in the example code for this [SH1107](https://github.com/peter-l5/SH1107 "SH1107 OLED display driver") display driver

## Loading the module

Use the following to import the module and extend the FrameBuffer class.<br>
`import framebuf2 as framebuf`<br>
The FrameBuffer class will then offer these additional methods besides all the standard methods.

## Requirements

Works with MicroPython version 1.19.1. Will also work with other versions. 

## Release notes

#### v206

- large_text() enhanced by the addition of rotation parameter 
- substantial speed improvements

#### v202

- triangle() and circle() drawing methods added