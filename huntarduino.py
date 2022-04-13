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
arduino = serial.Serial(port='COM10', baudrate=345600, timeout=.1)

# open record file and parse commands
alg = sys.argv[1]
commandItems, delays = shinyHuntUtils.readAndParseCommands(alg)

attempts = int(sys.argv[2])
form = app.window(title_re='mGBA - ')

# capture first set of pixels to test
pos, initialPixels = shinyHuntUtils.capturePosition("sprite")

# capture second set of pixels to fix false positive 
pos2, initialPixels2 = shinyHuntUtils.capturePosition("anchor")

form.send_keystrokes("]")
time.sleep(0.75)

while(1):
    attempts = attempts + 1
    shinyHuntUtils.writeCommands(arduino, commandItems, delays)

    # check if we have a shiny or if we're anchored
    pixels = pyautogui.screenshot().load()
    if ((pixels[pos[0], pos[1]] != initialPixels[pos[0], pos[1]]) and (pixels[pos2[0], pos2[1]] == initialPixels2[pos2[0], pos2[1]])):
        break
    form.send_keystrokes("]")
    time.sleep(0.75)
    
    shinyHuntUtils.printCurrentProgress(attempts)
    
shinyHuntUtils.sendSuccessMessage()
shinyHuntUtils.printCurrentTime()