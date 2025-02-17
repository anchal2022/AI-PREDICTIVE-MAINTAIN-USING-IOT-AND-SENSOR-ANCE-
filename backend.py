import serial
import time

try:
    arduino = serial.Serial('COM6', 9600, timeout=1)
    time.sleep(2)  # Wait for connection to initialize
    print("Arduino connected successfully!")
    while True:
        data = arduino.readline().decode('utf-8').strip()
        if data:
            print(f"Received: {data}")
except Exception as e:
    print(f"Error: {e}")