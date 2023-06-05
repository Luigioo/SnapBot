import cv2
import pyautogui
import numpy as np

# # Get screen size
screen_width, screen_height = pyautogui.size()

# Define 720p resolution
target_width, target_height = 1280, 720

# Create a transparent overlay window
overlay = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

while True:
    # Capture the screen
    screenshot = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Resize the frame to match the overlay dimensions
    frame = cv2.resize(frame, (overlay.shape[1], overlay.shape[0]))

    # Get the mouse position
    mouse_x, mouse_y = pyautogui.position()

    # Draw the bounding box around the mouse on the overlay
    overlay[:, :, :] = 0  # Clear the overlay
    box_size = 100  # Adjust the size of the bounding box as desired
    x1, y1 = mouse_x - box_size, mouse_y - box_size
    x2, y2 = mouse_x + box_size, mouse_y + box_size
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 0, 255), 2)  # BGR color format: (0, 255, 0), Alpha: 255 (opaque)

    # Combine the overlay with the frame
    result = cv2.addWeighted(frame, 1, overlay, 0.5, 0)

    # Resize the result to 720p resolution
    result = cv2.resize(result, (target_width, target_height))

    # Display the result
    cv2.imshow("Screen", result)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()