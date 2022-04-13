import pywinauto, pyautogui
import sys, time, serial, signal
import shinyHuntUtils

attempts: int = 0

def interruptHandler(sig, frame):
    print("\nStopped after {0} resets".format(attempts))
    sys.exit(0)

signal.signal(signal.SIGINT, interruptHandler)
shinyHuntUtils.printCurrentTime()

# connect to mGBA
app = pywinauto.application.Application().connect(best_match='mGBA - ', top_level_only=False, visible_only=False)
form = app.window(title_re='mGBA - ')

# capture first set of pixels to test
pos, initialPixels = shinyHuntUtils.capturePosition("sprite")

# capture second set of pixels to fix false positive 
pos2, initialPixels2 = shinyHuntUtils.capturePosition("anchor")

shinyHuntUtils.printCurrentProgress(attempts)
form.send_keystrokes("{VK_F5}")

while(1):
    attempts = attempts + 1
    form.send_keystrokes("xxxxxxx")
    time.sleep(0.1)
    form.send_keystrokes("xxxxxxx")
    time.sleep(1.0)

    # check if we have a catch by checking if our pixel has changed
    pixels = pyautogui.screenshot().load()
    if ((pixels[pos[0], pos[1]] != initialPixels[pos[0], pos[1]]) and (pixels[pos2[0], pos2[1]] == initialPixels2[pos2[0], pos2[1]])):
        break
    form.send_keystrokes("{VK_F5}")
    time.sleep(0.75)
    
    shinyHuntUtils.printCurrentProgress(attempts)
    
print("Done")
shinyHuntUtils.printCurrentTime()