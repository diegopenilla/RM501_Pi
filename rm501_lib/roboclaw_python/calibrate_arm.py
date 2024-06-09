import time
from roboclaw_3 import Roboclaw

# Set up the connection with the correct port and baud rate (Update port as necessary)
rc = Roboclaw("/dev/tty.usbserial-DN41WBZS", 115200)
rc.Open()

address1 = 0x80
address2 = 0x81
address3 = 0x82

enc1 = rc.ReadEncM2(address1) # base
enc2 = rc.ReadEncM1(address2) # shoulder
enc3 = rc.ReadEncM2(address2) # elbow
enc4 = rc.ReadEncM1(address3) # wrist pitch
enc5 = rc.ReadEncM2(address3) # wrist roll

def displayspeed():
    # enc0 = rc.ReadEncM1(address1)


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

def homeaxis(address, motorN, speed, caltime):
    print(f"Calibrating motor {motorN} on address {address} with speed {speed} and caltime {caltime}")
    # make homeaxis 
    if address == address3:
        
        if motorN == 1:
            rc.SetEncM1(address3, 50000)
            rc.SpeedM1(address3, 80)
            time.sleep(0.5)
            rc.SpeedM1(address3, -speed)
            
            for _ in range(caltime):
                if rc.ReadEncM1(address3)[1] > 10:
                    time.sleep(3)
            
            rc.SpeedM1(address, speed)
            time.sleep(0.1)
            rc.SpeedM1(address, -80)
            time.sleep(1)
            rc.SpeedM1(address, 0)
            
        else:
            rc.SetEncM2(address3, 5000)
            rc.SpeedM2(address3, 100)
            time.sleep(0.5)
            rc.SpeedM2(address3, -speed)
            for _ in range(caltime):
                if rc.ReadEncM2(address3)[1] > 10:
                    time.sleep(3)
            
            rc.SpeedM2(address, speed)
            time.sleep(0.1)
            rc.SpeedM2(address, -80)
            time.sleep(1)
            rc.SpeedM2(address, 0)
            
    # make homeaxis
    else:     
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
    
    print(f"Homaxis {motorN} on address {address} complete")
    
    

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
homeaxis(address2, 1, 2000, 10)
homeaxis(address2, 2, 2000, 10)
homeaxis(address3, 1, 2000, 10)
homeaxis(address3, 2, 2000, 10)


setEncM1 = rc.SetEncM1(address3, 0)
setEncM2 = rc.SetEncM2(address3, 0)

rc.SpeedAccelDeccelPositionM2(address1, 2000, 10000, 10000, 24000, 100)
time.sleep(0.5)
rc.SpeedAccelDeccelPositionM1(address2, 2000, 10000, 10000, 2500, 100)
time.sleep(0.5)
rc.SpeedAccelDeccelPositionM2(address2, 2000, 10000, 10000, 14500, 100)
time.sleep(0.5)

rc.SpeedAccelDeccelPositionM1(address3, 2000, 10000, 10000, 9200, 100)
time.sleep(0.5)
rc.SpeedAccelDeccelPositionM2(address3, 2000, 10000, 10000, 9200, 100)


while True:
    for i in range(20):
        displayspeed()
        time.sleep(0.01)
