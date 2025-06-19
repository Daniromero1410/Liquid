from machine import ADC, Pin
import network
import urequests
import time
import json

# Configurar el pin ADC para el higrómetro
sensor_pin = ADC(Pin(32))
sensor_pin.atten(ADC.ATTN_11DB)  # Configurar atenuación para el rango completo de 3.3v

wifi_config = {
    'ssid': '',
    'password': ''
}

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Desactivar el modo de punto de acceso
    network.WLAN(network.AP_IF).active(False)

    if not wlan.isconnected():
        print('Conectando a WiFi...')
        wlan.connect(wifi_config['ssid'], wifi_config['password'])
        while not wlan.isconnected():
            pass
    print("Conexión WiFi establecida")
    print('Dirección IP:', wlan.ifconfig()[0])

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def enviar_datos(sensor_value, humidity_percent):
    url = "http://tu_ip:puerto/accounts/receive/"
    
    data = {
        "sensor_value": sensor_value,
        "humidity_percent": humidity_percent
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = urequests.post(url, json=data, headers=headers)
        print("Respuesta del servidor:", response.text)
        response.close()
    except Exception as e:
        print("Error al enviar datos:", str(e))

def main():
    connect_wifi()
    
    while True:
        # Leer el valor analógico del sensor
        sensor_value = sensor_pin.read()
        
        # Mapear el valor a un porcentaje de humedad
        humidity_percent = map_value(sensor_value, 0, 4095, 100, 0)
        
        # Imprimir los resultados
        print("Valor del sensor:", sensor_value)
        print("Porcentaje de humedad: {}%".format(humidity_percent))
        print("------------------------")
        
        # Enviar datos al servidor
        enviar_datos(sensor_value, humidity_percent)
        
        time.sleep(1)  # Esperar 1 segundos antes de la siguiente lectura

if __name__ == "__main__":
    main()
