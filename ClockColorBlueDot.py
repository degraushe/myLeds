from myLedMatrix import LedMatrix
from bluedot import BlueDot
from colorsys import hsv_to_rgb
from time import sleep
from datetime import datetime

import json
import signal

DEBUG = False

# read configuration values for color & brightness
try:
    with open( 'ClockPanel.json', 'r' ) as config:
        data = json.load( config )
        red = data["red"]
        green = data["green"]
        blue = data["blue"]
        brightness = data["brightness"]
except:
    red = 255
    green = 255
    blue = 255
    brightness = 64
    with open( 'ClockPanel.json', 'w' ) as config:
        json.dump( { "red":red, "green":green, "blue":blue, "brightness":brightness },
                     config, indent=4 )

# initializing the LED Matrix panel
panel = LedMatrix(7,30)
panel.setall2off()
panel.setall2brightness(brightness)
panel.show()

# BlueDot handling
# 
def swiped(swipe):
    global red, green, blue
    rgb = [ 0, 0, 0 ]
    if swipe.angle < 0: angle_float = ( 360 + swipe.angle ) / 360
    else: angle_float = swipe.angle / 360
    speed_float = min( swipe.speed / 5.0 - 0.2 , 1.0)
    rgb = hsv_to_rgb( angle_float, 1.0, speed_float )
    red = int(rgb[0]*255)
    green = int(rgb[1]*255)
    blue = int(rgb[2]*255)
#
def double_pressed(position):
    global red, green, blue, brightness
    if position.left:
        brightness = max ( 6, brightness // 3 * 2 )
    elif position.right:
        brightness = min( 254, brightness * 3 // 2 )
    elif position.top:
        red = 255
        green = 255
        blue = 255
        brightness = 64
    elif position.bottom:
        with open( 'ClockPanel.json', 'w' ) as config:
            json.dump( { "red":red,
                         "green":green,
                         "blue":blue,
                         "brightness":brightness }, config, indent=4 )
#
bd = BlueDot()
bd.when_swiped = swiped
bd.when_double_pressed = double_pressed

# handling of TERM signal
def receivedTERM( signalNumber, frame ):
    raise KeyboardInterrupt()
    return

# register signal handler
signal.signal( signal.SIGTERM, receivedTERM )

## display time
old_second = 60
while True:
#    if brightness == 0 : break
    try:
        now = datetime.now()
        if now.second == old_second:
            sleep(0.05)
            continue
        old_second = now.second
        if DEBUG: print(now.second)
# date & time
        if now.second % 5 != 0:
            panel.set7x5text( '{:%H:%M}'.format(now) )
        else:
            panel.set7x5text( '{:%H %M}'.format(now) )
        panel.changeall2color( red, green, blue )
# seconds as red pixel
        pixel = abs( now.second % 30 - 29 * (  now.second // 30 ) )
        row = now.second // 30 * 6
        panel.row[row].pixel[pixel].set2red()
# ready to show on panel
        panel.setall2brightness(brightness)
        panel.show()
    except KeyboardInterrupt:
        break

# clean exit
panel.setall2off()
panel.show()

