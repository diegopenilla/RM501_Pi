import datetime
import time


# Get the current time
current_time = datetime.datetime.now()

# Format the current time as desired
formatted_time = current_time.strftime("%Y%m%d_%H%M%S")

# Create a filename using the formatted time
filename = f"./results/{formatted_time}.txt"

# Create and open the file
with open(filename, 'w') as file:
    file.write("This file was created at " + current_time.strftime("%Y-%m-%d %H:%M:%S"))

print(f"File {filename} has been created.")

time.sleep(60)
