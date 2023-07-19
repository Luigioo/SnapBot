import os
import time

from helper import *

def follow_file(file_path, gameInfo):
    with open(file_path, 'r') as file:
        # Move the file pointer to the end
        file.seek(0, os.SEEK_END)
        
        log = open('log.txt', 'w')
        extract_log = open('extract_log.txt', 'w')
        while True:
            # Check for any new data in the file
            line = file.readline()
            if not line:
                # If no new data, wait for a short time and check again
                # print('asdf')
                time.sleep(0.1)
                continue
            
            # Process the new line of data
            line = line.strip()
            log.write(line+"\n")

            # print(line)

            processed = line_process(line, gameInfo)
            if(processed):
                extract_log.write(processed+"\n")
                print(processed)

            
        extract_log.close()
        log.close()
            
def line_process(line, gameInfo):
    # start of game
    if(line.startswith("GameManager|OnStartGameScene")) :
        gameInfo['turn'] = 1
        return line
    # turn count
    if(line.startswith("EndTurn|Turn=")) : 
        turn_count = int(line.replace("EndTurn|Turn=", ""))+1
        gameInfo['turn'] = turn_count
        return line.replace("EndTurn|Turn=", "")
    # start of turn
    if(line.startswith("RemoteGame|SendRequestObject|RequestType=CubeGame.StartTurnRequest")) : 
        # play card logic...
        time.sleep(1)
        play_card_logic(gameInfo)
        return "starting turn "+str(gameInfo['turn'])
    # location info
    if(line.startswith("CreateCustomActionAsync|LoadVfxDef|Start|LocationVfxDefs/") and line.endswith("RevealLocation")) : 
        location_name = line.replace("CreateCustomActionAsync|LoadVfxDef|Start|LocationVfxDefs/", "").replace(".asset|RevealLocation", "")
        return "location revealed: "+location_name
    
    # draw card
    if(line.endswith("|DrawCard") and line.startswith("CreateCustomActionAsync|LoadVfxDef|Start|CardVfxDefs/") ) : 
        card_name = line.replace("CreateCustomActionAsync|LoadVfxDef|Start|CardVfxDefs/", "").replace(".asset|DrawCard", "")
        if(len(card_name)>0):
            gameInfo['cardInfo'].append({"name": card_name})
            return "draw card "+card_name
    
    # if(line.startswith("CreateCustomActionAsync|LoadVfxDef|Start|")) : return line

    return False

    if(line.startswith("AvatarView")) : return False
    if(line.startswith("Found card back material in cache")) : return False
    return True

def isPresent(cardName):
    return next((index for index, card in enumerate(gameInfo['cardInfo']) if card.get('name') == cardName), -1)
def dragCard(positionInHand, locationId):
    length = len(gameInfo['cardInfo'])
    if(length==0):
        print("error: no cards on hand")
    cardx = cardPosx[length]
    cardy = cardPosy
    dragTo([cardx, cardy], [locationArea[locationId], locationy])
def playIfPresent(cardName, locationId):
    cpos = isPresent(cardName)
    if(cpos!=-1):
        dragCard(cpos, 2)
    gameInfo['cardInfo']
    del gameInfo['cardInfo'][cpos]


def play_card_logic(gameInfo):
    if(gameInfo['turn']==1):
        
        playIfPresent('quicksilver', 2)
        return
    elif(gameInfo['turn']==2):
        playIfPresent('quicksilver', 2)
        pass
    elif(gameInfo['turn']==3):
        pass
    elif(gameInfo['turn']==4):
        pass
    elif(gameInfo['turn']==5):
        pass
    elif(gameInfo['turn']==6):
        pass

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
        {'pos' : [locationArea[0], locationy], 'name' : ''},
        {'pos' : [locationArea[1], locationy], 'name' : ''},
        {'pos' : [locationArea[2], locationy], 'name' : ''}
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


