import os
import time

def follow_file(file_path):
    with open(file_path, 'r') as file:
        # Move the file pointer to the end
        file.seek(0, os.SEEK_END)
        
        log_file = open('ignore/log.txt', 'w')

        while True:
            # Check for any new data in the file
            line = file.readline()
            if not line:
                # If no new data, wait for a short time and check again
                time.sleep(0.1)
                continue
            
            # Process the new line of data
            log_file.write("Log message\n")
            log_file.close()

            print(line.strip())  # Replace with your own processing logic
            

# Specify the path to the file you want to monitor
from ignore.private import path_to_snap_log # for your usage, comment out the following two lines and replace with: 
file_path = path_to_snap_log # file_path = '<Local User Folder>/AppData/LocalLow/Second Dinner/SNAP/Player.log'
follow_file(file_path)


