"""

About
+ Up And Down
+ Wrist Rotation
Needs to be kept in state -> set by speed not by position.\
IF kept in state, positions for them could be saved...

- Can be defined the speed and time to achieve 90 degrees up and down...


"""

import streamlit as st
import pandas as pd

from calibrate_arm_v2 import calibrate, homeaxis_claw
from roboclaw_3 import Roboclaw
import time

from app_utils import load_positions_from_csv, save_positions_to_csv

# INIT STATE
address1 = 0x80
address2 = 0x81
address3 = 0x82

if "gripper_closed" not in st.session_state:
    st.session_state["gripper_closed"] = True


def gripper_close(step=0.2):
    rc.SpeedAccelM1(address1, 3000, 3000)
    time.sleep(step)
    rc.SpeedAccelM1(address1, 3000, 0)
    st.session_state["gripper_closed"] = 1


def gripper_open(step=0.2):
    rc.SpeedAccelM1(address1, 3000, -3000)
    time.sleep(step)
    rc.SpeedAccelM1(address1, 3000, 0)
    st.session_state["gripper_closed"] = 0


if 'rc' not in st.session_state:
    rc = Roboclaw("/dev/RM501", 115200)
    st.session_state['rc'] = rc
    # CONTROL  ARM
    rc.Open()
    # send initial
    rc.SpeedAccelDeccelPositionM2(address1, 2000, 10000, 10000, 24000, 100)
    time.sleep(0.05)
    rc.SpeedAccelDeccelPositionM1(address2, 2000, 10000, 10000, 2500, 100)
    time.sleep(0.05)
    rc.SpeedAccelDeccelPositionM2(address2, 2000, 10000, 10000, 14500, 100)
    time.sleep(0.05)

    # set encoders 3 to 0
    rc.SetEncM1(address3, 0)
    rc.SetEncM2(address3, 0)

    # close gripper
    gripper_close(0.5)

if 'saved_positions' not in st.session_state:
    try:
        st.session_state['saved_positions'] = load_positions_from_csv("kpr_positions.csv")
    except Exception as e:
        st.error(f"Error loading positions: {e}, initialized as empty list")
        st.session_state['saved_positions'] = []

input_file_name = st.text_input("Input file name .csv", "kpr_positions")
if st.button("Load Positions"):
    try:
        st.session_state['saved_positions'] = load_positions_from_csv(f"{input_file_name}.csv")
    except Exception as e:
        st.error(f"Error loading positions: {e}")

if 'motor1_pos_current' not in st.session_state:
    st.session_state['motor1_pos_current'] = 0
    st.session_state['motor2_pos_current'] = 0
    st.session_state['motor3_pos_current'] = 0

if 'motor4_pos_current' not in st.session_state:
    st.session_state['motor4_pos_current'] = 0
    st.session_state['motor5_pos_current'] = 0

rc = st.session_state['rc']

if 'current_pos' not in st.session_state:
    enc1 = rc.ReadEncM2(address1)[1]  # base
    enc2 = rc.ReadEncM1(address2)[1]  # shoulder
    enc3 = rc.ReadEncM2(address2)[1]  # elbow

    enc4 = rc.ReadEncM1(address3)[1]  # wrist pitch
    enc5 = rc.ReadEncM2(address3)[1]  # wrist roll

    st.session_state['current_pos'] = True

    if 'motor1_slider_key' not in st.session_state:
        st.session_state['motor1_slider_key'] = enc1

    if 'motor2_slider_key' not in st.session_state:
        st.session_state['motor2_slider_key'] = enc2

    if 'motor3_slider_key' not in st.session_state:
        st.session_state['motor3_slider_key'] = enc3


# UTILS
def move_up_q4():
    current_4 = rc.ReadEncM1(address3)[1]
    current_5 = rc.ReadEncM2(address3)[1]

    rc.SpeedAccelDeccelPositionM1(address3, 3000, 10000, 10000, current_4 + 1000, 100)
    time.sleep(0.01)
    rc.SpeedAccelDeccelPositionM2(address3, 3000, 10000, 10000, current_5 + 1000, 100)

    time.sleep(2)

    # read encoder
    st.session_state['motor4_pos_current'] = rc.ReadEncM1(address3)[1]
    st.session_state['motor5_pos_current'] = rc.ReadEncM2(address3)[1]


