import cv2
import numpy as np
import random
import time
import pyautogui
from pynput.mouse import Button, Controller

handArea = [557, 796, 1366, 970] # x, y, x1, y1 with respect to 1080p screen, hand card area
locationy = 692
locationArea = [768, 968, 1152] #x, x1, x2 location position

cardPosy = 888
cardPosx=[
    [960],
    [890,1030],
    [860,960,1060],
    [800,910,1010,1120],
    [760,860,960,1060,1160],
    [780,850,920,990,1060,1130],
    [740,820,900,960,1020,1080,1170],
]
def mouseMove(x,y):

    mouse = Controller()
    start_mouse_pos = np.array([mouse.position[0],mouse.position[1]])
    target_pos = np.array([x,y])
    time_length = random.random()*0.1+0.1 #random 
    cur_time = time.time()
    end_time = cur_time+time_length

    random_tween()

    while(cur_time<end_time):
        t_proportion = (end_time-cur_time)/time_length
        new_pos = tween_func(target_pos,start_mouse_pos, t_proportion)
        mouse.position = (new_pos[0],new_pos[1])
        cur_time = time.time()
    
def mouseMovePos(position):
    mouseMove(position[0],position[1])

def linear_tween(start, end, t):
    """Linearly interpolate between start and end values."""
    return start * (1 - t) + end * t

def quadratic_ease_in(start, end, t):
    """Quadratic easing in."""
    return start * (1 - t**2) + end * t**2

def exponential_ease_out(start, end, t):
    """Exponential easing out."""
    return end * (1 - 2**(-10*t)) + start * (2**(-10*t))

tween_func = linear_tween
def random_tween():
    """Randomly choose a tweening algorithm."""
    global tween_func
    algorithms = [linear_tween, quadratic_ease_in, exponential_ease_out]
    tween_func = random.choice(algorithms)

def dragTo(start, end):
    mouse = Controller()
    mouseMovePos(start)
    time.sleep(0.2)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouseMovePos(end)
    time.sleep(0.1)
    mouse.release(Button.left)
    # global_utils.click([284, 46])
    time.sleep(0.1)

def matches_location(kp_mouse, kp_screenshot, good_matches):
    mouse_points = np.float32([kp_mouse[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    screenshot_points = np.float32([kp_screenshot[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    M, mask = cv2.findHomography(mouse_points, screenshot_points, cv2.RANSAC, 5.0)
    # h, w = mouse_image.shape
    h, w = 50, 50
    mouse_corners = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    transformed_corners = cv2.perspectiveTransform(mouse_corners, M)
    cursor_location = transformed_corners[0, 0]
    # return location as [x, y]
    return cursor_location

import cv2

def draw_point(overlay, pos, label):
    box_size = 10  # Adjust the size of the bounding box as desired
    x1, y1 = int(pos[0]) - box_size, int(pos[1]) - box_size
    x2, y2 = int(pos[0]) + box_size, int(pos[1]) + box_size
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 0, 255), 2)  # BGR color format: (0, 255, 0), Alpha: 255 (opaque)
    cv2.putText(overlay, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0, 255), 2)


