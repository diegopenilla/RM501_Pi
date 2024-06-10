import serial

# Initialize serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)  # replace '/dev/ttyACM0' with your port

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(f"Received message: {line}")
        break