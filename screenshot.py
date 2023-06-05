import pyautogui
import datetime

# Get the current timestamp
timestamp = datetime.datetime.now().strftime("%m%d%H%M%S")

# Capture the screen
screenshot = pyautogui.screenshot()

# Save the screenshot as an image file
screenshot.save(f"screen_{timestamp}.png")