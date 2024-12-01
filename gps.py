import serial
import time
import json
import requests

gps_serial = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

def parse_gps(data):
    if data[0:6] == "$GPGGA":
        parts = data.split(',')
        if parts[2] and parts[4]:
            latitude = parts[2]
            longitude = parts[4]
            print("latitude: ", latitude)
            print("longitude: ", longitude)
            return {
                "latitude": latitude,
                "longitude": longitude
            }
        else:
            print("No GPS fix yet.")
            return None
        return None


def send_gps_data(endpoint, gps_data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(endpoint, json=gps_data, headers=headers)
        if response.status_code == 200:
            print("Data sent successfully:", response.json())
        else:
            print("Failed to send data. Status code:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print("Error while sending data:", str(e))

endpoint = "http://umay.develop-er.org/upload-gps"
while True:
    line = gps_serial.readline().decode('ascii', errors='replace').strip()
    if line:
        gps_data = parse_gps(line)
        if gps_data != None:
            send_gps_data(endpoint, gps_data)
    time.sleep(0.1)

