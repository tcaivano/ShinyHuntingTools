import string
from tokenize import Number
from pyscreeze import pixel
import pyautogui
import sys
import time
from datetime import datetime
from twilio.rest import Client
import constants

def convertKeyToSerialCommand(key):
    match key:
        case "up":
            return b'\x01'
        case "down":
            return b'\x02'
        case "left":
            return b'\x03'
        case "right":
            return b'\x04'
        case "select":
            return b'\x05'
        case "start":
            return b'\x06'
        case "lb":
            return b'\x07'
        case "rb":
            return b'\x08'
        case "a":
            return b'\x09'
        case "b":
            return b'\x0a'
        case "y":
            return b'\x0b'
        case "x":
            return b'\x0c'

            
def writeToDevice(arduino, x):
    arduino.write(x)
    time.sleep(0.05)

def writeToDeviceAndSleep(arduino, key, delay):
    writeToDevice(arduino, convertKeyToSerialCommand(key))
    time.sleep(delay)

def printCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

def readAndParseCommands(alg):
    with open(alg, 'r') as f:
        data = f.read()
    commandItems = []
    delays = []
    splitData = data.split('\n')
    for x in splitData:
        commandItems.append(x.split(",")[0])
        delays.append(x.split(",")[1])
    return commandItems, delays

def capturePosition(name: string):
    print("Starting mouse capture, mouse over %s position..." % name)
    time.sleep(2)
    pos = pyautogui.position()
    initialScreenshot = pyautogui.screenshot()
    initialPixels = initialScreenshot.load()
    return pos, initialPixels

def writeCommands(arduino, commandItems, delays):
    for x in range (0, len(commandItems)):
        writeToDevice(arduino, convertKeyToSerialCommand(commandItems[x]))
        time.sleep(float(delays[x]))

def printCurrentProgress(attempts: int):
    sys.stdout.write("Attempt %s, %s%% chance of success...\r" % (attempts, (1 -(1023/1024)**attempts) * 100))
    sys.stdout.flush()

def sendSuccessMessage(attempts: int):
    client = Client(constants.account_sid, constants.auth_token)
    client.messages.create(
        to= constants.toPhone, 
        from_= constants.fromPhone,
        body="Shiny Hunt complete after {0} resets".format(attempts))
    print("\nComplete after {0} resets".format(attempts))
