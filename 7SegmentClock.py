from myLedMatrix import LedStrip
from time import sleep
from datetime import datetime

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

# pixel color & brightness
red = 128
green = 128
blue = 128
brightness = 128

# initializing the LED 7Segment panel
panel = LedStrip(117)
panel.setall2off()
panel.setall2brightness(brightness)
panel.show()

# handling of TERM signal
def receivedTERM( signalNumber, frame ):
    raise KeyboardInterrupt()
    return

# register signal handler
signal.signal( signal.SIGTERM, receivedTERM )

## display time
old_second = 60
while True:
    try:
        now = datetime.now()
        if now.second == old_second:
            sleep(0.05)
            continue
        old_second = now.second
        if DEBUG: print(now.second)
# set hour segments - 12H modus
        if now.hour == 12: hour = now.hour
        else: hour = now.hour % 12
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
        panel.show()
    except KeyboardInterrupt:
        break

# clean exit
panel.setall2off()
panel.show()

