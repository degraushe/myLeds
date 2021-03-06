__version__ = '0.2.0'

import spidev
import time
import random


from digit_7x5 import digit_7x5
from digit_5x3 import digit_5x3

LED_TYPE = ("APA102", "SK9822")

# limit power consumption - maximum in mA
power_limit = 9000

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

    def change2color(self, new_red=0, new_green=0, new_blue=0 ):
        if self.red > 0 or self.green > 0 or self.blue > 0:
            self.set2color( new_red, new_green, new_blue )
        
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
        if not ( type(pixels) is int and 2 <= pixels <= 1000 ):
            raise TypeError("pixels value must be 2..1000")
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

    def change2color(self, pixel=None, new_red=0, new_green=0, new_blue=0):
        if not ( type(pixel) is int and 1 <= pixel <= self.pixels ):
            raise TypeError("invalid pixel value")
        self.pixel[pixel-1].change2color(new_red, new_green, new_blue)

       
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
        # limit power consumption
        global power_limit
        power_total = 0
        # build data output array
        # start frames
        self.databytes = [ 0x00, 0x00, 0x00, 0x00 ]
        # data frames
        for x in self.pixel:
            self.databytes = self.databytes + x.databytes
            power = ( x.databytes[1] * 20 / 255 +
                      x.databytes[2] * 20 / 255 +
                      x.databytes[3] * 20 / 255 ) * ( x.databytes[0] % 32 ) / 31
            power_total += power  
        # refresh frames for SK9822
        if self.led_type == LED_TYPE[1]: 
            self.databytes = self.databytes + [ 0x00, 0x00, 0x00, 0x00 ]
        # additional clocks ticks - 1/2 per pixel
        for x in range ( ( ( self.pixels - 1 ) // 2 + 1 ) // 8 + 1 ):
            self.databytes = self.databytes + [ 0x00 ]
        # write to LED using SPI - respect power limit 
        if power_total < power_limit :
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
        if type( rows ) is not int or rows < 2 or rows > 79:
            raise TypeError("rows value must be 2..79")
        self.rows = rows
        if type( columns ) is not int or columns < 2 or columns > 1000:
            raise TypeError("columns value must be 2..1000")
        self.columns = columns
        self.row = [ LedStrip( columns, led_type ) for x in range ( rows ) ]
        
    def setall2brightness(self, brightness=32):
        [ self.row[x].pixel[y].set2brightness( brightness )
          for x in range ( self.rows ) for y in range ( self.columns )]
        
    def setall2off(self):
        [ self.row[x].pixel[y].set2off( )
          for x in range ( self.rows ) for y in range ( self.columns )]

    def changeall2color(self, new_red=0, new_green=0, new_blue=0):
        [ self.row[x].pixel[y].change2color( new_red, new_green, new_blue )
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

    def setall2random(self):
        [ self.row[x].setall2random( ) for x in range ( self.rows ) ]
                

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
        # limit power consumption
        global power_limit
        power_total = 0
        # start frames
        self.databytes = [ 0x00, 0x00, 0x00, 0x00 ] 
        for x in range ( self.rows ):  # serpent 1,1-1,n, 2,n-2,1, 3.1-3,n, ...
            if x % 2 == 0:
                for y in self.row[x].pixel:
                    self.databytes = self.databytes + y.databytes
                    power = ( y.databytes[1] * 20 / 255 +
                              y.databytes[2] * 20 / 255 +
                              y.databytes[3] * 20 / 255 ) * ( y.databytes[0] % 32 ) / 31
                    power_total += power
            else:
                for y in reversed(self.row[x].pixel):
                    self.databytes = self.databytes + y.databytes
                    power = ( y.databytes[1] * 20 / 255 +
                              y.databytes[2] * 20 / 255 +
                              y.databytes[3] * 20 / 255 ) * ( y.databytes[0] % 32 ) / 31
                    power_total += power  
        if self.led_type == LED_TYPE[1]:  # refresh bytes for SK9822
            self.databytes = self.databytes + [ 0x00, 0x00, 0x00, 0x00 ]
        for x in range ( ( ( self.rows * self.columns - 1 ) // 2 + 1 ) // 8 + 1 ):
            # additional clocks ticks - 1/2 per row
            self.databytes = self.databytes + [ 0x00 ]
        # write to LED using SPI - respect power limit 
        if power_total < power_limit :
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
            
                         

    def set2color( self, row=1, column=1, red=84, green=84, blue=84):
        if type( row ) is not int or row < 1 or row  > self.rows:
            raise TypeError("pixel does'nt fit in matrix rows")
        if type( column ) is not int or column < 1 or column > self.columns:
            raise TypeError("pixel does'nt fit in matrix columns")
        self.row[row-1].pixel[column-1].set2color( red, green, blue )

    def set5x3char( self, char=' ', startrow=1, startcolumn=1, red=84, green=84, blue=84):
        if type( startrow ) is not int or startrow < 1 or startrow + 4 > self.rows:
            raise TypeError("character does'nt fit in matrix rows")
        if type( startcolumn ) is not int or startcolumn < 1 or startcolumn + 3 > self.columns:
            raise TypeError("character does'nt fit in matrix columns")
        for x in range(5):
            for y in range(3):
                if digit_5x3[char][x][y] == 0:
                    self.row[startrow+x-1].pixel[startcolumn+y-1].set2off( )
                else:
                    self.row[startrow+x-1].pixel[startcolumn+y-1].set2color( red, green, blue )

    def set5x3text( self, text=' ', red=84, green=84, blue=84, replace=False):
        if not replace:
            self.setall2off()
        column = 1
        for char in text:
            if not ( replace and char == ' ' ):
                self.set5x3char( char, 1, column, red, green, blue )
            column += 4

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
            column += 6

class LedVirtualMatrix( LedMatrix ):
    def __init__( self, rows=30, columns=300, ledRows=7, ledColumns=30, led_type=LED_TYPE[1] ):
        if led_type not in LED_TYPE:
            raise TypeError("unknown LED type, use APA102 or SK9822")
        self.led_type = led_type
        if type( ledRows ) is not int or ledRows < 2 or ledRows > 16:
            raise TypeError("led rows value must be 2..16")
        self.ledRows = ledRows
        if type( ledColumns ) is not int or ledColumns < 2 or ledColumns > 64:
            raise TypeError("led columns value must be 2..64")
        self.ledColumns = ledColumns

        LedMatrix.__init__( self, rows, columns, led_type )

        if self.ledRows > self.rows:
            raise TypeError("rows value must be equal or greater than led rows value")
        if self.ledColumns > self.columns:
            raise TypeError("columns value must be equal or greater than led columns value")

    def show(self, startRow=1, startColumn=1):
        # keep window in virtual matrix
        self.startRow = ( startRow - 1 ) % ( self.rows - self.ledRows + 1 ) + 1
        self.startColumn = ( startColumn - 1 ) % ( self.columns - self.ledColumns + 1 ) + 1
        # start frames    
        self.databytes = [ 0x00, 0x00, 0x00, 0x00 ]  
        # serpent 1,1-1,n, 2,n-2,1, 3.1-3,n, ...
        for x in range ( self.ledRows ):
            xLed = x + self.startRow - 1
            for y in range ( self.ledColumns ):
                yLed = ( self.startColumn - 1 ) + y
                if x % 2 == 1:
                    yLed = ( self.startColumn - 1 ) + ( self.ledColumns - 1 ) - y 
                self.databytes = self.databytes + self.row[ xLed ].pixel[ yLed ].databytes
        # refresh bytes for SK9822
        if self.led_type == LED_TYPE[1]:  
            self.databytes = self.databytes + [ 0x00, 0x00, 0x00, 0x00 ]
        # additional clocks ticks - 1/2 per row
        for x in range ( ( ( self.ledRows * self.ledColumns - 1 ) // 2 + 1 ) // 8 + 1 ):
            self.databytes = self.databytes + [ 0x00 ]
        # write to LED using SPI
        spi = spidev.SpiDev()
        spi.open(0, 1)
        spi.max_speed_hz=8000000
        spi.xfer2( self.databytes )
        spi.close()


           
            
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
        for runs in range( 50 ):
            matrix.setall2random()
            matrix.show()
            time.sleep( 0.2 )
        matrix.setall2off()
        matrix.show()
        print( "bye" )
    else:
        print ( " usage: myLedMatrix <pixel> or myLedMatrix <rows> <colums>" )
        
                       

    

    
    

    

    



