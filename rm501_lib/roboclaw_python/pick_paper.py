import time
import csv
from roboclaw_3 import Roboclaw

# Constants
ADDRESS1 = 0x80
ADDRESS2 = 0x81
ADDRESS3 = 0x82


# Initialize RoboClaw connection
def initialize_roboclaw(port="/dev/ttyUSB0", baudrate=115200):
    rc = Roboclaw(port, baudrate)
    rc.Open()
    return rc


# Close the gripper
def gripper_close(rc, step=0.2):
    rc.SpeedAccelM1(ADDRESS1, 3000, 3000)
    time.sleep(step)
    rc.SpeedAccelM1(ADDRESS1, 3000, 0)


# Open the gripper
def gripper_open(rc, step=0.2):
    rc.SpeedAccelM1(ADDRESS1, 3000, -3000)
    time.sleep(step)
    rc.SpeedAccelM1(ADDRESS1, 3000, 0)


# Update motor positions safely
def safe_update_motor_position(rc, motor_id, position):
    try:
        if motor_id == 1:
            rc.SpeedAccelDeccelPositionM2(ADDRESS1, 10000, 10000, 10000, position, 100)
        elif motor_id == 2:
            rc.SpeedAccelDeccelPositionM1(ADDRESS2, 10000, 10000, 10000, position, 100)
        elif motor_id == 3:
            rc.SpeedAccelDeccelPositionM2(ADDRESS2, 10000, 10000, 10000, position, 100)
    except Exception as e:
        print(f"Error updating motor {motor_id} position: {e}")


# Update wrist positions
def update_wrist_positions(rc, pos4, pos5):
    rc.SpeedAccelDeccelPositionM1(ADDRESS3, 2000, 10000, 10000, pos4, 100)
    time.sleep(0.05)
    rc.SpeedAccelDeccelPositionM2(ADDRESS3, 2000, 10000, 10000, pos5, 100)


# Update all motor positions
def update_motor_positions(rc, positions, gripper_closed):
    safe_update_motor_position(rc, 1, positions[0])
    safe_update_motor_position(rc, 2, positions[1])
    safe_update_motor_position(rc, 3, positions[2])
    update_wrist_positions(rc, positions[3], positions[4])

    if positions[5] and not gripper_closed:
        gripper_close(rc, 0.1)
        gripper_closed = True
    elif not positions[5] and gripper_closed:
        gripper_open(rc, 0.1)
        gripper_closed = False

    # Sleep while encoders are changing
    time.sleep(2)

    return positions[0], positions[1], positions[2], positions[3], positions[4], gripper_closed


# Load positions from CSV
def load_positions_from_csv(filename):
    positions = []
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            positions.append([int(value) for value in row])
    return positions


# Main execution function
def execute_saved_positions(rc, positions):
    gripper_closed = True
    for pos in positions:
        update_motor_positions(rc, pos, gripper_closed)
    print("All saved positions executed successfully")


if __name__ == "__main__":
    rc = initialize_roboclaw()
    positions = load_positions_from_csv("kpr_positions.csv")
    execute_saved_positions(rc, positions)
