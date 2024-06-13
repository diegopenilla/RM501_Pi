# when connecting run
ssh pi@192.168.178.21
# pipi20
cd RM501_Pi/
source env/bin/activate
cd rm501_lib/roboclaw_python/
streamlit run app_csv_wrist.py

