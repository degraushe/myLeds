from bluedot import BlueDot
from colorsys import hsv_to_rgb
from time import sleep

from myLedMatrix import LedVirtualMatrix

waitForBtCommand = True
scrollValue = 0

def double_pressed(position):
   global waitForBtCommand
   global scrollValue
   if position.left:
      scrollValue -= 1
   elif position.right:
      scrollValue += 1
   elif position.top:
      scrollValue = 0
   elif position.middle:
      m.setall2off()
   else:
      m.setall2off()
      waitForBtCommand = False
   m.show()

def swiped(swipe):
   rgb = [ 0, 0, 0 ]
#   print("Swiped")
#   print("speed=",format(swipe.speed))
#   print("angle=",format(swipe.angle))
#   print("distance",format(swipe.distance))
   if swipe.angle < 0:
      angle_float = ( 360 + swipe.angle ) / 360
   else:
      angle_float = swipe.angle / 360
   speed_float = min( swipe.speed / 5.0 - 0.2 , 1.0)
#   print("angle=",format(angle_float))
#   print("speed=",format(speed_float))
   rgb = hsv_to_rgb( angle_float, 1.0, speed_float )
#   print ("Rot=", rgb[0] )
#   print ("Green=", rgb[1] )
#   print ("Blue=", rgb[2] )
   m.changeall2color ( int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
   m.show()

if __name__ == "__main__":
   import sys
   if len(sys.argv) == 2:
      myText = str(sys.argv[1])
      myTextLenght = len ( myText )
      myColumns = int( ( myTextLenght + 1 ) * 6 )
#
      m = LedVirtualMatrix(7, myColumns, 7, 30)
#
      bd = BlueDot()
      bd.when_swiped = swiped
      bd.when_double_pressed = double_pressed
      while waitForBtCommand:
         if scrollValue > 0:
            [ m.rotate_left() for x in range( scrollValue ) ]
         elif scrollValue < 0:
            [ m.rotate_right() for x in range( abs(scrollValue) ) ]
         else:   
            m.set7x5text(myText)
         m.show()
         sleep(0.1)
      print('Bye')
   else:
      print ( " usage: python3 BdTextScroll.py <text>" )

   
