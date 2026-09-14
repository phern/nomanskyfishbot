import pyautogui
import pydirectinput
import pywinctl as pwc
import time
import sys

from classes import Indicator, CatchUI

DELAY = 1.00

def main():
    waitForWindow()
    initPyAutoGUI()
    countdownTimer(10)
    fishingLoop()
    print("Done")

# get status of game window
def windowStatus():
    nms_window = pwc.getWindowsWithTitle("No Man's Sky")
    return bool(nms_window)

# wait for the target window
def waitForWindow():
    timeout = 0
    nms_window = None
    print("Waiting for game window...")
    while not nms_window:
        
        timeout += 1
        if timeout == 1000:
            print("Game window not found. Exiting...")
            sys.exit()
            
        time.sleep(0.2)
        
        windows = pwc.getWindowsWithTitle("No Man's Sky")
        if windows:
            print("No Man's Sky found.")
            nms_window = windows[0]
            moveWindow(nms_window)
   
# move target window 
def moveWindow(window):
    window.activate()
    window.moveTo(0 ,0)


# init pyautogui and enable the failsafe
def initPyAutoGUI():
    pyautogui.FAILSAFE = True


# countdown timer 
def countdownTimer(seconds): 
    print("Starting", end="")
    for i in range(0, seconds):
        print(".", end="")
        time.sleep(DELAY)
    print("Started")


# prints coordinates of mouse
def reportMousePosition(seconds=10):
    for i in range(0, seconds):
     print(pyautogui.position())
     time.sleep(DELAY)


# holds down mouse
def useMouseButton(seconds=0.10):
    pydirectinput.mouseDown()
    time.sleep(seconds)
    pydirectinput.mouseUp()
    time.sleep(DELAY)


# takes screenshot of a region of the game and
# iterate over pixels and check for color_to_find
def searchScreenAreaForColor(x, y, width, height, color_to_find):
    region = (x, y, width, height)  # Define the region of interest
    screenshot = pyautogui.screenshot(region=region)
    try:
        for row in range(screenshot.width):
            for col in range(screenshot.height):
                pixel_rgb = screenshot.getpixel(row, col)
                if pixel_rgb == color_to_find:
                    print("Pixel found")
                    return True
    except ValueError:
        print("ValueError exception caught while searching for pixel color")
        return False


# checks if fishing indicator is currently displayed
def checkFishingIndicator():
    print("Now checking fishing indicator.")
    if searchScreenAreaForColor(Indicator.X, Indicator.Y, Indicator.WIDTH, Indicator.HEIGHT, Indicator.COLOR):
        print("Fishing indicator is active.")
        return True
    else:
        print("Fishing indicator color not found.")
        return False


# checks if the summary box that appears after a fish is caught is displayed
def checkFishBox():
    if searchScreenAreaForColor(CatchUI.X, CatchUI.Y, CatchUI.WIDTH, CatchUI.HEIGHT, CatchUI.COLOR):
        return True
    else:
        print("Could not determine if fish box is active.")


# mouse input for the game
def catchFish():
        useMouseButton()
        print("Fish caught!")
        print("Continuing.")
        time.sleep(3.00)


# check for existing game window, call pixel search functions, call input functions, loop
def fishingLoop():
    bot_state = True
    while bot_state == True:
        if not windowStatus():
            bot_state = False
            print("Fishing loop has ended.")
            sys.exit()
        if checkFishBox():
            catchFish()
            continue
        elif checkFishingIndicator():
            useMouseButton()
            if checkFishBox():
                catchFish()
                continue
            else:
                print("Fish not detected.")
                continue
        else:
            print("Indicator not detected.")
            continue


if __name__ == "__main__":
    main()
