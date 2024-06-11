"""
Mechanical Origin Script
- Issue: requires switch 5 for the wrist roll to not be pressed when switch 4 is pressed

UNTANGLE CABLE

    rc.SpeedM1(address3, -2000)
    rc.SpeedM2(address3, 2000)
    time.sleep(30)
    rc.SpeedM1(address3, 0)
    rc.SpeedM2(address3, 0)
"""
import time
from roboclaw_3 import Roboclaw

address1 = 0x80
address2 = 0x81
address3 = 0x82
# Set up the connection with the correct port and baud rate (Update port as necessary)
rc = Roboclaw("/dev/tty.usbserial-DN41WBZS", 115200)
rc.Open()

if __name__ == "__main__":

    # set encoders to 0
    rc.SetEncM1(address3, 0)
    rc.SetEncM2(address3, 0)

    # calibrate()
    read_encoder_3 = rc.ReadEncM1(address3)[1]
    read_encoder_3_2 = rc.ReadEncM2(address3)[1]

    print("WRIST ENCODERS")
    print(read_encoder_3)
    print(read_encoder_3_2)

    rc.SpeedAccelDeccelPositionM1(address3, 2000, 10000, 10000, 1000, 100)
    rc.SpeedAccelDeccelPositionM2(address3, 2000, 10000, 10000, 1000, 100)

    time.sleep(5)
    print("AFTER WRIST ENCODERS")
    read_encoder_3 = rc.ReadEncM1(address3)[1]
    read_encoder_3_2 = rc.ReadEncM2(address3)[1]
    print(read_encoder_3)
    print(read_encoder_3_2)

    rc.SpeedAccelDeccelPositionM1(address3, 2000, 10000, 10000, 0, 100)
    rc.SpeedAccelDeccelPositionM2(address3, 2000, 10000, 10000, 2000, 100)
    print("AFTER WRIST TURN ENCODERS")
    time.sleep(5)
    read_encoder_3 = rc.ReadEncM1(address3)[1]
    read_encoder_3_2 = rc.ReadEncM2(address3)[1]
    print(read_encoder_3)
    print(read_encoder_3_2)

    rc.SpeedAccelDeccelPositionM1(address3, 2000, 10000, 10000, -2000, 100)
    rc.SpeedAccelDeccelPositionM2(address3, 2000, 10000, 10000, 4000, 100)
    print("AFTER WRIST TURN 2 ENCODERS")
    time.sleep(5)
    read_encoder_3 = rc.ReadEncM1(address3)[1]
    read_encoder_3_2 = rc.ReadEncM2(address3)[1]
    print(read_encoder_3)
    print(read_encoder_3_2)


    rc.SpeedAccelDeccelPositionM1(address3, 2000, 10000, 10000, 3000, 100)
    rc.SpeedAccelDeccelPositionM2(address3, 2000, 10000, 10000, 9000, 100)
    print("AFTER WRIST TURN 2 ENCODERS")
    time.sleep(5)
    read_encoder_3 = rc.ReadEncM1(address3)[1]
    read_encoder_3_2 = rc.ReadEncM2(address3)[1]
    print(read_encoder_3)
    print(read_encoder_3_2)


    print("ORIGIN SHOULDC COME")
    rc.SpeedAccelDeccelPositionM1(address3, 2000, 10000, 10000, 0, 100)
    rc.SpeedAccelDeccelPositionM2(address3, 2000, 10000, 10000, 0, 100)

    time.sleep(5)
    print("AFTER WRIST FINAL ENCODERS")
    read_encoder_3 = rc.ReadEncM1(address3)[1]
    read_encoder_3_2 = rc.ReadEncM2(address3)[1]
    print(read_encoder_3)
    print(read_encoder_3_2)