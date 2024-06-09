import roboticstoolbox as rtb
from spatialmath import *
import math
import numpy as np

import time
from roboclaw_3 import Roboclaw
import pandas as pd


def transform_to_pos_df(T, q, steps: int = 5) -> pd.DataFrame:
    # INVERSE KINEMATICS - SECRET TRICK NICE
    sol = rm501.ikine_LM(T, q0=[q for i in range(1000)], ilimit=1000, slimit=1000, tol=1e-6, joint_limits=True)
    print("Joint configuration for end effector position: ", sol.q)

    initial_q = q
    final_q = sol.q
    qt = rtb.jtraj(initial_q, final_q, steps)

    # _____________________________________
    angle_per_pos = [48000 / 300, 21000 / 130, 14500 / 90, -9500 / 90]  # 9500 / 180]

    def angle2_to_position(angle):
        return 154.17 * angle + 16375

    def convert_angles_to_pos(angles):
        pos = []
        for i in range(len(angles)):

            if i == 1:
                pos.append(angle2_to_position(angles[i]))

            elif i == 2:
                pos.append(
                    int(abs((90 - angles[i]) * angle_per_pos[i]))
                )

            elif i == 3:
                pos.append(
                    int(((angles[i]) * angle_per_pos[i]))
                )
            elif i == 4:
                pos.append(
                    10000 - int(angles[i] * angle_per_pos[i])
                )
            else:
                pos.append(
                    int(angles[i] * angle_per_pos[i])
                )
        return pos

    qt_degrees = np.degrees(qt.q)
    converted_positions = list()
    for joint_angles in qt_degrees:
        converted_positions.append(
            convert_angles_to_pos(joint_angles)
        )

    qs_df = pd.DataFrame(qt_degrees, columns=['q0', 'q1', 'q2', 'q3'])  # 'q4'])
    pos_df = pd.DataFrame(converted_positions, columns=['pos_q0', 'pos_q1', 'pos_q2', 'pos_q3'])  # 'pos_q4'])

    print("Joint angles")
    print(qs_df)
    print("Position Angles")
    print(pos_df)
    return pos_df, final_q


address1 = 0x80
address2 = 0x81
address3 = 0x82


def displayspeed():
    # enc0 = rc.ReadEncM1(address1)
    enc1 = rc.ReadEncM2(address1)  # base
    enc2 = rc.ReadEncM1(address2)  # shoulder
    enc3 = rc.ReadEncM2(address2)  # elbow
    enc4 = rc.ReadEncM1(address3)  # wrist pitch
    enc5 = rc.ReadEncM2(address3)  # wrist roll

    speed1 = rc.ReadSpeedM1(address1)
    speed2 = rc.ReadSpeedM2(address1)

    print("\nEncoder1:", end=" ")
    if enc1[0] == 1:
        print(enc1[1], format(enc1[2], '02x'), end=" ")
    else:
        print("failed", end=" ")
    print("Encoder2:", end=" ")
    if enc2[0] == 1:
        print(enc2[1], format(enc2[2], '02x'), end=" ")
    else:
        print("failed ", end=" ")
    print("Encoder3:", end=" ")
    if enc3[0] == 1:
        print(enc3[1], format(enc3[2], '02x'), end=" ")
    else:
        print("failed", end=" ")
    print("Encoder4:", end=" ")
    if enc4[0] == 1:
        print(enc4[1], format(enc4[2], '02x'), end=" ")
    else:
        print("failed ", end=" ")
    print("Encoder5:", end=" ")
    if enc5[0] == 1:
        print(enc5[1], format(enc5[2], '02x'))
    else:
        print("failed")


def move_q4(q4_pos: int):
    """
    Assume

    TODO: keep state of q4 position fixed even if wrist is turned... [ ]
    """
    global q4_pos_current

    enc4 = rc.ReadEncM1(address3)  # wrist pitch
    time.sleep(0.05)
    enc5 = rc.ReadEncM2(address3)  # wrist roll
    time.sleep(0.05)

    move_by_pos = q4_pos_current - q4_pos
    if move_by_pos < 0:
        move_by_pos = 0

    if q4_pos_current > q4_pos:
        enc4_move_pos = enc4[1] - move_by_pos
        enc5_move_pos = enc5[1] - move_by_pos

    else:
        enc4_move_pos = enc4[1] + move_by_pos
        enc5_move_pos = enc5[1] + move_by_pos

    rc.SpeedAccelDeccelPositionM1(address3, 2000, 10000, 10000, enc4_move_pos, 100)
    time.sleep(0.05)
    rc.SpeedAccelDeccelPositionM2(address3, 2000, 10000, 10000, enc5_move_pos, 100)
    time.sleep(0.05)

    # update current position to keep state of up and down
    q4_pos_current = q4_pos


def move_robot(pos_angles: list[list[int]]):
    for angle_set in pos_angles:
        q1, q2, q3, q4 = angle_set  # q5
        print(f"Setting joint angles to: {q1, q2, q3, q4}")  # q5

        rc.SpeedAccelDeccelPositionM2(address1, 2000, 10000, 10000, q1, 100)
        time.sleep(0.05)
        rc.SpeedAccelDeccelPositionM1(address2, 2000, 10000, 10000, q2, 100)
        time.sleep(0.05)
        rc.SpeedAccelDeccelPositionM2(address2, 2000, 10000, 10000, q3, 100)
        time.sleep(0.05)

        # q4 up and down
        move_q4(q4)

        time.sleep(0.05)


if __name__ == "__main__":

    # CONTROL  ARM
    rc = Roboclaw("/dev/tty.usbserial-DN41WBZS", 115200)
    rc.Open()

    rm501 = rtb.DHRobot(
        [
            rtb.RevoluteDH(d=250, a=0, alpha=-math.pi / 2, qlim=np.radians([0, 300])),
            rtb.RevoluteDH(flip=True, a=220, alpha=0, d=0, qlim=np.radians([-100, 30])),
            rtb.RevoluteDH(a=160, alpha=0, d=0, qlim=np.radians([0, 90])),
            # change a 215 for 0 just as a replacement for q5 inabaility to render
            rtb.RevoluteDH(flip=True, a=0, alpha=-math.pi / 2, d=0, qlim=np.radians([-90, 0])),  # -90 to 90
            # rtb.RevoluteDH(a=0, alpha=0, d=215, qlim=np.radians([-180, 180])),

        ], name="RM501")

    # setting default position
    rc.SpeedAccelDeccelPositionM2(address1, 2000, 10000, 10000, 24000, 100)
    time.sleep(0.05)
    rc.SpeedAccelDeccelPositionM1(address2, 2000, 10000, 10000, 2500, 100)
    time.sleep(0.05)
    rc.SpeedAccelDeccelPositionM2(address2, 2000, 10000, 10000, 14500, 100)
    time.sleep(0.05)
    # IK
    time.sleep(5)
    print("READY...")

    rm501.q = [math.radians(150), -math.pi / 2, 0, math.radians(-90)]  # math.radians(90)]

    # UP AND DOWN GLOBAL VARIABLE
    q4_pos_current = 9500  # must be within 9500 and 0

    transformations_list = [
        SE3(-300, 200, 600),
        SE3(300, 200, 600),
        SE3(300, 800, 600),

    ]

    for T in transformations_list:
        print(f"Transforming to position: {T}")
        q = rm501.q
        pos_df, final_q = transform_to_pos_df(T, q, steps=20)

        # MOVE ROBOT
        pos_angles = [list(int(i) for i in angle_set) for angle_set in pos_df.values]

        move_robot(pos_angles)
        rm501.q = final_q
