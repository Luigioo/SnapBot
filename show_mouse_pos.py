import tkinter as tk
import pyautogui

class MousePositionWidget:
    def __init__(self, master):
        self.master = master
        self.master.title('Mouse Position')
        
        # create a label to display the mouse position
        self.label = tk.Label(master, text='')
        self.label.pack(padx=10, pady=10)
        
        # update the mouse position every 100 milliseconds
        self.update_position()
        self.master.after(100, self.update_position)
        
    def update_position(self):
        # get the current mouse position
        x, y = pyautogui.position()
        
        # update the label text
        self.label.config(text='Mouse position: x = %d, y = %d' % (x, y))
        
        # schedule the next update
        self.master.after(100, self.update_position)

# create a Tkinter window and start the main event loop
root = tk.Tk()
root.attributes("-topmost", True)
widget = MousePositionWidget(root)
root.mainloop()