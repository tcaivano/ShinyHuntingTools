# AutomatedShinyHunting
Tools to automate shiny hunting in various games

## Main Files

### hunterarduino.py
Accepts two mandatory arguments of a command file location and starting count of attempts.
Standard shiny hunting utility. Attaches to the emulator using pywinauto and to the Arduino via serial, and executes commands defined in a command file. Prompts the user for a "sprite" position, which is a pixel location on the target's sprite that should change, and then prompts the user for an "anchor" position, which is a pixel location that should not change, such as an area of the GUI. Executes the commands from the command file input until the "sprite" pixels change. Will also send a text message when complete.

### hunterarduinoss.py
Accepts three mandatory arguments of a command file location, a secondary command file location, and starting count of attempts.
Shiny hunting utility that takes advantage of the field move "Sweet Scent". Attaches to the emulator using pywinauto and to the Arduino via serial, and executes commands defined in a command file. Prompts the user for two "sprite" positions, which define a square area to check for shiny sparkles, and then prompts the user for an "anchor" position, which is a pixel location that should not change, such as an area of the GUI. Executes the commands from the command file input and captures several screenshots. If a sparkle pixel is detected in the screenshot, then stops the loop. Otherwise, will attempt to run from the battle and begin the secondary command list. Otherwise will reset and try again. Will also send a text message when complete.