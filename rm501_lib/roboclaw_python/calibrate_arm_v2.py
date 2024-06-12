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
rc = Roboclaw("/dev/ttyUSB0", 115200)
rc.Open()


def homeaxis_claw(address, speed, caltime, wrist_time=10):
    rc.SpeedM2(address, 2000)
    time.sleep(2)
    rc.SpeedM2(address, 0)

    if address != address3:
        return

    print("Calibrating wrist pitch")
    # pitch # pitch
    rc.SetEncM1(address3, 50000)

    rc.SpeedM1(address3, 2000)
    rc.SpeedM2(address3, 2000)
    time.sleep(1)
    rc.SpeedM1(address3, -2000)
    rc.SpeedM2(address3, -2000)

    for _ in range(caltime):
        if rc.ReadEncM1(address3)[1] > 5:
            time.sleep(3)
        else:
            break

    # correct to not touch the switch
    rc.SpeedM1(address, 2000)
    time.sleep(0.01)
    rc.SpeedM2(address, 2000)
    time.sleep(0.01)
    time.sleep(0.03)

    # set 0
    rc.SpeedM1(address3, 0)
    time.sleep(0.05)
    rc.SpeedM2(address3, 0)
    time.sleep(2)
    rc.SetEncM1(address3, 50000)
    time.sleep(0.1)
    rc.SetEncM2(address3, 50000)
    time.sleep(0.1)

    # roll
    print("Calibrating wrist roll")
    m1_speed = 2000

    if rc.ReadEncM2(address3)[1] <= 10:
        print("Wrist Roll Switch Already Hit, skipping...")

    else:
        # Find the switch...
        # Rotate 180 degrees in one direction
        rc.SpeedM1(address3, m1_speed)
        time.sleep(0.03)
        rc.SpeedM2(address3, -m1_speed)

        found = False
        for _ in range(wrist_time):
            if rc.ReadEncM2(address3)[1] <= 20:
                time.sleep(0.01)
                rc.SpeedM1(address3, 0)
                time.sleep(0.01)
                rc.SpeedM2(address3, 0)
                print("SLEEPING SWITCH ON!!!")
                time.sleep(1)
                found = True
                break
            time.sleep(1)

        if not found:
            # If the switch is not hit, rotate 180 degrees in the opposite direction
            m1_speed = -m1_speed
            rc.SpeedM1(address3, m1_speed)
            rc.SpeedM2(address3, -m1_speed)

            for _ in range(int(wrist_time*1.5)):
                if rc.ReadEncM2(address3)[1] <= 20:
                    time.sleep(0.01)
                    rc.SpeedM1(address3, 0)
                    time.sleep(0.01)
                    rc.SpeedM2(address3, 0)
                    print("SLEEPING SWITCH ON!!!")
                    found = True
                    break
                time.sleep(1)

        print(f"Wrist Roll Switch Found? :  {found}")
        time.sleep(0.5)

    # let it got a bit further
    rc.SpeedM1(address3, m1_speed)
    time.sleep(0.01)
    rc.SpeedM2(address3, -m1_speed)
    time.sleep(0.8)
    rc.SpeedM1(address3, 0)
    time.sleep(0.01)
    rc.SpeedM2(address3,
               0)  # both needs to be stopeed or only one gets switched off and the other one rotates it but moves


    # now correct pitch
    print("correcting pitch angle....")
    rc.SpeedM1(address3, 2000)
    time.sleep(0.03)
    rc.SpeedM2(address3, 2000)
    time.sleep(4) # time to reach center of range

    rc.SpeedM1(address3, 0)
    time.sleep(0.01)
    rc.SpeedM2(address3, 0)

    print("Set encoders to 0")
    setEncM1 = rc.SetEncM1(address3, 0)
    time.sleep(0.05)
    setEncM2 = rc.SetEncM2(address3, 0)
    time.sleep(0.05)

    return




def homeaxis(address, motorN, speed, caltime):
        print(f"Calibrating motor {motorN} on address {address} with speed {speed} and caltime {caltime}")
        # make homeaxis

        if motorN == 1:
            rc.SetEncM1(address, 50000)
            rc.SpeedM1(address, 80)
            time.sleep(0.5)
            rc.SpeedM1(address, -speed)
            for _ in range(caltime):
                if rc.ReadEncM1(address)[1] > 10:
                    time.sleep(3)

            rc.SpeedM1(address, speed)
            time.sleep(0.1)
            rc.SpeedM1(address, -80)
            time.sleep(3)
            rc.SpeedM1(address, 0)
        else:
            rc.SetEncM2(address, 50000)
            rc.SpeedM2(address, 80)
            time.sleep(0.5)
            rc.SpeedM2(address, -speed)
            for _ in range(caltime):
                if rc.ReadEncM2(address)[1] > 10:
                    time.sleep(3)

            rc.SpeedM2(address, speed)
            time.sleep(0.1)
            rc.SpeedM2(address, -80)
            time.sleep(3)
            rc.SpeedM2(address, 0)

            setEncM1 = rc.SetEncM1(address, 0)
            setEncM2 = rc.SetEncM2(address, 0)

        print(f"Homaxis {motorN} on address {address} complete")

def calibrate(rc = rc):

    enc1 = rc.ReadEncM2(address1)  # base
    enc2 = rc.ReadEncM1(address2)  # shoulder
    enc3 = rc.ReadEncM2(address2)  # elbow
    enc4 = rc.ReadEncM1(address3)  # wrist pitch
    enc5 = rc.ReadEncM2(address3)  # wrist roll

    def displayspeed():

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

    version1 = rc.ReadVersion(address1)
    version2 = rc.ReadVersion(address2)
    version3 = rc.ReadVersion(address3)

    if not version1[0]:
        print("GETVERSION Failed")
    else:
        print(repr(version1[1]))
        print(repr(version2[1]))
        print(repr(version3[1]))

    homeaxis(address1, 2, 2000, 10)
    homeaxis(address2, 1, 2000, 5)
    homeaxis(address2, 2, 2000, 5)
    homeaxis_claw(address3, 2000, 400)

    rc.SpeedAccelDeccelPositionM2(address1, 2000, 10000, 10000, 24000, 100)
    time.sleep(0.1)
    rc.SpeedAccelDeccelPositionM1(address2, 2000, 10000, 10000, 2500, 100)
    time.sleep(0.1)
    rc.SpeedAccelDeccelPositionM2(address2, 2000, 10000, 10000, 18000, 100)


    # 1-3 motors need to time to reach the position
    time.sleep(5)
    print("FINAL POSITION")


if __name__ == "__main__":
    # calibrate()

    homeaxis_claw(address3, 2000, 400)


