import Adafruit_DHT
import json
from cryptography.fernet import Fernet

#Details for retrieving sensor info
Sensor = Adafruit_DHT.DHT11
Pin = 4

#Private class
class _Encrypt:
    #Intialize key
    def __init__(self):
        self.key = Fernet.generate_key()
        self.f = Fernet(self.key)
    
    #Retrieve and convert data into json. COnvert json into bytes and encrypt
    def _collectData(self):
        humidity, temperature = Adafruit_DHT.read_retry(Sensor, Pin)
        data = {"temperature": temperature, "humidity": humidity}
        encryptedData = self.f.encrypt(bytes(json.dumps(data), 'utf-8'))
        print(encryptedData.decode())


if __name__ == '__main__':
    _Encrypt()._collectData()
    
    