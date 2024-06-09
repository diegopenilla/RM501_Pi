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

from calibrate_arm_v2 import calibrate
from roboclaw_3 import Roboclaw
import time

from app_utils import load_positions_from_csv, save_positions_to_csv

# INIT STATE
address1 = 0x80
address2 = 0x81
address3 = 0x82

if 'rc' not in st.session_state:
    rc = Roboclaw("/dev/tty.usbserial-DN41WBZS", 115200)
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

if 'q4_angle' not in st.session_state:
    st.session_state['q4_angle'] = 90

if 'q5_angle' not in st.session_state:
    st.session_state['q5_angle'] = 0

if 'saved_positions' not in st.session_state:
    try:
        st.session_state['saved_positions'] = load_positions_from_csv("positions_kpr.csv")
    except Exception as e:
        st.error(f"Error loading positions: {e}, initialized as empty list")
        st.session_state['saved_positions'] = []


input_file_name = st.text_input("Input file name .csv", "positions_kpr")
if st.button("Load Positions"):
    try:
        st.session_state['saved_positions'] = load_positions_from_csv(f"{input_file_name}.csv")
    except Exception as e:
        st.error(f"Error loading positions: {e}")

if 'motor1_pos_current' not in st.session_state:
    st.session_state['motor1_pos_current'] = 0
    st.session_state['motor2_pos_current'] = 0
    st.session_state['motor3_pos_current'] = 0

rc = st.session_state['rc']

if 'current_pos' not in st.session_state:
    enc1 = rc.ReadEncM2(address1)[1]  # base
    enc2 = rc.ReadEncM1(address2)[1]  # shoulder
    enc3 = rc.ReadEncM2(address2)[1]  # elbow

    enc4 = rc.ReadEncM1(address3)[1]  # wrist pitch
    enc5 = rc.ReadEncM2(address3)[1]  # wrist roll

    st.session_state['current_pos'] = [enc1, enc2, enc3]

    if 'motor1_slider_key' not in st.session_state:
        st.session_state['motor1_slider_key'] = enc1

    if 'motor2_slider_key' not in st.session_state:
        st.session_state['motor2_slider_key'] = enc2

    if 'motor3_slider_key' not in st.session_state:
        st.session_state['motor3_slider_key'] = enc3


def gripper_close(step=0.5):
    rc.SpeedAccelM1(address1, 3000, 3000)
    time.sleep(step)
    rc.SpeedAccelM1(address1, 3000, 0)


def gripper_open(step=0.5):
    rc.SpeedAccelM1(address1, 3000, -3000)
    time.sleep(step)
    rc.SpeedAccelM1(address1, 3000, 0)


# UTILS
def move_up_q4(continuous=True):
    rc.SpeedM1(address3, 2000)
    time.sleep(0.01)
    rc.SpeedM2(address3, 2000)
    time.sleep(0.5)

    st.session_state['q4_angle'] += 90/8

    if continuous:
        rc.SpeedM1(address3, 0)
        time.sleep(0.01)
        rc.SpeedM2(address3, 0)


def move_down_q4(continuous=True):
    rc.SpeedM1(address3, -2000)
    time.sleep(0.01)
    rc.SpeedM2(address3, -2000)
    time.sleep(0.5)

    st.session_state['q4_angle'] -= 90/8

    if continuous:
        rc.SpeedM1(address3, 0)
        time.sleep(0.01)
        rc.SpeedM2(address3, 0)


def turn_left_q5(continuous=True):
    rc.SpeedM1(address3, 2000)  # Motor 1 spins forward
    rc.SpeedM2(address3, -2000)  # Motor 2 spins backward
    time.sleep(0.5)  # Allow motors to spin long enough to achieve rotation
    st.session_state['q5_angle'] += 90 / 8

    if continuous:
        rc.SpeedM1(address3, 0)  # Stop Motor 1
        rc.SpeedM2(address3, 0)  # Stop Motor 2
        time.sleep(0.01)


def turn_right_q5(continuous=True):
    rc.SpeedM1(address3, -2000)  # Motor 1 spins backward
    rc.SpeedM2(address3, 2000)  # Motor 2 spins forward
    time.sleep(0.5)  # Allow motors to spin long enough to achieve rotation
    st.session_state['q5_angle'] -= 90 / 8

    if continuous:
        rc.SpeedM1(address3, 0)  # Stop Motor 1
        rc.SpeedM2(address3, 0)  # Stop Motor 2
        time.sleep(0.01)


