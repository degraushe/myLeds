from myLedMatrix import LedStrip
from bluedot import BlueDot
from colorsys import hsv_to_rgb
from time import sleep
from datetime import datetime

import json
import signal

DEBUG = False

# numbers on 7Segment panel - 0..9
n7s = [ [1,1,1,0,1,1,1],
        [0,0,1,0,0,0,1],
        [0,1,1,1,1,1,0],
        [0,1,1,1,0,1,1],
        [1,0,1,1,0,0,1],
        [1,1,0,1,0,1,1],
        [1,1,0,1,1,1,1],
        [0,1,1,0,0,0,1],
        [1,1,1,1,1,1,1],
        [1,1,1,1,0,1,1] ]

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

# initializing the LED 7Segment panel
panel = LedStrip(117)
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
        brightness = brightness // 2
    elif position.right:
        brightness = brightness + ( 255 - brightness ) // 2
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
    if brightness == 0 : break
    try:
        now = datetime.now()
        if now.second == old_second:
            sleep(0.05)
            continue
        old_second = now.second
        if DEBUG: print(now.second)
# set hour segments - 12H modus
        if now.hour == 12:
            hour = now.hour
        else:
            hour = now.hour % 12
        nr = hour // 10
        if DEBUG: print(nr)
        [ panel.set2color( led,
                           red * nr,
                           green * nr,
                           blue * nr ) for led in range ( 1,11 ) ]
# 
        nr = hour % 10
        if DEBUG: print(nr)
        [ panel.set2color( 11 + segment * 5 + led,
                           red * n7s[nr][segment],
                           green * n7s[nr][segment],
                           blue * n7s[nr][segment] ) for segment in range ( 7 )
                                                     for led in range ( 5 )]
# blink with hour / minute separator pixels
        nr = now.second % 2
        [ panel.set2color( 46 + led,
                           red * nr,
                           green * nr,
                           blue * nr ) for led in range ( 2 ) ]
# set minute segments
        nr = now.minute // 10
        if DEBUG: print(nr)
        [ panel.set2color( 48 + segment * 5 + led,
                           red * n7s[nr][segment],
                           green * n7s[nr][segment],
                           blue * n7s[nr][segment] ) for segment in range ( 7 )
                                                     for led in range ( 5 )]
#
        nr = now.minute % 10
        if DEBUG: print(nr)
        [ panel.set2color( 83 + segment * 5 + led,
                           red * n7s[nr][segment],
                           green * n7s[nr][segment],
                           blue * n7s[nr][segment] ) for segment in range ( 7 )
                                                     for led in range ( 5 )]

# ready to show on panel
        panel.setall2brightness(brightness)
        panel.show()
    except KeyboardInterrupt:
        break

# clean exit
panel.setall2off()
panel.show()

