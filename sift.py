import cv2
import numpy as np
import time
from helper import *

# Load images
mouse_image = cv2.imread('data/quick.png', 0)  # Load the mouse image in grayscale
screenshot = cv2.imread('data/home.png', 0)    # Load the screenshot in grayscale

# Initialize SIFT
sift = cv2.SIFT_create()
orb = cv2.ORB_create()



# Find keypoints and descriptors
kp_mouse, des_mouse = sift.detectAndCompute(mouse_image, None)
kp_screenshot, des_screenshot = sift.detectAndCompute(screenshot, None)

time_start = time.time()

for i in range(10):
# Step 3: Detect keypoints and compute descriptors for the screenshot
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des_mouse, des_screenshot, k=2)

print(time.time()-time_start)



# Match keypoints

# Apply ratio test
good_matches = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)
        
print(len(good_matches))

# # Compute cursor location
# mouse_points = np.float32([kp_mouse[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
# screenshot_points = np.float32([kp_screenshot[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

# M, mask = cv2.findHomography(mouse_points, screenshot_points, cv2.RANSAC, 5.0)
# h, w = mouse_image.shape
# mouse_corners = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
# transformed_corners = cv2.perspectiveTransform(mouse_corners, M)
cursor_location = matches_location(kp_mouse, kp_screenshot, good_matches)

# Print cursor location
print("Mouse Cursor Location: ", cursor_location)