def safe_update_motor_position(motor_id, position):
    try:
        if motor_id == 1:
            rc.SpeedAccelDeccelPositionM2(address1, 10000, 10000, 10000, position, 100)
        elif motor_id == 2:
            rc.SpeedAccelDeccelPositionM1(address2, 10000, 10000, 10000, position, 100)
        elif motor_id == 3:
            rc.SpeedAccelDeccelPositionM2(address2, 10000, 10000, 10000, position, 100)
        time.sleep(1)
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


def axis2_position_to_angle(position):
    return -(position - 16375) / 154.17


# Define a function to convert the motor positions to angles for a more general approach
def position_to_angle(position, max_angle, max_position):
    return position * max_angle / max_position


def update_motor_positions(positions):
    safe_update_motor_position(1, positions[0])
    safe_update_motor_position(2, positions[1])
    safe_update_motor_position(3, positions[2])

    # q4 is handled by speed, each call by 10 degrees
    target_angle4 = positions[3]
    current_angle4 = st.session_state['q4_angle']
    print(f"Current angle {current_angle4} target {target_angle4}")

    if current_angle4 > target_angle4:
        diff_steps = (current_angle4 - target_angle4) / 10
        print(f"Diff steps {diff_steps}")
        for i in range(int(diff_steps)):
            if i == diff_steps - 1:
                move_down_q4(continuous=True)
            move_down_q4()

    else:
        diff_steps = (target_angle4 - current_angle4) / 10
        for i in range(int(diff_steps)):
            if i == int(diff_steps) - 1:
                move_up_q4(continuous=True)
            move_up_q4()

    # q5
    target_angle5 = positions[4]
    current_angle5 = st.session_state['q5_angle']
    print(f"Current angle {current_angle5} target {target_angle5}")

    if current_angle5 > target_angle5:
        diff_steps = (current_angle5 - target_angle5) / (90 / 8)
        print(f"Diff steps {diff_steps}")
        for i in range(int(diff_steps)):
            if i == diff_steps - 1:
                turn_right_q5(continuous=True)
            turn_right_q5()

    else:
        diff_steps = (target_angle5 - current_angle5) / (90 / 8)
        for i in range(int(diff_steps)):
            if i == int(diff_steps) - 1:
                turn_left_q5(continuous=True)
            turn_left_q5()

    st.session_state['motor1_pos_current'] = positions[0]
    st.session_state['motor2_pos_current'] = positions[1]
    st.session_state['motor3_pos_current'] = positions[2]
    st.session_state['q4_angle'] = positions[3]
    st.session_state['q5_angle'] = positions[4]


# __________Streamlit app__________
# Assuming 'saved_positions' is already initialized and filled with lists of angle data
if 'saved_positions' not in st.session_state:
    st.session_state['saved_positions'] = []

st.sidebar.title('RM501 Move Master II')


save_position_name = st.sidebar.text_input("Position Name", "")
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Calibrate"):
        calibrate()

with col2:
    if st.button("Save Position"):
        pos = [st.session_state['motor1_slider_key'], st.session_state['motor2_slider_key'],
               st.session_state['motor3_slider_key'], st.session_state['q4_angle'], st.session_state['q5_angle'], save_position_name]

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
angle1 = position_to_angle(st.session_state['motor1_slider_key'], 300, 48000)
angle2 = axis2_position_to_angle(st.session_state['motor2_slider_key'])
angle3 = position_to_angle(st.session_state['motor3_slider_key'], 90, 14500)
angle4 = st.session_state['q4_angle']  # Assuming 'q4_angle' exists in session_state and initialized properly
angle5 = st.session_state['q5_angle']  # Assuming 'q5_angle' exists and is initialized


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

st.sidebar.subheader("Motor Positions")
# Set up number inputs
s = st.sidebar.number_input('Motor 1', -200, 48000, value=m1, step=1000, key='motor1_slider_key',
                            on_change=update_motor_position1)
a = st.sidebar.number_input('Motor 2', -200, 22000, value=m2, step=1000, key='motor2_slider_key',
                            on_change=update_motor_position2)
t = st.sidebar.number_input('Motor 3', -200, 15000, value=m3, step=1000, key='motor3_slider_key',
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
#
output_file_name = st.text_input("Output file name .csv", "positions_kpr")
if st.button("Save Positions"):
    save_positions_to_csv(st.session_state['saved_positions'], f"{output_file_name}.csv")