import pyautogui
import random
import tkinter as tk
import threading
import keyboard
import time  # Import the time module
from datetime import datetime

# Define three different click zones
click_zones = [
    (4978, 1230, 98, 100),  # Zone 1
]

scriptRunning = False
next_click_time = 0

def click_within_zone(zone):
    # Generate random coordinates within the specified zone
    x = random.randint(zone[0], zone[0] + zone[2])
    y = random.randint(zone[1], zone[1] + zone[3])

    # Move mouse to the random position and click
    pyautogui.moveTo(x, y, duration=random.uniform(1, 2))  # Randomize duration
    pyautogui.click()

def toggle_script():
    global scriptRunning
    scriptRunning = not scriptRunning
    if scriptRunning:
        start_stop_button.config(text="Stop Script")
    else:
        start_stop_button.config(text="Start Script")
    print("Script running:", scriptRunning)

def stop_listener():
    keyboard.add_hotkey('f12', lambda: toggle_script())

def update_status_label():
    global next_click_time
    if scriptRunning:
        status_label.config(text="Script running")
    else:
        status_label.config(text="Script stopped")
    if next_click_time > 0:
        next_click_label.config(text="Next Click in: {}s".format(round(next_click_time)))
    else:
        next_click_label.config(text="")
    root.after(1000, update_status_label)  # Update every second

def click_thread():
    global next_click_time
    while True:
        if scriptRunning:
            # Choose a random click zone
            selected_zone = random.choice(click_zones)
            click_within_zone(selected_zone)
            print("Clicked at", datetime.now())
            next_click_time = random.uniform(43, 266)   # Set next click time
            for _ in range(round(next_click_time)):
                if not scriptRunning:
                    break
                time.sleep(1)
                next_click_time -= 1
        else:
            time.sleep(1)

# Create GUI window
root = tk.Tk()
root.title("Script Status")
root.geometry("250x150")
root.attributes('-topmost', True)  # Make window stay on top

# Status label
status_label = tk.Label(root, text="Script stopped", font=("Arial", 12))
status_label.pack(pady=5)

# Button to start/stop the script
start_stop_button = tk.Button(root, text="Start Script", command=toggle_script)
start_stop_button.pack(pady=5)

# Next click timer label
next_click_label = tk.Label(root, text="", font=("Arial", 12))
next_click_label.pack(pady=5)

# Start the keyboard listener
stop_listener()

# Start the click thread
click_thread = threading.Thread(target=click_thread)
click_thread.daemon = True
click_thread.start()

# Start updating status label
update_status_label()

# Start the Tkinter event loop
root.mainloop()
