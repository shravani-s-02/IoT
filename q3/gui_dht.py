import tkinter as tk
from flask import Flask
import pymysql
import Adafruit_DHT
import time

root = tk.Tk()

app = Flask(__name__)

#Details to connect to database
Host = "localhost"
User = "pi"
Password = "raspberry99"
Database = "19mcme01"

#Details to retrive sensor data
Sensor = Adafruit_DHT.DHT11
Pin = 4

#Create DB and table if not created
def intializeDB():
    conn = pymysql.connect(host = Host, user = User, password = Password)
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS 19mcme01')
    conn.commit()
    conn.close()

    conn = pymysql.connect(host=Host, user = User, password = Password, database = Database)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS DHT_data (id INT AUTO_INCREMENT PRIMARY KEY, temperature FLOAT, humidity FLOAT)')
    conn.commit()
    conn.close()

#GUI
class SensorApp:
    #Intialize GUI(labels and button)
    def __init__(self, master):
        self.master = master
        master.title("Sensor Data Collector")

        self.label1 = tk.Label(master, text="Temperature:")
        self.label1.pack()
    
        self.temp_label = tk.Label(master, text="")
        self.temp_label.pack()

        self.label2 = tk.Label(master, text="Humidity:")
        self.label2.pack()

        self.humidity_label = tk.Label(master, text="")
        self.humidity_label.pack()

        self.collect_button = tk.Button(master, text="Start collection", command=self.collect_and_store)
        self.collect_button.pack()

    #Loop for 24 hr and store data in database as well as insert into GUI
    def collect_and_store(self):
        timeout = 60*60*24
        time_start = time.time()
        try:
            while time.time() < time_start + timeout:
                humidity, temperature = Adafruit_DHT.read_retry(Sensor, Pin)
                if humidity is not None and temperature is not None:
                    self.temp_label.configure(text="{:.2f}°C".format(temperature))
                    self.humidity_label.configure(text="{:.2f}%".format(humidity))
                    
                    root.update()
                    
                    conn = pymysql.connect(host=Host, user = User, password = Password, database = Database)
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO DHT_data (temperature, humidity) VALUES (%s, %s)", (temperature, humidity))
                    conn.commit()
                    conn.close()
                else:
                    self.temp_label.config(text="Failed to retrieve sensor data.")
                    self.humidity_label.config(text="")
                    break
                print(temperature,humidity)
        except KeyboardInterrupt:
            print("Program terminated\n")
            
def main():
    app = SensorApp(root)
    root.mainloop()

if __name__ == '__main__':
    intializeDB()
    main() 

