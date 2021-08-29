# This code is a modified version of: https://gist.github.com/wulfboy-95/0969c4f7135aa46e02bc0a9d3990286e

import board
import digitalio
import struct
import usb_hid
import time

from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# ConsumerControl object
cc = ConsumerControl(usb_hid.devices)

# initializing USB hid device
keyboard = None
for dev in list(usb_hid.devices):
    if ((dev.usage == 0x06) and
        (dev.usage_page == 0x01) and
        hasattr(dev, "send_report")):
        keyboard = dev
if keyboard == None:
    raise Exception("Device cannot be found")

# custom keycodes, actions are handeled in handleCustomkeycodes function
class CustomKeycodes:
    TOGGLEMACRO = 0x70
    SWITCHLAYOUTWINDOWS = 0x71
    SWITCHLAYOUTMAC = 0x72
    MACRO1 = 0x73
    MACRO2 = 0x74
    MACRO3 = 0x75
    MACRO4 = 0x76

# default 1-4 row layout
defaultColumns = [
    [
        Keycode.ESCAPE, Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.FOUR,
        Keycode.FIVE, Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE,
        Keycode.ZERO, Keycode.MINUS, Keycode.EQUALS, Keycode.BACKSPACE,
        Keycode.GRAVE_ACCENT
    ],
    [
        Keycode.TAB, Keycode.Q, Keycode.W, Keycode.E, Keycode.R, Keycode.T,
        Keycode.Y, Keycode.U, Keycode.I, Keycode.O, Keycode.P,
        Keycode.LEFT_BRACKET, Keycode.RIGHT_BRACKET, Keycode.BACKSLASH,
        Keycode.DELETE
    ],
    [
        Keycode.CAPS_LOCK, Keycode.A, Keycode.S, Keycode.D, Keycode.F,
        Keycode.G, Keycode.H, Keycode.J, Keycode.K, Keycode.L,
        Keycode.SEMICOLON, Keycode.QUOTE, Keycode.RETURN, Keycode.ENTER,
        Keycode.PAGE_UP
    ],
    [
        Keycode.LEFT_SHIFT, Keycode.SHIFT, Keycode.Z, Keycode.X, Keycode.C,
        Keycode.V, Keycode.B, Keycode.N, Keycode.M, Keycode.COMMA,
        Keycode.PERIOD, Keycode.FORWARD_SLASH, Keycode.RIGHT_SHIFT,
        Keycode.UP_ARROW, Keycode.PAGE_DOWN
    ]
]

# Replaces 4 keys on the right side to be macro keys
# (GRAVE_ACCENT, DELETE, PAGE_UP, PAGE_DOWN) -> (MACRO1, MACRO2, MACRO3, MACRO4)
# Replaces RIGHT_SHIFT with GRAVE_ACCENT
macroColumns = [
    [
        Keycode.ESCAPE, Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.FOUR,
        Keycode.FIVE, Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE,
        Keycode.ZERO, Keycode.MINUS, Keycode.EQUALS, Keycode.BACKSPACE,
        CustomKeycodes.MACRO1
    ],
    [
        Keycode.TAB, Keycode.Q, Keycode.W, Keycode.E, Keycode.R, Keycode.T,
        Keycode.Y, Keycode.U, Keycode.I, Keycode.O, Keycode.P,
        Keycode.LEFT_BRACKET, Keycode.RIGHT_BRACKET, Keycode.BACKSLASH,
        CustomKeycodes.MACRO2
    ],
    [
        Keycode.CAPS_LOCK, Keycode.A, Keycode.S, Keycode.D, Keycode.F,
        Keycode.G, Keycode.H, Keycode.J, Keycode.K, Keycode.L,
        Keycode.SEMICOLON, Keycode.QUOTE, Keycode.RETURN, Keycode.ENTER,
        CustomKeycodes.MACRO3
    ],
    [
        Keycode.LEFT_SHIFT, Keycode.SHIFT, Keycode.Z, Keycode.X, Keycode.C,
        Keycode.V, Keycode.B, Keycode.N, Keycode.M, Keycode.COMMA,
        Keycode.PERIOD, Keycode.FORWARD_SLASH, Keycode.GRAVE_ACCENT,
        Keycode.UP_ARROW, CustomKeycodes.MACRO4
    ]
]

# bottom row layout for macOS
layoutMac = [
    Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.LEFT_GUI,
    Keycode.SPACE, Keycode.SPACE, Keycode.SPACE, Keycode.SPACEBAR,
    Keycode.SPACE, Keycode.SPACE, CustomKeycodes.TOGGLEMACRO, CustomKeycodes.SWITCHLAYOUTWINDOWS,
    CustomKeycodes.SWITCHLAYOUTMAC, Keycode.LEFT_ARROW, Keycode.DOWN_ARROW,
    Keycode.RIGHT_ARROW
]

