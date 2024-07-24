import tkinter as tk
import paho.mqtt.client as mqtt
import thingspeak
import threading

#Details for connecting to broker
broker = "mqtt3.thingspeak.com"
port = 1883
username = "NSo7DRolEyQDCBUUEjAjADc"
password = "vaO8ej6VvH5DIMN01Z0ETC/N"
client_id = "NSo7DRolEyQDCBUUEjAjADc"

#Details for subscribing to topic
channelID = "2476822"
readAPIKey = "IECR6GT64ZV8Q3DI"
topic = "channels/" + channelID + "/subscribe/fields/+" 

client = mqtt.Client(client_id, mqtt.MQTTv31)

#Subscribe GUI
class MQTTSubscribeApp:
    #Intialize GUI(labels and buttons)
    def __init__(self, master):
        self.master = master
        master.title("MQTT Subscribe")
        
        self.message_label = tk.Label(master, text="Messages")
        self.message_label.pack()
        
        self.message_text = tk.Text(master, height=10, width=50)
        self.message_text.pack()
        
        #Connect button
        self.connect_button = tk.Button(master, text="Connect", command=self.connect_mqtt)
        self.connect_button.pack()
        
        #Disconnect button
        self.disconnect_button = tk.Button(master, text="Disconnect", command=self.disconnect_mqtt, state=tk.DISABLED)
        self.disconnect_button.pack()
        
        self.mqtt_client = client
        
        self.mqtt_client.username_pw_set(username, password)

    #Connect button function in which broker is connected to
    def connect_mqtt(self):
        self.mqtt_client.connect(broker, port, keepalive=60, bind_address="")
        self.mqtt_client.loop_start()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.disconnect_button.config(state=tk.NORMAL)
        self.connect_button.config(state=tk.DISABLED)

    #Disconnect button function in which looping is stopped and broker is disconnected from
    def disconnect_mqtt(self):
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()
        self.disconnect_button.config(state=tk.DISABLED)
        self.connect_button.config(state=tk.NORMAL)
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("rc:"+str(rc))
            print(self.mqtt_client.subscribe(topic,0))
 
    def on_message(self, client, userdata, msg):
        print("recieved message\n")
        message = "temperature,humidity:" + msg.payload + "\n"
        self.message_text.insert(tk.END, message)
    
def main():
    root = tk.Tk()
    app = MQTTSubscribeApp(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()

