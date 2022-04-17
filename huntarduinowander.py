from operator import truediv
import threading
import pywinauto, pyautogui
import sys, time, serial, signal
import shinyHuntUtils


attempts: int
combat: bool = False

def interruptHandler(sig, frame):
    print("\nStopped after {0} resets".format(attempts))
    sys.exit(0)

def threadDetectCombat():
    global combat
    while(1):
        s = pyautogui.screenshot(region=r)
        pixels = s.load()
        s.save("logs\screenshotz.png") # save screenshots for logging purposes
        combat |= shinyHuntUtils.isEncounterDetected(pixels)

signal.signal(signal.SIGINT, interruptHandler)
shinyHuntUtils.printCurrentTime()

# connect to mGBA
app = pywinauto.application.Application().connect(best_match='mGBA - ', top_level_only=False, visible_only=False)

# connect to arduino
arduino = serial.Serial(port=shinyHuntUtils.findArduinoCOM(), baudrate=345600, timeout=.1)

attempts = int(sys.argv[1])
form = app.window(title_re='mGBA - ')

# capture first coord to test
pos, _ = shinyHuntUtils.capturePosition("upper left")

# capture second coord to test
pos2, _ = shinyHuntUtils.capturePosition("bottom right")

# initialize controls
found = False
w = pos2[0]-pos[0]
h = pos2[1]-pos[1]
r = (pos[0], pos[1], w, h)
walk = "left"

threading.Thread(target=threadDetectCombat, daemon=True).start()

while(1):
    shinyHuntUtils.printCurrentProgress(attempts)
    form.send_keystrokes("]")
    time.sleep(0.75)
    attempts = attempts + 1
    
    for _ in range(0, 6):
        shinyHuntUtils.writeToDeviceAndSleep(arduino, "a", 0.5)

     # while we don't have an encounter, wander
    combat = False
    while(combat == False):
        shinyHuntUtils.writeToDeviceAndSleep(arduino, walk, 0.01)
        if (combat == True):
            break
        else:
            shinyHuntUtils.writeToDeviceAndSleep(arduino, "a", 0.1)
            if (walk == "left"):
                walk = "right"
            else:
                walk = "left"

    
    # try to capture our shiny appearing
    screenshots = []
    for x in range(0, 15):
        screenshots.append(pyautogui.screenshot(region=r))
    
    # scrub through each screenshot
    z = 0
    for s in screenshots:
        pixels = s.load()
        s.save("logs\screenshot" + str(z) + ".png") # save screenshots for logging purposes
        z = z + 1
        for x in range (0, w):
            for y in range (0, h):
                if (pixels[x, y] == (255, 222, 140)):
                    found = True
                    break
    if (found):
        break

shinyHuntUtils.sendSuccessMessage(attempts)
shinyHuntUtils.printCurrentTime()