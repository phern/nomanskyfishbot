import pyautogui
import pydirectinput
import time


DELAY = 1.00

#These constants represent the X and Y coordinates where we
#will begin our search for on screen items.
#Resolution is assumed to be 1080p


#
INDICATOR_X = 927
INDICATOR_Y = 549
INDICATOR_WIDTH = 100
INDICATOR_HEIGHT = 100
INDICATOR_COLOR = (245,189,91)


LINE_X = 1124
LINE_Y = 180
LINE_WIDTH = 75
LINE_HEIGHT = 75
LINE_COLOR = (51,247,137)


CATCHUI_X = 939
CATCHUI_Y = 627
CATCHUI_WIDTH = 15
CATCHUI_HEIGHT =  15
CATCHUI_COLOR = (36,43,34)


def main():

    initializePyAutoGUI()

    countdownTimer(10)

    #reportMousePosition()
    ##checkFishingIndicator()
    ##startFishing()
    fishingLoop()



    print("Done")


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


#prints coordinates
def reportMousePosition(seconds=10):
    for i in range(0, seconds):
     print(pyautogui.position())
     time.sleep(DELAY)


#holds down key for duration in seconds with a delay after
def useMouseButton(seconds=0.10):
    pydirectinput.mouseDown()
    time.sleep(seconds)
    pydirectinput.mouseUp()
    time.sleep(DELAY)


##def stopFishing():
def searchScreenAreaForColor(x, y, width, height, color_to_find, tolerance):
    ##color_to_find = (255, 0, 0)
    region = (x, y, width, height)  # Define the region of interest
    screenshot = pyautogui.screenshot(region=region)

    #iterates over each pixel in region and checks for color_to_find
    for x in range(screenshot.width):
        for y in range(screenshot.height):
            if pyautogui.pixelMatchesColor(x + region[0], y + region[1], color_to_find, tolerance):
                print("Pixel found at:", x + region[0], y + region[1])
                return True
            else:
                continue


#checks the color of the screen where the fishing indicator is expected to appear
def checkFishingIndicator():
    print("Now checking fishing indicator.")
    if searchScreenAreaForColor(INDICATOR_X, INDICATOR_Y, INDICATOR_WIDTH, INDICATOR_HEIGHT, INDICATOR_COLOR, 25):
        print("Fishing indicator is active.")
        return True
    else:
        print("Fishing indicator color not found.")
        return False


#checks the color of the screen for the popup box that only appears after catching a fish
#if the fish is caught, calls the entire sequence
def checkFishBox():
    if searchScreenAreaForColor(CATCHUI_X, CATCHUI_Y, CATCHUI_WIDTH, CATCHUI_HEIGHT, CATCHUI_COLOR, 10):
        return True
    else:
        print("Could not determine if fish box is active.")


def catchFish():
        useMouseButton()
        print("Fish caught!")
        print("Continuing.")
        time.sleep(3.00)


def startFishing():
    if checkFishingIndicator():
        useMouseButton()
        if checkFishBox():
            catchFish()
            startFishing()
        else:
            checkFishBox()
            print("Problem catching the fish")
    else:
        print("Unexpected Fishing error.")
        exit()


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