import time
import csv
from roboclaw_3 import Roboclaw
from app_utils import load_positions_from_csv, save_positions_to_csv

# Constants
ADDRESS1 = 0x80
ADDRESS2 = 0x81
ADDRESS3 = 0x82


class RobotArm:
    def __init__(self, port, baud_rate):
        self.rc = Roboclaw(port, baud_rate)
        self.gripper_closed = True

    # Update motor positions safely
    def safe_update_motor_position(self, motor_id, position):
        try:
            if motor_id == 1:
                self.rc.SpeedAccelDeccelPositionM2(ADDRESS1, 10000, 10000, 10000, position, 100)
            elif motor_id == 2:
                self.rc.SpeedAccelDeccelPositionM1(ADDRESS2, 10000, 10000, 10000, position, 100)
            elif motor_id == 3:
                self.rc.SpeedAccelDeccelPositionM2(ADDRESS2, 10000, 10000, 10000, position, 100)
        except Exception as e:
            print(f"Error updating motor {motor_id} position: {e}")

    # Update wrist positions
    def update_wrist_positions(self, pos4, pos5):
        self.rc.SpeedAccelDeccelPositionM1(ADDRESS3, 2000, 10000, 10000, pos4, 100)
        time.sleep(0.05)
        self.rc.SpeedAccelDeccelPositionM2(ADDRESS3, 2000, 10000, 10000, pos5, 100)

    def gripper_close(self, step=0.1):
        self.rc.SpeedAccelM1(ADDRESS1, 3000, 3000)
        time.sleep(step)
        self.rc.SpeedAccelM1(ADDRESS1, 3000, 0)
        self.gripper_closed = True

    def gripper_open(self, step=0.1):
        self.rc.SpeedAccelM1(ADDRESS1, 3000, -3000)
        time.sleep(step)
        self.rc.SpeedAccelM1(ADDRESS1, 3000, 0)
        self.gripper_closed = False

    # Update all motor positions
    def update_motor_positions(self, positions):
        self.safe_update_motor_position(1, positions[0])
        self.safe_update_motor_position(2, positions[1])
        self.safe_update_motor_position(3, positions[2])
        self.update_wrist_positions(positions[3], positions[4])

        if positions[5] and not self.gripper_closed:
            self.gripper_close(0.1)
        elif not positions[5] and self.gripper_closed:
            self.gripper_open(0.1)

        # Sleep while encoders are changing
        time.sleep(3)

        return positions[0], positions[1], positions[2], positions[3], positions[4], self.gripper_closed

    # Load positions from CSV
    def load_positions(self, file_path):
        return load_positions_from_csv(file_path)

    # Execute saved positions
    def execute_saved_positions(self, positions):
        for pos in positions[:-1]:
            self.update_motor_positions(pos)

        self.update_motor_positions(positions[-1])
        time.sleep(3)
        print("All saved positions executed successfully")

    # Main execution function
    def initialize_and_execute(self, positions_file):
        # Send initial positions
        self.rc.SpeedAccelDeccelPositionM2(ADDRESS1, 2000, 10000, 10000, 24000, 100)
        time.sleep(0.05)
        self.rc.SpeedAccelDeccelPositionM1(ADDRESS2, 2000, 10000, 10000, 2500, 100)
        time.sleep(0.05)
        self.rc.SpeedAccelDeccelPositionM2(ADDRESS2, 2000, 10000, 10000, 14500, 100)
        time.sleep(0.05)

        # Set encoders 3 to 0
        self.rc.SetEncM1(ADDRESS3, 0)
        self.rc.SetEncM2(ADDRESS3, 0)

        # Close grippers
        self.rc.SpeedAccelM1(ADDRESS1, 3000, 3000)
        time.sleep(0.5)
        self.rc.SpeedAccelM1(ADDRESS1, 3000, 0)

        positions = self.load_positions(positions_file)
        self.execute_saved_positions(positions)


def main():
    robot_arm = RobotArm("/dev/RM501", 115200)
    robot_arm.initialize_and_execute("kpr_positions.csv")


if __name__ == "__main__":
    main()
