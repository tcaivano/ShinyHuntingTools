import string, serial, sys, time
import pyautogui
from datetime import datetime
from twilio.rest import Client
import serial.tools.list_ports
import constants

def convertKeyToSerialCommand(key: string):
    """
    convertKeyToSerialCommand converts a literal controller input to the corresponding serial command code

    :param key: controller input to convert
    :return: converted byte value of the input
    """ 
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

            
def writeToDevice(arduino, data):
    """
    writeToDevice writes a byte to the device and sleeps to prevent timeouts

    :param arduino: device to write to
    :param data: byte value to write
    :return: void
    """ 
    arduino.write(data)
    time.sleep(0.05)

def writeToDeviceAndSleep(arduino, key, delay):
    """
    writeToDeviceAndSleep writes a byte to the device with writeToDevice and sleeps before another command is sent 

    :param arduino: device to write to
    :param key: controller command to write to the device
    :param delay: amount of time to sleep, in seconds
    :return: void
    """ 
    writeToDevice(arduino, convertKeyToSerialCommand(key))
    time.sleep(delay)

def printCurrentTime():
    """
    printCurrentTime prints the current time to console

    :return: void
    """ 
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

def readAndParseCommands(alg):
    """
    readAndParseCommands reads commands from a text file to be used in a hunting loop. Command files should be structured with one command/time pair per line, separated by a comma

    :param alg: file to read
    :return: list of commands, list of delays
    """ 
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
    """
    capturePosition captures the user's mouse input at a particular point on the primary monitor

    :param name: string that indicates the current location being captured
    :return: position tuple that the user selected, initial screenshot of the primary monitor
    """ 
    print("Starting mouse capture, mouse over %s position..." % name)
    time.sleep(2)
    pos = pyautogui.position()
    initialPixels = pyautogui.screenshot().load()
    return pos, initialPixels

def writeCommands(arduino, commandItems, delays):
    """
    writeCommands writes a list of commandItems to an arduino device, sleeping between each command. commandItems and delays should have the same length

    :param device: device to write to
    :param commandItems: list of commands to write
    :param delays: list of delays between each command 
    :return: void
    """ 
    for x in range (0, len(commandItems)):
        writeToDevice(arduino, convertKeyToSerialCommand(commandItems[x]))
        time.sleep(float(delays[x]))

def printCurrentProgress(attempts: int):
    """
    printCurrentProgress prints the current hunt progress

    :param attempts: int number of attempts
    :return: void
    """ 
    sys.stdout.write("Attempt %s, %s%% chance of success...\r" % (attempts, round((1 -(1023/1024)**attempts) * 100, 2)))
    sys.stdout.flush()

def sendSuccessMessage(attempts: int):
    """
    sendSuccessMessage messages a phone number indicating that the hunt has been completed using the Twilio API

    :param attempts: int number of attempts
    :return: void
    """ 
    client = Client(constants.account_sid, constants.auth_token)
    client.messages.create(
        to= constants.toPhone, 
        from_= constants.fromPhone,
        body="Shiny Hunt complete after {0} resets".format(attempts))
    print("\nComplete after {0} resets".format(attempts))

def findArduinoCOM():
    """
    findArduinoCOM finds the first COM port with an Arduino device

    :return: string of the COM port name, i.e. COMX
    """ 
    ports = serial.tools.list_ports.comports(include_links=False)
    for port, desc, hwid in sorted(ports):
        if "Arduino" in desc:
            return port


def isEncounterDetected(pixels):
    if (pixels[0,0] == (0,0,0)):
        return True
    return False
