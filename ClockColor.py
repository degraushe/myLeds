from myLedMatrix import LedMatrix
import time
import datetime

# initializing the LED matrix
m = LedMatrix(7, 30)
m.setall2off()
m.setall2brightness(128)
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
        if now.second % 5 != 0:
            m.set7x5text( '{:%H:%M}'.format(now) )
        else:
            m.set7x5text( '{:%H %M}'.format(now) )
        rgb = [ ( 247 - now.second % 20 * 13 ),
                ( now.second % 20 * 13 ), 0 ]
        for i in range ( now.second // 20 * 2 ):
            rgb.append( rgb.pop(0) )
        m.changeall2color( rgb[0], rgb[1], rgb[2] )
        pixel = now.second % 30
        row = now.second // 30 * 6
        m.row[row].pixel[pixel].set2red()
        m.show()
    except KeyboardInterrupt:
        break
    
# clean exit
m.setall2off()
m.show()
