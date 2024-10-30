from machine import ADC, Pin
import network
import urequests
import time
import json

# Configure ADC pin for hygrometer
sensor_pin = ADC(Pin(32))
sensor_pin.atten(ADC.ATTN_11DB)

# Server configuration - Update with your Django server's IP and port
SERVER_URL = "http://127.0.0.1:8000//accounts/api/sensor-data/"

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)
        retry_count = 0
        while not wlan.isconnected() and retry_count < 20:
            time.sleep(1)
            retry_count += 1
        if not wlan.isconnected():
            raise Exception("Failed to connect to WiFi")
    print("WiFi Connected")
    print('IP Address:', wlan.ifconfig()[0])

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def send_data(sensor_value, humidity_percent):
    data = {
        "sensor_value": sensor_value,
        "humidity_percent": humidity_percent
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = urequests.post(SERVER_URL, json=data, headers=headers)
        result = response.json()
        print("Server response:", result)
        response.close()
        return result
    except Exception as e:
        print("Error sending data:", str(e))
        return None

def main():
    # WiFi credentials - update these
    ssid = "FAMILIA-ROMERO"
    password = "Fernando01."
    
    try:
        connect_wifi(ssid, password)
        
        while True:
            try:
                # Read sensor
                sensor_value = sensor_pin.read()
                humidity_percent = map_value(sensor_value, 0, 4095, 100, 0)
                
                # Print local values
                print(f"Sensor value: {sensor_value}")
                print(f"Humidity: {humidity_percent}%")
                print("-" * 40)
                
                # Send to server
                result = send_data(sensor_value, humidity_percent)
                if result and result.get('status') == 'success':
                    print("Data successfully saved to database")
                
                # Wait before next reading
                time.sleep(2)
                
            except Exception as e:
                print("Error in sensor reading:", str(e))
                time.sleep(5)
    
    except Exception as e:
        print("Fatal error:", str(e))
        machine.reset()

if __name__ == "__main__":
    main()