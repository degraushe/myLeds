from myLedMatrix import LedMatrix
import time
import datetime

# initializing the LED matrix
m = LedMatrix(7, 30)
m.setall2off()
m.setall2brightness(64)
m.show()

# display time
old_second = 60
while True:
    try:
        now = datetime.datetime.now()
        if now.second == old_second:
            time.sleep(0.05)
            continue
        old_second = now.second
#
        hour = '{:%H}'.format(now) 
        m.set5x3char( hour[0:1],2, 2 ) 
        m.set5x3char( hour[1:2],2, 6 ) 
#
        m.set2color(3,10)
        m.set2color(5,10)
#
        minute = '{:%M}'.format(now) 
        m.set5x3char( minute[0:1],2, 12 ) 
        m.set5x3char( minute[1:2],2, 16 ) 
#
        m.set2color(3,20)
        m.set2color(5,20)
#
        second = '{:%S}'.format(now) 
        m.set5x3char( second[0:1],2, 22 ) 
        m.set5x3char( second[1:2],2, 26 ) 

#
        rgb = [ ( 247 - now.second % 20 * 13 ),
                ( now.second % 20 * 13 ), 0 ]
        for i in range ( now.second // 20 * 2 ):
            rgb.append( rgb.pop(0) )
        m.changeall2color( rgb[0], rgb[1], rgb[2] )
#
        m.show()
    except KeyboardInterrupt:
        break
    
# clean exit
m.setall2off()
m.show()
