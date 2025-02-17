import random
import serial  # For real-time data from Arduino

# Initialize Serial Communication
try:
    arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)  # Replace 'COM6' with your Arduino's COM port
    print("Connected to Arduino")
except Exception as e:
    arduino = None
    print(f"Error connecting to Arduino: {e}")

def get_sensor_data():
    """
    Function to fetch real-time sensor data from Arduino.
    Falls back to simulated data if Arduino is not connected.
    """
    data = {}

    if arduino and arduino.is_open:
        try:
            # Read real-time data from Arduino
            arduino.write(b"GET\n")  # Send a request to Arduino
            line = arduino.readline().decode('utf-8').strip()

            if line:
                # Assuming Arduino sends data as a comma-separated string: "temperature,vibration,distance,current"
                temperature, vibration, distance, current = map(str.strip, line.split(","))
                data = {
                    "temperature": float(temperature),
                    "distance": float(distance),
                    "current": float(current)
                }
            else:
                print("No data received from Arduino, using simulated data.")
                data = generate_simulated_data()
        except Exception as e:
            print(f"Error reading from Arduino: {e}. Using simulated data.")
            data = generate_simulated_data()
    else:
        print("Arduino not connected. Using simulated data.")
        data = generate_simulated_data()

    # Fault and Reason Logic
    data["temperature_fault"] = "Overheating" if data["temperature"] > 60 else "Normal"
    data["temperature_reason"] = "High machine load" if data["temperature"] > 60 else "Temperature within safe range"

    data["distance_fault"] = "Obstacle Detected" if data["distance"] < 30 else "Clear"
    data["distance_reason"] = "Object near the machine" if data["distance"] < 30 else "No obstacles detected"

    data["current_fault"] = "Overcurrent" if data["current"] > 10 else "Normal"
    data["current_reason"] = "Electrical overload or short circuit" if data["current"] > 10 else "Current within safe range"

    return data

def generate_simulated_data():
    """
    Generates simulated data for fallback.
    """
    return {
        "temperature": round(random.uniform(20, 70), 2),  # Temperature in °C
        "vibration": random.choice(["Normal", "High"]),   # Vibration status
        "distance": round(random.uniform(10, 100), 2),    # Ultrasonic Distance in cm
        "current": round(random.uniform(0, 15), 2)        # Current in Amperes
    }

# Example Usage
if __name__ == "__main__":
    while True:
        sensor_data = get_sensor_data()
        print(sensor_data)
