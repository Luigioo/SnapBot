import tkinter as tk
import cv2
import pyautogui
from PIL import Image, ImageTk
import numpy as np

def update_frame():
    # Capture the screen
    screenshot = pyautogui.screenshot()
    
    # Convert the screenshot to an OpenCV image
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Convert the OpenCV image to a PIL image
    pil_image = Image.fromarray(frame)
    
    # Convert the PIL image to a Tkinter-compatible image
    tk_image = ImageTk.PhotoImage(pil_image)
    
    # Update the label with the new image
    label.config(image=tk_image)
    label.image = tk_image
    
    # # Schedule the next update
    root.after(10, update_frame)

# Create the main window
root = tk.Tk()

# Create a label to display the screenshot
label = tk.Label(root)
label.pack()

# Start the update loop
root.after(10, update_frame)

# Start the Tkinter event loop
root.mainloop()