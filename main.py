import pyautogui
import pydirectinput
import time

from classes import Indicator, CatchUI

DELAY = 1.00

#These constants represent the X and Y coordinates where we
# will begin our search for UI colors.
#Resolution is assumed to be 1080p


def main():

    try:
        initializePyAutoGUI()
        countdownTimer(10)
        fishingLoop()
        print("Done")
    except Exception as e:
        print(f"An error occured: {str(e)}")
    finally:
        print("L")

#initializing pyautogui and enabling the failsafe
def initializePyAutoGUI():
    pyautogui.FAILSAFE = True


#countdown timer 
def countdownTimer(seconds): 
    print("Starting", end="")
    for i in range(0, seconds):
        print(".", end="")
        time.sleep(DELAY)
    print("Started")


#prints coordinates of mouse
def reportMousePosition(seconds=10):
    for i in range(0, seconds):
     print(pyautogui.position())
     time.sleep(DELAY)


#holds down mouse
def useMouseButton(seconds=0.10):
    pydirectinput.mouseDown()
    time.sleep(seconds)
    pydirectinput.mouseUp()
    time.sleep(DELAY)



def searchScreenAreaForColor(x, y, width, height, color_to_find, tolerance):
    region = (x, y, width, height)  # Define the region of interest
    screenshot = pyautogui.screenshot(region=region)

    #iterates over each pixel in region and checks for color_to_find
    try:
        for x in range(screenshot.width):
            for y in range(screenshot.height):
                if pyautogui.pixelMatchesColor(x + region[0], y + region[1], color_to_find, tolerance):
                    print("Pixel found at:", x + region[0], y + region[1])
                    return True
                else:
                    continue
    except:
        print("oops")


#checks if fishing indicator is currently displayed
def checkFishingIndicator():
    print("Now checking fishing indicator.")
    if searchScreenAreaForColor(Indicator.X, Indicator.Y, Indicator.WIDTH, Indicator.HEIGHT, Indicator.COLOR, 25):
        print("Fishing indicator is active.")
        return True
    else:
        print("Fishing indicator color not found.")
        return False

#checks if the summary box that appears after a fish is caught is displayed
def checkFishBox():
    if searchScreenAreaForColor(CatchUI.X, CatchUI.Y, CatchUI.WIDTH, CatchUI.HEIGHT, CatchUI.COLOR, 10):
        return True
    else:
        print("Could not determine if fish box is active.")

#not great naming
def catchFish():
        useMouseButton()
        print("Fish caught!")
        print("Continuing.")
        time.sleep(3.00)


def fishingLoop():
    bot_state = True
    while bot_state == True:
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
    else:
        bot_state = False
        print("Fishing loop has ended.")
        exit()


if __name__ == "__main__":
    main()