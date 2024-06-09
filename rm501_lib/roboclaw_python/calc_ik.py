"""
in this script qr (taken from puma config 'working') IS where I want to go
I start from joint angle 0,0,0,0,0,0

TODO
 [x] Fix teach method along limits for properly visualizing angles -> transform to positions and check movement (...)

 [ ] tool transform rm501.tool e.g transl(0, 0, 2)... fkine should change..

 - Interpolation -
 [ ] joint angle trajectory jtraj PLOT -> Transformed Plot to Positions -> + DF to test individual column ranges..
 [ ] cartesian interpolation same process [to make straight x and y ]

# q3 inverse effect starts at 14000 but being 0  needs to - later


# NOTES
q0 => OK
q1 => initial position 2500 means -90 degrees. ranges up to 21000 which is 30 degrees. Looks Alright!
q2 => initial position as 14000 means 0 degrees. Looks Alright!
_____
q3 => fucking it up
q4 => fucking it up

"""
import roboticstoolbox as rtb
import pandas as pd
from spatialmath import *
import math
import numpy as np

rm501 = rtb.DHRobot(
    [
        rtb.RevoluteDH(d=250, a=0, alpha=-math.pi / 2, qlim=np.radians([0, 300])),
        rtb.RevoluteDH(flip=True, a=220, alpha=0, d=0, qlim=np.radians([-100, 30])),
        rtb.RevoluteDH(a=160, alpha=0, d=0, qlim=np.radians([0, 90])),
        # change a 215 for 0 just as a replacement for q5 inabaility to render
        rtb.RevoluteDH(a=0, alpha=-math.pi / 2, d=0, qlim=np.radians([-90, 0])),  # -90 to 90
        # rtb.RevoluteDH(a=0, alpha=0, d=215, qlim=np.radians([-180, 180])),

    ], name="RM501")

rm501.q = [math.radians(150), -math.pi / 2, 0, math.radians(-90)] # math.radians(90)]
q = rm501.q

# visualize robot and joints , set limits otherwise -pi to pi which is wrong
rm501.teach(q)

T = SE3(-250, 300, 100)  # * SE3.RPY([0.0, 0.0, 0.0], order='xyz')

# qr = [math.radians(150), -math.pi/2, 0, -math.radians(90), 0]
# T = rm501.fkine(qr)
print("End effector position: ", T)

# INVERSE KINEMATICS - SECRET TRICK NICE
sol = rm501.ikine_LM(T, q0=[q for i in range(1000)], ilimit=1000, slimit=1000, tol=1e-6, joint_limits=True)
print("Joint configuration for end effector position: ", sol.q)

initial_q = q
final_q = sol.q
qt = rtb.jtraj(initial_q, final_q, 5)

# _____________________________________
qt_degrees = np.degrees(qt.q)
angle_per_pos = [48000 / 300, 21000 / 130, 14500 / 90, -9500 / 90] # 9500 / 180]


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
                9500 - int(angles[i] * angle_per_pos[i])
            )
        else:
            pos.append(
                int(angles[i] * angle_per_pos[i])
            )
    return pos


converted_positions = list()
for joint_angles in qt_degrees:
    converted_positions.append(
        convert_angles_to_pos(joint_angles)
    )

qs_df = pd.DataFrame(np.degrees(qt.q), columns=['q0', 'q1', 'q2', 'q3']) # 'q4'])
pos_df = pd.DataFrame(converted_positions, columns=['pos_q0', 'pos_q1', 'pos_q2', 'pos_q3']) # 'pos_q4'])

print(qs_df)

# write pos_df in csv
pos_df.to_csv(
    '/Users/diegopenilla/Desktop/genArt/robotics-toolbox-python/rm501_robot/robot_Lib/roboclaw_python_library/roboclaw_python/positions.csv')

# corrected plot
cq = list()
for angles in qt.q:
    cq.append(
        [angles[0], angles[1], angles[2], angles[3]] # angles[4]]
    )

rm501.plot(np.array(cq), backend="pyplot", dt=0.3)

