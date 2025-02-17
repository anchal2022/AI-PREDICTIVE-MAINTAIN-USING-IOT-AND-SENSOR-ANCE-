import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import serial  # For Arduino communication

# Arduino serial port configuration
SERIAL_PORT = "COM6"  # Update with your Arduino's COM port
BAUD_RATE = 9600

# Step 1: Load or Generate Dataset
def generate_dataset():
    # Simulated data for training
    data = {
        "temperature": [30, 65, 75, 40, 20, 85],
        "distance": [40, 20, 15, 60, 70, 10],  # Ultrasonic distance in cm
        "current": [5, 12, 15, 8, 3, 14],  # Current in Amperes
        "fault": ["No Fault", "Overheating", "Overcurrent", "No Fault", "No Fault", "Obstacle Detected"]
    }
    return pd.DataFrame(data)

# Step 2: Prepare Dataset
df = generate_dataset()
X = df[["temperature",  "distance", "current"]]  # Features
y = df["fault"]  # Labels

# Step 3: Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train the Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 5: Evaluate the Model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Step 6: Save the Model
with open("sensor_fault_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Step 7: Predict Function for Real-Time Use
def predict_fault(temperature,  distance, current):
    with open("sensor_fault_model.pkl", "rb") as file:
        loaded_model = pickle.load(file)
    input_data = [[temperature, distance, current]]
    prediction = loaded_model.predict(input_data)
    return prediction[0]

# Step 8: Fetch Data from Arduino
def get_real_time_data():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            # Read data from Arduino
            line = ser.readline().decode('utf-8').strip()
            # Assuming Arduino sends data as: temperature,vibration,distance,current
            temp,  dist, curr = map(float, line.split(','))
            return {
                "temperature": temp,
                "distance": dist,
                "current": curr
            }
    except Exception as e:
        print(f"Error reading from Arduino: {e}")
        return None

if __name__ == "__main__":
    while True:
        real_time_data = get_real_time_data()
        if real_time_data:
            fault = predict_fault(
                real_time_data["temperature"],
                real_time_data["distance"],
                real_time_data["current"]
            )
            print(f"Predicted Fault: {fault}")
