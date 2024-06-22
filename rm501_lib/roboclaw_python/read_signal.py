"""
PI starts listening to device configured CoinAcceptor by serial...

User should position the robot now in the standard position, completely upright.
with the claw orientation Red strip facing towards the paper pick-up area.

When coin is given the signal coin is received:
- this should trigger the robot to pick the paper
- in case of error mode -> replace stickers and press button 1..

When signal app1 is received -> Button 2 Press
- this should trigger the streamlit app to start

When signal app0 or Ready Mode is received -> Button 2 Press
- this should trigger the streamlit app to stop
"""

import serial
import time
import subprocess
import pick_paper

# Initialize serial connection
ser = serial.Serial('/dev/CoinAcceptor', 9600)  # replace '/dev/tty.usbserial-2120' with your port
streamlit_process = None

# TODO:
# 1. Determine duration of coreography to pick sticker define duration in seconds
duration = 20

def terminate_app():
    global streamlit_process
    if streamlit_process is not None:
        print("Terminating Streamlit app...")
        streamlit_process.terminate()
        streamlit_process = None
    else:
        print("Streamlit app is not running.")

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            if line == "Ready Mode":
                if streamlit_process is not None:
                    print("Terminating Streamlit app...")
                    streamlit_process.terminate()
                    streamlit_process = None
            elif line == "coin":
                print("COIN!!")
                try:
                    robot_arm = pick_paper.RobotArm("/dev/RM501", 115200)
                    robot_arm.initialize_and_execute("kpr_positions.csv")
                    time.sleep(duration)
                except Exception as e:
                    print("Coin received but connection not possible")

                # launch script python3 pick_paper.py
                # subprocess.Popen(['python3', 'pick_paper.py'])

            elif line == "app1":
                if streamlit_process is None:
                    print("Starting Streamlit app...")
                    streamlit_process = subprocess.Popen(['streamlit', 'run', 'app_csv_wrist.py'])
                else:
                    print("Streamlit app is already running.")
            elif line == "app0":
                if streamlit_process is not None:
                    terminate_app()
                else:
                    print("Streamlit app is not running.")

except KeyboardInterrupt:
    print("Program interrupted. Exiting.")
finally:
    if streamlit_process is not None:
        streamlit_process.terminate()
    ser.close()
