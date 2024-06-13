import datetime
import time


# Get the current time
current_time = datetime.datetime.now()

# Format the current time as desired
formatted_time = current_time.strftime("%Y%m%d_%H%M%S")

# Create a filename using the formatted time
filename = f"./results/{formatted_time}.txt"


time.sleep(600)
