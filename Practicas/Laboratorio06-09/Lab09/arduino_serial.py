# Script Python para comunicarse con Arduino
# pip install pyserial
import serial
import json
import time

arduino = serial.Serial('COM4', 115200, timeout=1)  # Cambia el puerto si es necesario
time.sleep(2)

def enviar(cmd):
    arduino.write((cmd + '\n').encode())

    while True:
        linea = arduino.readline().decode(errors='ignore').strip()

        if not linea:
            return None

        # Solo intentar parsear si parece JSON
        if linea.startswith('{'):
            try:
                return json.loads(linea)
            except:
                print("JSON mal formado:", linea)
                return None
        else:
            print("Ignorando:", linea)

print('Conectado:', enviar('ALL'))

# Ciclo de monitoreo
for _ in range(5):
    resp = enviar('ALL')
    
    if resp and 'data' in resp:
        d = resp['data']
        print(f"Temp: {d['temp']}°C Hum: {d['hum']}% Luz: {d['luz']}")
    else:
        print("Sin datos válidos")

    time.sleep(3)

enviar('LED:ON')
time.sleep(1)
enviar('LED:OFF')

arduino.close()