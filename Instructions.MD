# RM501 Hax Notes

## NOTE
Coin Acceptor bottom PIN (stands for COUNTER) should be connected to PIN 2 in the arduino MEGA.

## WARNING
All operations must be carried out after the robot is in ORIGIN: 
With base motor (bottom most motor) at half range.
Pointing fully upwards and with
The RED STRIPE in the claw mechanism pointing directly forwards (towards sticker mechanism position). 

This can be achieved manually or using the app (more notes below).

## Summary 

In short, the PI should connect to the arduino via serial and start receiving messages, which activate the robot. To do this, the script read_signal.py on the directory /rm501_lib/roboclaw_python needs to be run. 

```bash
 cd /rm501_lib/roboclaw_python
python3  read_signal.py
```


While this script is running, coins given should activate the movement. 
Operating the Robot
Here is a breakdown of how to operate the robot. The robot has 4 states:
- READY (Green Lights) - ready to accept coins and trigger.
- OPERATING Mode (Yellow Lights) - coin has been received and the positions are executing.
- ERROR (Red Lights) - 
- APP (Blue Lights) 

The states are controlled with the 2 buttons and via the coin acceptor:

Button UP (turns light Green or Red).
When lights are GREEN the robot is READY to accept coins and trigger the picking sequence. 
This button sets the counter to 0 (green - ready ) or sets the counter to 20 (red - error
Button Down (turns light Blue or OFF). 
This should run the streamlight app, more notes below. 













## TODO:
Before the robot can work with the LEDs, buttons etc. these steps still need to be done 😀:


- Connect the Arduino Mega to the PI.
- Pull the repository code to the PI by running git pull.
- Check that the Arduino Mega is called /dev/CoinAcceptor in devices, check ls /dev/tty…
- If not, either configure the device with udev (tricky) 
  - OR change the name of the device in the script read_signal.py ->  this will work but the device name assigned could change..


In case the ARDUINO needs to be changed, the code to flash it is located in ./rmpi/controller.ino

- Once this is done turn on everything
- Go to  cd rm501_lib/roboclaw_python/ and execute
```
python3 read_signal.py
```
- Set the mechanical ORIGIN. 
    - Either turn the robot off and move the robot manually to the origin position 
    - OR with the robot on click the bottom button one time.
        - The lights should turn Blue.
        - Go to localhost:8501 or localhost:8502 in the browser if an app has not automatically opened already.
        - If needed, Calibrate the robot and calibrate the claw positions using the controls on the left. 


- Place the tooth mechanism around the picking point. 
- The precise point needs to be found. To do this, the sequence to pick the paper needs to be run. 
- To do this, there are 3 ways listed below (all require the robot to be in ORIGIN)

  1. Run python3 pick_paper.py (executes kpr_positions.csv)
  2. By running the app: streamlit run app_csv_wrist.py (UI APP)
  3. While read_signal.py is running, the LEDs are green: put a coin in the coin acceptor (executes kpr_positions too).


Any of these methods should allow you to execute the waypoint positions to pick the paper: kpr_positions.csv.

- Execute the sequence. When the robot goes into the position of pushing the mechanism. 
- Place the mechanism at that exact location.
- Run the sequence again and verify that the mechanism is correctly activated. 


Should the mechanism not be activated properly at any position (due to new print) in the next step you will be able to fix this. 

### Finishing the Movement 

- The current kpr_positions.csv with the waypoints to pick the paper does not currently include how to drop the paper onto the funnel.
- In the pi ( cd rm501_lib/roboclaw_python/ ), and run:

```bash
streamlit run app_csv_wrist.py     # Runs UI APP
```

- The app launches by default by loading kpr_positions.csv, each step in the sequence can be seen and executed on the right. 
- Click each position one by one, the robot should move each position one by one. find the stage at which the paper should be moved to the funnel. That step/waypoint needs to be edited. 
- Find the desired position(s) with (open claw to drop the paper onto the funnel) and record the position numbers…
- In the pi go to kpr_positions.csv and modify the specific entries. This is the ONLY way (the app cannot delete positions in sequence only add waypoints (steps) to the selected/current sequence of positions). 
- Once the csv has been manually edited, reload the csv file inside the app by clicking load button. This should reload the contents of kpr_positions.csv
- Execute the positions and see if it picks the paper.

### Operating the Robot

- Turn on devices in both boxes (RM501 and Lights Box)
- To make the robot operational simply the script needs to run.

```bash
python3 read_signal.py # needs to be run. 
```


## APP UI NOTES

To run the app alone, with the robot ON and plugged to the PI. 

```bash
streamlit run app_wrist_csv.py
```

### Right Side

- Chosen position Sequence 
- Load a position sequence by specifying the csv file name (these are found in the code directory, by default kpr_positions.csv is loaded. This file includes the instructions to pick the paper).
- See and trigger each individual position loaded.
- Save current positions in a csv file, this file can be loaded later to execute positions. 

### Left Side

- Control Absolute Positions for Motors 1,2,3
- Move Claw up and down and Turn it Right or Left. 
- Save a step onto the position sequence -> add the current position to the sequence.
