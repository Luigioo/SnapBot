import cv2
import pyautogui
import numpy as np
import os
import time
from helper import *

# init GUI
screen_width, screen_height = pyautogui.size()
target_width, target_height = int(1280*1.2), int(720*1.2)
overlay = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

sift = cv2.SIFT_create()
bf = cv2.BFMatcher()

card_dict = {}
folder_path = "./data/cards/"
for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        card_image = cv2.imread(folder_path+filename, 0)
        kp_card, des_card = sift.detectAndCompute(card_image, None)
        card_dict[filename[:-4]] = [kp_card, des_card]


gameInfo = {
    'cardInfo': {},
    # "cardInfo(dict)" : {
    #     "cardname" : {'location': [int x, int y], },
    #     ....
    #     "cardname" : {}
    # }
    'locationInfo': [
        [locationArea[0], locationArea[3]],
        [locationArea[1], locationArea[3]],
        [locationArea[2], locationArea[3]],
    ],
    # locationInfo[location[int x, int y] *3]
    'energy': 0,
    'turn' : 0
}


while True:
    # Capture the screen
    screenshot = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    kp_screenshot, des_screenshot = sift.detectAndCompute(frame, None)

    # Draw the bounding box around the mouse on the overlay
    overlay[:, :, :] = 0

    gameInfo['cardInfo'] = {}

    for name, content in card_dict.items():

        matches = bf.knnMatch(content[1], des_screenshot, k=2)
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
        if(len(good_matches)<4):
            continue
        location = matches_location(content[0], kp_screenshot, good_matches)

        # add card info
        gameInfo['cardInfo'][name]['location'] = location
        

        draw_point(overlay, location)


    # Get the mouse position
    mouse_x, mouse_y = pyautogui.position()


    draw_point(overlay, [mouse_x, mouse_y])


    result = cv2.addWeighted(frame, 1, overlay, 0.5, 0)
    result = cv2.resize(result, (target_width, target_height))
    # cv2.imshow("Screen", result)
    if cv2.waitKey(1) == ord('q'):
        break
    time.sleep(0.001)

# Release resources
cv2.destroyAllWindows()