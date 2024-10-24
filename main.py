import pyautogui
import pydirectinput
import time


DELAY = 1.00


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


#########################################################################################################################


def main():

    initializePyAutoGUI()

    countdownTimer(10)

    ##reportMousePosition()
    ##checkFishingIndicator()
    startFishing()



    print("Done")


#########################################################################################################################


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


#used to capture coordinates needed to inspect the screen
def reportMousePosition(seconds=10):
    for i in range(0, seconds):
     print(pyautogui.position())
     time.sleep(DELAY)


#holds down key for duration in seconds with a delay after
def usemMouseButton(seconds=0.10):
    pydirectinput.mouseDown()
    time.sleep(seconds)
    pydirectinput.mouseUp()
    time.sleep(DELAY)



#########################################################################################################################



##def stopFishing():
def searchScreenAreaForColor(x, y, width, height, color_to_find):
    ##color_to_find = (255, 0, 0)
    region = (x, y, width, height)  # Define the region of interest
    screenshot = pyautogui.screenshot(region=region)

    #iterates over each pixel in region and checks for color_to_find
    for x in range(screenshot.width):
        for y in range(screenshot.height):
            if pyautogui.pixelMatchesColor(x + region[0], y + region[1], color_to_find, tolerance=55):
                print("Pixel found at:", x + region[0], y + region[1])
                return True
            else:
                print("incorrect pixel")
                ##time.sleep(0.25)
                
                

            ##pixel_color = screenshot.getpixel((x, y))

            ##print(pixel_color)
            ##if pixel_color == color_to_find:
            ##print("Color found at:", x + region[0], y + region[1])


def checkFishingIndicator():
    print("Now checking fishing indicator.")
    state = searchScreenAreaForColor(INDICATOR_X, INDICATOR_Y, INDICATOR_WIDTH, INDICATOR_HEIGHT, INDICATOR_COLOR)
    if state == True:
        print("Fishing indicator is active.")
        return True
    else:
        print("Unsure what happened with fishing indicator, please restart")
        exit()


def checkFishingLine():
    print("Now checking fishing line.")
    state = searchScreenAreaForColor(LINE_X, LINE_Y, LINE_WIDTH, LINE_HEIGHT, LINE_COLOR)
    if state == True:
        print("Fishing line is active")
        return True
    else:
        checkFishingLine()
        print("Unsure what happened with fishing line, please restart")
        ##exit()


def checkFishCaught():
    state = searchScreenAreaForColor(CATCHUI_X, CATCHUI_Y, CATCHUI_WIDTH, CATCHUI_HEIGHT, CATCHUI_COLOR)
    if state == True:
        usemMouseButton()
        print("Fish caught!")
        print("Continuing.")
        time.sleep(3.00)
        startFishing()
    else:
        print("Could not determine if fish was caught.")
        exit()


def reelInTheFish():
    usemMouseButton(3.00)
    time.sleep(5.00)
    checkFishCaught()


def startFishing():
    if checkFishingIndicator():
        usemMouseButton()
        if checkFishingLine():
            reelInTheFish()
        else:
            print("Problem checking the fishing line")
            exit()
    else:
        print("Unexpected Fishing error.")
        exit()


if __name__ == "__main__":
    main()