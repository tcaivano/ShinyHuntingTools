import pywinauto, pyautogui
import sys, time, serial, signal
import shinyHuntUtils


attempts: int

def interruptHandler(sig, frame):
    print("\nStopped after {0} resets".format(attempts))
    sys.exit(0)

signal.signal(signal.SIGINT, interruptHandler)
shinyHuntUtils.printCurrentTime()

# connect to mGBA
app = pywinauto.application.Application().connect(best_match='mGBA - ', top_level_only=False, visible_only=False)

# connect to arduino
arduino = serial.Serial(port=shinyHuntUtils.findArduinoCOM(), baudrate=345600, timeout=.1)

# open record file and parse commands

alg = sys.argv[1]
commandItems, delays = shinyHuntUtils.readAndParseCommands(alg)
alg2 = sys.argv[2]
commandItems2, delays2 = shinyHuntUtils.readAndParseCommands(alg2)

attempts = int(sys.argv[3])
form = app.window(title_re='mGBA - ')

# capture first coord to test
pos, z = shinyHuntUtils.capturePosition("upper left")

# capture second coord to test
pos2, z = shinyHuntUtils.capturePosition("bottom right")

# capture third coord to anchor
pos3, initialPixels3 = shinyHuntUtils.capturePosition("anchor")

shinyHuntUtils.printCurrentProgress(attempts)
form.send_keystrokes("]")
time.sleep(0.75)

found = False
reset = True
w = pos2[0]-pos[0]
h = pos2[1]-pos[1]
r = (pos[0], pos[1], w, h)
while(1):
    time.sleep(0.75)
    attempts = attempts + 1
    if reset == True:
        shinyHuntUtils.writeCommands(arduino, commandItems, delays)
    else:
        shinyHuntUtils.writeCommands(arduino, commandItems2, delays2)

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

    pixels = pyautogui.screenshot().load()
    if ((pixels[pos3[0], pos3[1]] != initialPixels3[pos3[0], pos3[1]])):
        form.send_keystrokes("]")
        attempts = attempts - 1
        reset = True
    else:
        reset = False
    
    # run from the fight and try again
    if reset == False:
        # weather - todo add if
        # time.sleep(0.5)
        # shinyHuntUtils.writeToDeviceAndSleep(arduino, "a", 0.5)

        shinyHuntUtils.writeToDeviceAndSleep(arduino, "a", 0.25)
        shinyHuntUtils.writeToDeviceAndSleep(arduino, "down", 0.25)
        shinyHuntUtils.writeToDeviceAndSleep(arduino, "down", 0.25)
        shinyHuntUtils.writeToDeviceAndSleep(arduino, "right", 0.25)
        shinyHuntUtils.writeToDeviceAndSleep(arduino, "a", 0.5)
        shinyHuntUtils.writeToDeviceAndSleep(arduino, "a", 1.5)
        
        # check to see if we were blocked from running
        screenshot = pyautogui.screenshot()
        pixels = screenshot.load()
        if ((pixels[pos3[0], pos3[1]] == initialPixels3[pos3[0], pos3[1]])):
            form.send_keystrokes("]")
            reset = True
        else:
            reset = False

    shinyHuntUtils.printCurrentProgress(attempts)

shinyHuntUtils.sendSuccessMessage(attempts)
shinyHuntUtils.printCurrentTime()