from myLedMatrix import LedStrip
import time
import datetime

# initializing the LED matrix
m = LedStrip(6)
m.setall2off()
m.setall2brightness(255)
m.show()

for i in range(1,7):
    m.set2fullwhite(i)
m.show()
time.sleep(10)
m.setall2off()
m.show()
time.sleep(3)

for i in range(1,7):
    m.set2fullwhite(i)
m.show()
time.sleep(10)
m.setall2off()
m.show()
time.sleep(3)

for i in range(1,7):
    m.set2fullwhite(i)
m.show()
time.sleep(10)
m.setall2off()
m.show()
time.sleep(3)

