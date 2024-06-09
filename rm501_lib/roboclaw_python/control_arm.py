import time
from roboclaw_3 import Roboclaw
import pandas as pd

# Set up the connection with the correct port and baud rate (Update port as necessary)
rc = Roboclaw("/dev/tty.usbserial-DN41WBZS", 115200)
positions = pd.read_csv("positions.csv")
del positions['Unnamed: 0']

pos_angles = [list(int(i) for i in angle_set) for angle_set in positions.values]

def displayspeed():
    # enc0 = rc.ReadEncM1(address1)
    enc1 = rc.ReadEncM2(address1) # base
    enc2 = rc.ReadEncM1(address2) # shoulder
    enc3 = rc.ReadEncM2(address2) # elbow
    enc4 = rc.ReadEncM1(address3) # wrist pitch
    enc5 = rc.ReadEncM2(address3) # wrist roll

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

rc.Open()
address1 = 0x80
address2 = 0x81
address3 = 0x82


q4_pos_current = 9500 # must be within 9500 and 0
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


started = False
for angle_set in pos_angles:

    q1, q2, q3, q4 = angle_set # q5
    print(f"Setting joint angles to: {q1, q2, q3, q4}") #q5
    
    rc.SpeedAccelDeccelPositionM2(address1, 2000, 10000, 10000, q1, 100)
    time.sleep(0.5)
    rc.SpeedAccelDeccelPositionM1(address2, 2000, 10000, 10000, q2, 100)
    time.sleep(0.5)
    rc.SpeedAccelDeccelPositionM2(address2, 2000, 10000, 10000, q3, 100)
    
    # q4 up and down
    move_q4(q4)

    time.sleep(1)

    # time.sleep(4)
    # rc.SpeedAccelDeccelPositionM1(address3, 2000, 8000, 8000, q5, 100)
    # rc.SpeedAccelDeccelPositionM2(address3, 2000, 8000, 8000, -int(q5), 100)
    #

    if not started:
        time.sleep(5)
        started = True
        print('Reached start position')
        
    time.sleep(1)


