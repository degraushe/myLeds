import paho.mqtt.client as mqtt
import ssl
import time
from myLedMatrix import LedMatrix

# initializing the LED matrix
m = LedMatrix(7, 30)
m.setall2off()
m.show()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("CunjaBella/IT/LedMatrix/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    topic = msg.topic.split('/')[-1].lower()
    if topic == 'text':
        text = str(msg.payload,"utf-8")
        m.set7x5text(text[0:5])
        m.show()
    elif topic == 'farbe':
        farbe = str(msg.payload,"utf-8").lower().lstrip().rstrip()
        if farbe == 'rot':
            m.changeall2color(255,0,0)
        elif farbe == 'gruen':
            m.changeall2color(0,255,0)
        elif farbe == 'blau':
            m.changeall2color(0,0,255)
        else:
            m.changeall2color(128,128,128)
        m.show()
    elif topic == 'rgb':
        rgb = str(msg.payload,"utf-8").lower().lstrip().rstrip()[4:-1]
        [rot,gruen,blau] = rgb.split(',')
        m.changeall2color(int(rot),int(gruen),int(blau))
        m.show()
    elif topic == 'random':
        dauer = str(msg.payload,"utf-8").lower().lstrip().rstrip()
        if not dauer.isdecimal():
            dauer='3'
        for runs in range( int(dauer) * 5 ):
            m.setall2random()
            m.show()
            time.sleep(0.1)
        m.setall2off()
        m.show()
    elif topic == 'off':
        m.setall2off()
        m.show()
    elif topic == 'stop':
        client.disconnect()
    else:
        pass

# The callback for clean up on disconnect called.
def on_disconnect(client, userdata, rc):
    if rc == 0:
        print("Bye")
    else:
        print("Unexpected disconnection.")
    m.setall2off()
    m.show()

# connect as user LedMatrix01
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.tls_set(ca_certs="/home/pi/ssl/certs/LetsEncryptCAbundle.pem",
        certfile="/home/pi/ssl/certs/pi20170601-cert.pem",
        keyfile="/home/pi/ssl/certs/pi20170601-key.pem",
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLS,
        ciphers=None)
client.connect("mqtt.cunjabella.eu", 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