def move_down_q4():
    current_4 = rc.ReadEncM1(address3)[1]
    current_5 = rc.ReadEncM2(address3)[1]

    rc.SpeedAccelDeccelPositionM1(address3, 3000, 10000, 10000, current_4 - 1000, 100)
    time.sleep(0.01)
    rc.SpeedAccelDeccelPositionM2(address3, 3000, 10000, 10000, current_5 - 1000, 100)

    time.sleep(2)

    # read encoder
    st.session_state['motor4_pos_current'] = rc.ReadEncM1(address3)[1]
    st.session_state['motor5_pos_current'] = rc.ReadEncM2(address3)[1]


def turn_left_q5():
    current4 = rc.ReadEncM1(address3)[1]
    current5 = rc.ReadEncM2(address3)[1]

    rc.SpeedAccelDeccelPositionM1(address3, 2000, 10000, 10000, current4 + 1000, 100)
    time.sleep(0.01)
    rc.SpeedAccelDeccelPositionM2(address3, 2000, 10000, 10000, current5 - 1000, 100)

    time.sleep(1)

    # read encoder
    st.session_state['motor4_pos_current'] = rc.ReadEncM1(address3)[1]
    st.session_state['motor5_pos_current'] = rc.ReadEncM2(address3)[1]


def turn_right_q5():
    current4 = rc.ReadEncM1(address3)[1]
    current5 = rc.ReadEncM2(address3)[1]

    rc.SpeedAccelDeccelPositionM1(address3, 2000, 10000, 10000, current4 - 1000, 100)
    time.sleep(0.01)
    rc.SpeedAccelDeccelPositionM2(address3, 2000, 10000, 10000, current5 + 1000, 100)

    time.sleep(2)

    # read encoder
    st.session_state['motor4_pos_current'] = rc.ReadEncM1(address3)[1]
    st.session_state['motor5_pos_current'] = rc.ReadEncM2(address3)[1]


def safe_update_motor_position(motor_id, position):
    try:
        if motor_id == 1:
            rc.SpeedAccelDeccelPositionM2(address1, 10000, 10000, 10000, position, 100)
        elif motor_id == 2:
            rc.SpeedAccelDeccelPositionM1(address2, 10000, 10000, 10000, position, 100)
        elif motor_id == 3:
            rc.SpeedAccelDeccelPositionM2(address2, 10000, 10000, 10000, position, 100)
        return position
    except Exception as e:
        st.error(f"Error updating motor {motor_id} position: {e}")
        return position  # return current position in case of an error


# Handlers for motor position updates
def update_motor_position1():
    if 'motor1_slider_key' in st.session_state:
        st.session_state['motor1_pos_current'] = safe_update_motor_position(1, st.session_state['motor1_slider_key'],
                                                                            )


def update_motor_position2():
    if 'motor2_slider_key' in st.session_state:
        st.session_state['motor2_pos_current'] = safe_update_motor_position(2, st.session_state['motor2_slider_key'],
                                                                            )


def update_motor_position3():
    if 'motor3_slider_key' in st.session_state:
        st.session_state['motor3_pos_current'] = safe_update_motor_position(3, st.session_state['motor3_slider_key'],
                                                                            )


def update_wrist_positions(pos4, pos5):
    rc.SpeedAccelDeccelPositionM1(address3, 2000, 10000, 10000, pos4, 100)
    time.sleep(0.05)
    rc.SpeedAccelDeccelPositionM2(address3, 2000, 10000, 10000, pos5, 100)


def axis2_position_to_angle(position):
    return -(position - 16375) / 154.17


# Define a function to convert the motor positions to angles for a more general approach
def position_to_angle(position, max_angle, max_position):
    return position * max_angle / max_position


def update_motor_positions(positions):
    safe_update_motor_position(1, positions[0])
    safe_update_motor_position(2, positions[1])
    safe_update_motor_position(3, positions[2])
    update_wrist_positions(positions[3], positions[4])

    if positions[5] and not st.session_state['gripper_closed']:
        gripper_close(0.1)

    elif not positions[5] and st.session_state['gripper_closed']:
        gripper_open(0.1)

    # sleep while encoders are changing, all addresses
    time.sleep(2)

    st.session_state['motor1_pos_current'] = positions[0]
    st.session_state['motor2_pos_current'] = positions[1]
    st.session_state['motor3_pos_current'] = positions[2]
    st.session_state['motor4_pos_current'] = positions[3]
    st.session_state['motor5_pos_current'] = positions[4]

    st.session_state['gripper_closed'] = positions[5]


# __________Streamlit app__________
# Assuming 'saved_positions' is already initialized and filled with lists of angle data
if 'saved_positions' not in st.session_state:
    st.session_state['saved_positions'] = []

st.sidebar.title('RM501 Move Master II')

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Calibrate"):
        calibrate()

    if st.button("Calibrate Claw"):
        homeaxis_claw(address3, 2000, 400)

