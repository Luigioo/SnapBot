import os
import time

from helper import *

def follow_file(file_path, gameInfo):
    with open(file_path, 'r') as file:
        # Move the file pointer to the end
        # file.seek(0, os.SEEK_END)
        
        log = open('log.txt', 'w')
        extract_log = open('extract_log.txt', 'w')
        while True:
            # Check for any new data in the file
            line = file.readline()
            if not line:
                # If no new data, wait for a short time and check again
                time.sleep(0.1)
                continue
            
            # Process the new line of data
            line = line.strip()
            log.write(line+"\n")

            processed = line_process(line, gameInfo)
            if(processed):
                extract_log.write(processed+"\n")
                print(processed)  # Replace with your own processing logic

            
        extract_log.close()
        log.close()
            
def line_process(line, gameInfo):
    if(line.startswith("GameManager|OnStartGameScene")) : return line
    if(line.startswith("EndTurn|Turn=")) : 
        return line.replace("EndTurn|Turn=", "")
    if(line.startswith("CreateCustomActionAsync|LoadVfxDef|Start|LocationVfxDefs/") and line.endswith("RevealLocation")) : 
        return line.replace("CreateCustomActionAsync|LoadVfxDef|Start|LocationVfxDefs/", "").replace(".asset|RevealLocation", "")
    if(line.endswith("|DrawCard") and line.startswith("CreateCustomActionAsync|LoadVfxDef|Start|CardVfxDefs/") ) : 
        return line.replace("CreateCustomActionAsync|LoadVfxDef|Start|CardVfxDefs/", "").replace(".asset|DrawCard", "")
    
    if(line.startswith("CreateCustomActionAsync|LoadVfxDef|Start|")) : return line

    return False

    if(line.startswith("AvatarView")) : return False
    if(line.startswith("Found card back material in cache")) : return False
    return True


gameInfo = {
    'cardInfo': [],
    # "cardInfo(array)" : [
    #     {"name" : "quicksilver",
    #        },
    #     
    #     ....
    #     {}
    # ]
    'locationInfo': [
        {'pos' : [locationArea[0], locationArea[3]], 'name' : ''},
        {'pos' : [locationArea[1], locationArea[3]], 'name' : ''},
        {'pos' : [locationArea[2], locationArea[3]], 'name' : ''}
    ],
    # locationInfo[location[int x, int y] *3]
    'energy': 0,
    'turn' : 0
}

# Specify the path to the file you want to monitor
# for your usage, comment out the following two lines and replace with: 
# file_path = '<Local User Folder>/AppData/LocalLow/Second Dinner/SNAP/Player.log'
from ignore.private import path_to_snap_log 
file_path = path_to_snap_log 


follow_file(file_path, gameInfo)


