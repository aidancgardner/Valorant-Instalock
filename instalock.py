import pyautogui
import keyboard
import cv2
import numpy as np
import time
from pynput.mouse import Listener, Button, Controller

# The toggle switch
toggle = False

# The coordinates of the screen region
top_left_x = 500
top_left_y = 885
bottom_right_x = 1418
bottom_right_y = 1048

# The sub-images to be located
sub_image = 'jett.png' # you can change the image to another character if wanted
selected_image = 'selectedjett.png' # also change this if you change the image above


# Mouse Controller
mouse = Controller()

def click_until_selected():
    # Load the image to be located
    template = cv2.imread(sub_image, 0)
    selected_template = cv2.imread(selected_image, 0)

    while True:  # Keep doing this until the "selected" image is found
        # Take a screenshot of the specified region
        screenshot = pyautogui.screenshot(region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y))
        
        # Convert the screenshot to grayscale
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        
        # Perform template matching for both images
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        selected_result = cv2.matchTemplate(screenshot, selected_template, cv2.TM_CCOEFF_NORMED)
        
        # Find the location of the best match
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        selected_min_val, selected_max_val, selected_min_loc, selected_max_loc = cv2.minMaxLoc(selected_result)
        
        # If the "selected" image is found, break the loop
        if selected_max_val >= 0.8:
            break

        # If the first image is found, click it
        if max_val >= 0.8:
            # Calculate the coordinates of the best match
            x = max_loc[0] + top_left_x
            y = max_loc[1] + top_left_y

            # Move the mouse to the center of the image and click
            mouse.position = (x + template.shape[1] // 2, y + template.shape[0] // 2)
            mouse.click(Button.left)
            time.sleep(0.1)  # Delay

    # The second position
    second_position = (960, 815)

    # Move the mouse to the second position and click
    mouse.position = second_position
    for i in range(10):
        mouse.click(Button.left)

    # Print "Locked in"
    print("Locked in")
    print("Program is toggled off.")

    # Turn off the program
    global toggle
    toggle = False

def toggle_program():
    global toggle
    toggle = not toggle
    if toggle:
        print("Program is toggled on.")
    else:
        print("Program is toggled off.")

# Set the hotkey to toggle the program on and off
keyboard.add_hotkey('t', toggle_program)

while True:
    if toggle:
        click_until_selected()
