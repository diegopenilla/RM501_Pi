import serial

# Initialize serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600)  # replace '/dev/ttyACM0' with your port

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(f"Received message: {line}")
except KeyboardInterrupt:
    print("Program interrupted. Exiting.")
finally:
    ser.close()