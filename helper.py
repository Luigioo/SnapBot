import cv2
import numpy as np


handArea = [557, 796, 1366, 970] # x, y, x1, y1 with respect to 1080p screen, hand card area
locationArea = [768, 968, 1152, 692] #x, x1, x2, y, location position


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
