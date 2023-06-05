import cv2
import pyautogui
import numpy as np

# Initialize SIFT
sift = cv2.SIFT_create()


def find_most_probable_object(screenshot, object_images, sift = cv2.SIFT_create()):
    # Step 2: Convert screenshot to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Step 3: Detect keypoints and compute descriptors for the screenshot
    keypoints_screenshot, descriptors_screenshot = sift.detectAndCompute(screenshot_gray, None)

    best_match_score = 0
    best_match_index = -1

    for i, object_image in enumerate(object_images):
        # Step 5: Convert object image to grayscale
        object_gray = cv2.cvtColor(object_image, cv2.COLOR_BGR2GRAY)

        # Step 6: Detect keypoints and compute descriptors for the object image
        keypoints_object, descriptors_object = sift.detectAndCompute(object_gray, None)

        # Step 6: Match the descriptors
        matcher = cv2.BFMatcher(cv2.NORM_L2)
        matches = matcher.match(descriptors_screenshot, descriptors_object)

        # Step 7: Calculate a similarity score
        match_score = len(matches)

        if match_score > best_match_score:
            best_match_score = match_score
            best_match_index = i

    # Step 8: Select the most probable object
    most_probable_object = object_images[best_match_index]

    return most_probable_object

