#Taken from given MQTT publish demo

from __future__ import print_function
import paho.mqtt.publish as publish
import string
import Adafruit_DHT

channelID = "2476822"
writeAPIKey = "K0OOOBO0AR2L726S"
mqttHost = "mqtt3.thingspeak.com"
mqttUsername="NSo7DRolEyQDCBUUEjAjADc"
mqttclientid="NSo7DRolEyQDCBUUEjAjADc"
mqttpass="vaO8ej6VvH5DIMN01Z0ETC/N"
mqttAPIKey = "V6MY4M6PNVCJH6DA"
tTransport = "websockets"
tPort = 80
topic = "channels/" + channelID + "/publish"
sensor=Adafruit_DHT.DHT11
gpio=4


humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

while(1):

    if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
                print('Failed to get reading')

    payload = "field1=" + str(temperature) + "&field2=" + str(humidity)
    
    try:
        publish.single(topic, payload, hostname=mqttHost, transport=tTransport, port=tPort,client_id=mqttclientid,auth={'username':mqttUsername,'password':mqttpass})
    
    except (KeyboardInterrupt):
        break

    except:
        print ("There was an error while publishing the data.")

    
        








