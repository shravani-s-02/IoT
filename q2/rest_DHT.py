from flask import Flask, jsonify
import pymysql
import Adafruit_DHT
from threading import Thread
import requests
import time

app = Flask(__name__)

#Details to connect to database
Host = "localhost"
User = "pi"
Password = "raspberry99"
Database = "19mcme01"

#Details to retrieve sensor info
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

#POST method to upload data to table in database 
@app.route('/', methods=['POST'])
def storeData():
    humidity, temperature = Adafruit_DHT.read_retry(Sensor, Pin)
    
    if humidity is not None and temperature is not None:
        conn = pymysql.connect(host=Host, user = User, password = Password, database = Database)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO DHT_data (temperature, humidity) VALUES (%s, %s)", (temperature, humidity))
        conn.commit()
        conn.close()
        return jsonify({"message": "Data added"}), 201
    else:
        return jsonify({"error": "Failed to retrieve sensor data"}), 500

#GET method to retrieve all data from table in database (in json format)
@app.route('/', methods=['GET'])
def get_sensor_data():
    conn = pymysql.connect(host=Host, user = User, password = Password, database = Database)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DHT_data")
    rows = cursor.fetchall()
    conn.close()

    data = [{"id": row[0], "temperature": row[1], "humidity": row[2]} for row in rows]

    return jsonify(data)

#Function to continously call POST method for 24hrs
def get_and_store_data():
    timeout = 60 * 60 * 24
    time_start = time.time()
    try:
        while time.time() < time_start + timeout:
            result = requests.post("http://127.0.01:8080/")
            data = result.json()
            for key in data:
                if key == "error":
                    break
    except KeyboardInterrupt:
            print("Program terminated\n")

#Collection is run as a seperate process via thread in order for POST method to be continously called
if __name__ == '__main__':
    intializeDB()
    
    sensor_thread = Thread(target=get_and_store_data)
    sensor_thread.daemon = True
    sensor_thread.start()
    app.run(debug=True, port = "8080")