__version__ = '0.1.6'

import spidev
import time
import random


from digit_7x5 import digit_7x5

LED_TYPE = ("APA102", "SK9822")

class Led:
    def __init__(self, red=0, green=0, blue=0, brightness=32, led_type=LED_TYPE[1]):
        if led_type not in LED_TYPE:
            raise TypeError("unknown LED type, use APA102 or SK9822")
        self.led_type=led_type
        self.set2color(red, green, blue, brightness)
        
    def set2brightness(self, brightness=32):
        self.set2color(self.red, self.green, self.blue, brightness)

    def set2off(self):
        self.set2color(0, 0, 0)
        
    def set2white(self):
        self.set2color(84, 84, 84)
        
    def set2fullwhite(self):
        self.set2color(255, 255, 255)
        
    def set2red(self):
        self.set2color(red=255)
        
    def set2green(self):
        self.set2color(green=255)
        
    def set2blue(self):
        self.set2color(blue=255)
        
    def set2yellow(self):
        self.set2color(red=128, green=128)
        
    def set2cyan(self):
        self.set2color(blue=128, green=128)
        
    def set2magenta(self):
        self.set2color(blue=128, red=128)
        
    def set2color(self, red=0, green=0, blue=0, brightness=None):
        """ 
        allowed numeric input values are 0..255         
        """ 
        if type(red) is not int or red < 0 or red > 255:
            raise TypeError("red value must be 0..255")
        self.red = red
        if type(green) is not int or green < 0 or green > 255:
            raise TypeError("green value must be 0..255")
        self.green = green
        if type(blue) is not int or blue < 0 or blue > 255:
            raise TypeError("blue value must be 0..255")
        self.blue = blue
        if brightness is not None:
            if type(brightness) is not int or brightness < 0 or brightness > 255:
                raise TypeError("brightness value must be 0..255")
            self.brightness = brightness

        if self.led_type == LED_TYPE[0]:
            """ 
            don't use hardware brightness value on APA102
            set brightness to 11111 to avoid side effects         
            """ 
            p_brightness = 31 | 0xE0
            p_red = ( red * self.brightness // 255 ) & 0xFF
            p_green = ( green * self.brightness // 255 ) & 0xFF
            p_blue = ( blue * self.brightness // 255 ) & 0xFF
        elif self.led_type == LED_TYPE[1]:
            """ 
            hardware brightness value on SK9822 is 0..31
            """ 
            p_brightness = ( self.brightness // 8 ) | 0xE0
            p_red = red & 0xFF
            p_green = green & 0xFF
            p_blue = blue & 0xFF

        self.databytes = [ p_brightness, p_blue, p_green, p_red ]

    
class LedStrip:
    def __init__( self, pixels=5, led_type=LED_TYPE[1] ):
        if led_type not in LED_TYPE:
            raise TypeError("unknown LED type, use APA102 or SK9822")
        self.led_type = led_type
        if not ( type(pixels) is int and 2 <= pixels <= 300 ):
            raise TypeError("pixels value must be 2..300")
        self.pixels = pixels
        self.pixel = [ Led( led_type=led_type ) for x in range ( pixels ) ]
        
    def setall2brightness(self, brightness=32):
        [ self.pixel[x].set2brightness( brightness ) for x in range ( self.pixels ) ]
        
    def set2brightness(self, pixel=None, brightness=32):
        if not ( type(pixel) is int and 1 <= pixel <= self.pixels ):
            raise TypeError("invalid pixel value")
        self.pixel[pixel-1].set2brightness( brightness ) 
        
    def setall2off(self):
        [ self.pixel[x].set2off( ) for x in range ( self.pixels ) ]
        
    def set2off(self, pixel=None):
        if not ( type(pixel) is int and 1 <= pixel <= self.pixels ):
            raise TypeError("invalid pixel value")
        self.pixel[pixel-1].set2off( )

    def set2red(self, pixel=None):
        if not ( type(pixel) is int and 1 <= pixel <= self.pixels ):
            raise TypeError("invalid pixel value")
        self.pixel[pixel-1].set2red( )

    def set2green(self, pixel=None):
        if not ( type(pixel) is int and 1 <= pixel <= self.pixels ):
            raise TypeError("invalid pixel value")
        self.pixel[pixel-1].set2green( )

    def set2blue(self, pixel=None):
        if not ( type(pixel) is int and 1 <= pixel <= self.pixels ):
            raise TypeError("invalid pixel value")
        self.pixel[pixel-1].set2blue( )

    def set2yellow(self, pixel=None):
        if not ( type(pixel) is int and 1 <= pixel <= self.pixels ):
            raise TypeError("invalid pixel value")
        self.pixel[pixel-1].set2yellow( )

    def set2magenta(self, pixel=None):
        if not ( type(pixel) is int and 1 <= pixel <= self.pixels ):
            raise TypeError("invalid pixel value")
        self.pixel[pixel-1].set2magenta( )

    def set2cyan(self, pixel=None):
        if not ( type(pixel) is int and 1 <= pixel <= self.pixels ):
            raise TypeError("invalid pixel value")
        self.pixel[pixel-1].set2cyan( )

    def set2white(self, pixel=None):
        if not ( type(pixel) is int and 1 <= pixel <= self.pixels ):
            raise TypeError("invalid pixel value")
        self.pixel[pixel-1].set2white( )

    def set2fullwhite(self, pixel=None):
        if not ( type(pixel) is int and 1 <= pixel <= self.pixels ):
            raise TypeError("invalid pixel value")
        self.pixel[pixel-1].set2fullwhite( )

    def set2color(self, pixel=None, red=0, green=0, blue=0, brightness=None):
        if not ( type(pixel) is int and 1 <= pixel <= self.pixels ):
            raise TypeError("invalid pixel value")
        self.pixel[pixel-1].set2color(red, green, blue, brightness)

        
    def test(self):
        for x in range ( self.pixels ):
            if x % 7 == 0:
                self.pixel[x].set2red()
            elif x % 7 == 1:
                self.pixel[x].set2yellow()
            elif x % 7 == 2:
                self.pixel[x].set2green()
            elif x % 7 == 3:
                self.pixel[x].set2cyan()
            elif x % 7 == 4:
                self.pixel[x].set2blue()
            elif x % 7 == 5:
                self.pixel[x].set2magenta()
            else:
                self.pixel[x].set2off()

    def test_random(self,colors=4):
        colors = ( colors - 1 ) % 7 + 1
        for x in range ( self.pixels ):
            y = random.randint(0, colors) 
            if y == 0:
                self.pixel[x].set2off()
            elif y == 1:
                self.pixel[x].set2red()
            elif y == 2:
                self.pixel[x].set2green()
            elif y == 3:
                self.pixel[x].set2blue()
            elif y == 4:
                self.pixel[x].set2yellow()
            elif y == 5:
                self.pixel[x].set2cyan()
            elif y == 6:
                self.pixel[x].set2magenta()
            else:
                self.pixel[x].set2white()

    def setall2random(self):
        for x in range ( self.pixels ):
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            self.pixel[x].set2color(red, green, blue)
              

    def rotate_left(self):
        self.pixel.append(self.pixel.pop(0))
             
    def rotate_right(self):
        self.pixel.insert(0,self.pixel.pop(self.pixels - 1))
             
    def flip(self):
        self.pixel.reverse()
                 
        
    def show(self):
        self.databytes = [ 0x00, 0x00, 0x00, 0x00 ] # start frames
        for x in self.pixel:  # data frames
            self.databytes = self.databytes + x.databytes
        if self.led_type == LED_TYPE[1]:  # refresh frames for SK9822
            self.databytes = self.databytes + [ 0x00, 0x00, 0x00, 0x00 ]
        for x in range ( ( ( self.pixels - 1 ) // 2 + 1 ) // 8 + 1 ):
            # additional clocks ticks - 1/2 per pixel
            self.databytes = self.databytes + [ 0x00 ]
        # write to LED using SPI
        spi = spidev.SpiDev()
        spi.open(0, 1)
        spi.max_speed_hz=8000000
        spi.xfer2( self.databytes )
        spi.close()

class LedMatrix:
    def __init__( self, rows=2, columns=2, led_type=LED_TYPE[1] ):
        if led_type not in LED_TYPE:
            raise TypeError("unknown LED type, use APA102 or SK9822")
        self.led_type = led_type
        if type( rows ) is not int or rows < 2 or rows > 16:
            raise TypeError("rows value must be 0..16")
        self.rows = rows
        if type( columns ) is not int or columns < 2 or columns > 64:
            raise TypeError("columns value must be 0..64")
        self.columns = columns
        self.row = [ LedStrip( columns, led_type ) for x in range ( rows ) ]
        
    def setall2brightness(self, brightness=32):
        [ self.row[x].pixel[y].set2brightness( brightness )
          for x in range ( self.rows ) for y in range ( self.columns )]
        
    def setall2off(self):
        [ self.row[x].pixel[y].set2off( )
          for x in range ( self.rows ) for y in range ( self.columns )]

    def test(self):
        for x in range ( self.rows):
            if x % 2 == 0:
                self.row[x].setall2brightness( 16 )
            if x % 2 == 1:
                self.row[x].setall2brightness( 128 )
            for y in range (self.columns ):
                if y % 4 == 0:
                    self.row[x].pixel[y].set2red()
                if y % 4 == 1:
                    self.row[x].pixel[y].set2green()
                if y % 4 == 2:
                    self.row[x].pixel[y].set2blue()
                if y % 4 == 3:
                    self.row[x].pixel[y].set2white()
                

    def rotate_left(self):
        [ self.row[x].pixel.append(self.row[x].pixel.pop(0))
          for x in range ( self.rows ) ]
             
    def rotate_right(self):
        [ self.row[x].pixel.insert(0,self.row[x].pixel.pop(self.columns - 1))
          for x in range ( self.rows ) ]
             
    def rotate_up(self):
        self.row.append(self.row.pop(0))
             
    def rotate_down(self):
        self.row.insert(0,self.row.pop(self.rows - 1))
             
    def flip_horizontal(self):
        [ self.row[x].pixel.reverse() for x in range ( self.rows ) ]
                 
    def flip_vertical(self):
        self.row.reverse()
        
    def show(self):
        self.databytes = [ 0x00, 0x00, 0x00, 0x00 ]  # start frames
        for x in range ( self.rows ):  # serpent 1,1-1,n, 2,n-2,1, 3.1-3,n, ...
            if x % 2 == 0:
                for y in self.row[x].pixel:
                    self.databytes = self.databytes + y.databytes
            else:
                for y in reversed(self.row[x].pixel):
                    self.databytes = self.databytes + y.databytes
        if self.led_type == LED_TYPE[1]:  # refresh bytes for SK9822
            self.databytes = self.databytes + [ 0x00, 0x00, 0x00, 0x00 ]
        for x in range ( ( ( self.rows * self.columns - 1 ) // 2 + 1 ) // 8 + 1 ):
            # additional clocks ticks - 1/2 per row
            self.databytes = self.databytes + [ 0x00 ]
        # write to LED using SPI
        spi = spidev.SpiDev()
        spi.open(0, 1)
        spi.max_speed_hz=8000000
        spi.xfer2( self.databytes )
        spi.close()

           
    def showtext(self):
        for x in range ( self.rows):
            text = ' '
            for y in range ( self.columns ):
                z = 0
                if self.row[x].pixel[y].red != 0:
                    z += 1
                if self.row[x].pixel[y].green != 0:
                    z += 2
                if self.row[x].pixel[y].blue != 0:
                    z += 4
                if z == 0:
                    text = text + ' '
                else:
                    text = text + str(z)
            print(text)
            
                         

    def set7x5char( self, char=' ', startrow=1, startcolumn=1, red=84, green=84, blue=84):
        if type( startrow ) is not int or startrow < 1 or startrow + 6 > self.rows:
            raise TypeError("character does'nt fit in matrix rows")
        if type( startcolumn ) is not int or startcolumn < 1 or startcolumn + 4 > self.columns:
            raise TypeError("character does'nt fit in matrix columns")
        for x in range(7):
            for y in range(5):
                if digit_7x5[char][x][y] == 0:
                    self.row[startrow+x-1].pixel[startcolumn+y-1].set2off( )
                else:
                    self.row[startrow+x-1].pixel[startcolumn+y-1].set2color( red, green, blue )

    def set7x5text( self, text=' ', red=84, green=84, blue=84, replace=False):
        if not replace:
            self.setall2off()
        column = 1
        for char in text:
            if not ( replace and char == ' ' ):
                self.set7x5char( char, 1, column, red, green, blue )
            column += 7
            
            
if __name__ == "__main__":
    import sys
    import math
    if len(sys.argv) == 2:
        print ( "LedStripTest" )
        strip = LedStrip(int(sys.argv[1]))
        strip.setall2off()
        delay = 1 / math.sqrt(50 * strip.pixels)
        for runs in range(5):
            strip.pixel[0].set2green()
            strip.pixel[1].set2yellow()
            strip.pixel[2].set2blue()
            for x in range(3,strip.pixels):
                strip.rotate_right()
                strip.show()
                time.sleep(delay)
            strip.pixel[strip.pixels - 1].set2green()
            strip.pixel[strip.pixels - 2].set2yellow()
            strip.pixel[strip.pixels - 3].set2blue()
            for x in range(3,strip.pixels):
                strip.rotate_left()
                strip.show()
                time.sleep(delay)
        strip.setall2off()
        strip.show()
        print( "bye" )
    elif len(sys.argv) == 3:
        print ( "LedMatrixTest" )
        matrix = LedMatrix(int(sys.argv[1]),int(sys.argv[2]))
        matrix.setall2off()
        delay = 1 / math.sqrt(5 * matrix.rows)
        for x in range(matrix.rows):
            for y in range(matrix.columns):
                if x % 7 == 0 :
                    matrix.row[x].pixel[y].set2red() 
                elif x % 7 == 1 :
                    matrix.row[x].pixel[y].set2green()
                elif x % 7 == 2 :
                    matrix.row[x].pixel[y].set2blue()
                elif x % 7 == 3 :
                    matrix.row[x].pixel[y].set2cyan()
                elif x % 7 == 4 :
                    matrix.row[x].pixel[y].set2magenta()
                elif x % 7 == 5 :
                    matrix.row[x].pixel[y].set2yellow()
                elif x % 7 == 6 :
                    matrix.row[x].pixel[y].set2white()
        for runs in range( 5 * matrix.rows):
            matrix.show()
            time.sleep(delay)
            matrix.rotate_up()
        matrix.setall2off()
        matrix.show()
        print( "bye" )
    else:
        print ( " usage: myLedMatrix <pixel> or myLedMatrix <rows> <colums>" )
        
                       

    

    
    

    

    