# bottom row layout for windowsOS
layoutWindows = [
    Keycode.LEFT_CONTROL, Keycode.LEFT_GUI, Keycode.LEFT_ALT,
    Keycode.SPACE, Keycode.SPACE, Keycode.SPACE, Keycode.SPACEBAR,
    Keycode.SPACE, Keycode.SPACE, CustomKeycodes.TOGGLEMACRO, CustomKeycodes.SWITCHLAYOUTWINDOWS,
    CustomKeycodes.SWITCHLAYOUTMAC, Keycode.LEFT_ARROW, Keycode.DOWN_ARROW,
    Keycode.RIGHT_ARROW
]

# Default boot layout is macOS based
matrix = [
    defaultColumns[0],
    defaultColumns[1],
    defaultColumns[2],
    defaultColumns[3],
    layoutMac
]

# Handles codes from Customkeycodes class
def handleCustomKeycodes(code):
    if code == CustomKeycodes.TOGGLEMACRO:
        if matrix[0] == defaultColumns[0]:
            print('macro on')
            matrix[0] = macroColumns[0]
            matrix[1] = macroColumns[1]
            matrix[2] = macroColumns[2]
            matrix[3] = macroColumns[3]
        else:
            print('macro off')
            matrix[0] = defaultColumns[0]
            matrix[1] = defaultColumns[1]
            matrix[2] = defaultColumns[2]
            matrix[3] = defaultColumns[3]
    elif code == CustomKeycodes.SWITCHLAYOUTWINDOWS:
        print('SWITCHLAYOUTWINDOWS')
        matrix[4] = layoutWindows
    elif code == CustomKeycodes.SWITCHLAYOUTMAC:
        print('SWITCHLAYOUTMAC')
        matrix[4] = layoutMac
    elif code == CustomKeycodes.MACRO1:
        print('MACRO1')
        cc.send(ConsumerControlCode.PLAY_PAUSE)
    elif code == CustomKeycodes.MACRO2:
        print('MACRO2')
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
    elif code == CustomKeycodes.MACRO3:
        print('MACRO3')
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
    elif code == CustomKeycodes.MACRO4:
        print('MACRO4')
        cc.send(ConsumerControlCode.MUTE)
    else:
        print('could not find custom keycode')
    
    time.sleep(0.15) # we sleep here since the custom keycodes execute some toggles and macros

inputPins = (board.GP0, board.GP1, board.GP2, board.GP3,board.GP4) # 5 input rows

inputPinArray = [] # DigitalIO array for inputs.

outputPins = (
    board.GP5, board.GP6, board.GP7, board.GP8, board.GP9,
    board.GP10, board.GP11, board.GP12, board.GP13, board.GP14,
    board.GP15, board.GP28, board.GP27, board.GP26, board.GP22
) # 15 output columns

outputPinArray = [] # DigitalIO array for outputs.

# Initialise DigitalIO pins.
for pin in inputPins:
    keyPin = digitalio.DigitalInOut(pin)
    keyPin.direction = digitalio.Direction.INPUT
    keyPin.pull = digitalio.Pull.DOWN
    inputPinArray.append(keyPin)

for pin in outputPins:
    keyPin = digitalio.DigitalInOut(pin)
    keyPin.direction = digitalio.Direction.OUTPUT
    keyPin.drive_mode = digitalio.DriveMode.PUSH_PULL
    outputPinArray.append(keyPin)

keysPressed = [] # list for possible n-key rollover functionality extension in the future
reportArray = [0x00] * 8

while True:
    for col in range(len(outputPinArray)):
        outputPinArray[col].value = True # Turn on column pin.
        for row in range(len(inputPinArray)):
            if (matrix[row][col] >= 0xE0) and (inputPinArray[row].value): # Check if modifier is pressed
                reportArray[0] |= Keycode.modifier_bit(matrix[row][col]) # Add modifier bit to report.
            elif inputPinArray[row].value: # Check if key is pressed.
                if matrix[row][col] >= 0x70: # Check if key is CustomKeycode
                    handleCustomKeycodes(matrix[row][col]) # evaluate & execute CustomKeycode command
                else:
                    keysPressed.append(matrix[row][col])
        outputPinArray[col].value = False # Turn off column pin.
    if len(keysPressed) > 6: # Check for Rollover Error
        for i in range(2,8):
            reportArray[i] = 0x01 # Add Rollover Error keycode*6 to report.
    else:
        for i in range(6):
            reportArray[i+2] = keysPressed[i] if i < len(keysPressed) else 0 # Add keycode to report.
    keyboard.send_report(struct.pack("8B",*reportArray))
    reportArray = [0x00] * 8
    keysPressed = []
