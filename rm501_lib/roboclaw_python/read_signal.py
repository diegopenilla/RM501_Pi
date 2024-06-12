import serial
import time
import pick_paper  # import the pick_paper module

# Initialize serial connection
ser = serial.Serial('/dev/CoinAcceptor', 9600)  # replace '/dev/ttyACM0' with your port

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(f"Received message: {line}")

            # Call the main function of pick_paper
            pick_paper.main()  # replace with the actual function name if it's not 'execute_saved_positions'

            time.sleep(10)
except KeyboardInterrupt:
    print("Program interrupted. Exiting.")
finally:
    ser.close()