with col2:
    if st.button("Set Claw Zero"):
        rc.SetEncM1(address3, 0)
        rc.SetEncM2(address3, 0)

    if st.button("Return Claw Zero"):
        # move positions to 0 for address 3
        rc.SpeedAccelDeccelPositionM1(address3, 2000, 10000, 10000, 0, 100)
        time.sleep(0.05)
        rc.SpeedAccelDeccelPositionM2(address3, 2000, 10000, 10000, 0, 100)

save_position_name = st.sidebar.text_input("Position Name", "")
if st.sidebar.button("Save Position"):
    pos = [st.session_state['motor1_slider_key'], st.session_state['motor2_slider_key'],
           st.session_state['motor3_slider_key'], st.session_state['motor4_pos_current'],
           st.session_state['motor5_pos_current'], st.session_state['gripper_closed'],
           save_position_name]

    st.session_state['motor1_pos_current'] = st.session_state['motor1_slider_key']
    st.session_state['motor2_pos_current'] = st.session_state['motor2_slider_key']
    st.session_state['motor3_pos_current'] = st.session_state['motor3_slider_key']

    st.session_state['saved_positions'].append(pos)

st.sidebar.subheader('Differential Drive')
with st.sidebar.container():
    # Using columns to organize buttons
    col1, col2 = st.columns(2, gap="small")

    with col1:

        if st.button("⬆️ Up"):
            move_up_q4()

        if st.button("⬇️ Down"):
            move_down_q4()

    with col2:
        if st.button("️↪️ Right"):
            turn_right_q5()

        if st.button("↩️ Left"):
            turn_left_q5()

st.markdown("### `Current Joint Angles`")
angle1 = st.session_state['motor1_pos_current']
angle2 = st.session_state['motor2_pos_current']
angle3 = st.session_state['motor3_pos_current']
angle4 = st.session_state[
    'motor4_pos_current']  # Assuming 'motor_4_pos_current' exists in session_state and initialized properly
angle5 = st.session_state['motor5_pos_current']  # Assuming 'motor_5_pos_current' exists and is initialized

# Display the saved positions with a corresponding button
for idx, positions in enumerate(st.session_state['saved_positions']):
    col1, col2 = st.columns([2, 1])  # Adjust the ratio if needed
    with col1:
        st.text(positions)  # Display angles as a comma-separated list
    with col2:
        if st.button("Select", key=f"select{idx}"):  # Unique key for each button
            update_motor_positions(positions)

m1 = st.session_state['motor1_pos_current']
m2 = st.session_state['motor2_pos_current']
m3 = st.session_state['motor3_pos_current']
m4 = st.session_state['motor4_pos_current']
m5 = st.session_state['motor5_pos_current']

st.sidebar.subheader("Motor Positions")
# Set up number inputs
s = st.sidebar.number_input('Motor 1', -200, 48000, value=m1, step=200, key='motor1_slider_key',
                            on_change=update_motor_position1)
a = st.sidebar.number_input('Motor 2', -200, 22000, value=m2, step=200, key='motor2_slider_key',
                            on_change=update_motor_position2)
t = st.sidebar.number_input('Motor 3', -200, 15000, value=m3, step=200, key='motor3_slider_key',
                            on_change=update_motor_position3)

st.sidebar.subheader("Gripper")
c1, c2, c3 = st.sidebar.columns(3)

with c1:
    sleep = st.number_input("Duration", 0.04, 0.4, value=0.1, step=0.02)

with c2:
    if st.button("Open"):
        gripper_open(sleep)

with c3:
    if st.button("Close"):
        gripper_close(sleep)

# col1, col2, col3, col4, col5 = st.columns(5)
# with col1:
#     st.metric(label='Axis1', value=angle1)
# with col2:
#     st.metric(label='Axis2', value=angle2)
# with col3:
#     st.metric(label='Axis3', value=angle3)
# with col4:
#     st.metric(label='Axis4', value=angle4)
# with col5:
#     st.metric(label='Axis5', value=angle5)

output_file_name = st.text_input("Output file name .csv", "kpr_positions")
if st.button("Save Positions"):
    save_positions_to_csv(st.session_state['saved_positions'], f"{output_file_name}.csv")


# create a button that looops over saved positions and excutes each of them every 0.5 seconds
if st.button("Execute Saved Positions"):
    for pos in st.session_state['saved_positions']:
        update_motor_positions(pos)
    st.success("All saved positions executed successfully")

st.warning("Only if calibrated, claw pointing upwards with red stripe facing front")
