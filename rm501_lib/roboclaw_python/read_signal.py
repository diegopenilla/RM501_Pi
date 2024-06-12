import serial
import time
import pick_paper  # import the pick_paper module

# Initialize serial connection
ser = serial.Serial('/dev/CoinAcceptor', 9600)  # replace '/dev/ttyACM0' with your port

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line == "coin":
                robot_arm = pick_paper.RobotArm("/dev/RM501", 115200)
                robot_arm.initialize_and_execute("kpr_positions.csv")

            time.sleep(10)
except KeyboardInterrupt:
    print("Program interrupted. Exiting.")
finally:
    ser.close()