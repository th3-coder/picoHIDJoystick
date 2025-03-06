import time
import board
import analogio
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_debouncer import Debouncer

#name file main.py to run automatically 

#HID member 
kbd = Keyboard(usb_hid.devices)

#joystick pins
jy = analogio.AnalogIn(board.A1)
jx = analogio.AnalogIn(board.A0)

#button, debounce library to ensure accurate button presses
pin = digitalio.DigitalInOut(board.GP21)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP
button = Debouncer(pin)

#declare global variable to store previous input and check with current
prevX = None
prevY = None

#to determine voltage at analog pins
def get_voltage(raw):
    return (raw * 3.3) / 65536

while True:
    #must call every iteration to get updated button state
    button.update()
    
    #read joystick inputs inputs
    x = int(((jx.value) - 32768) / 100)
    y = int(((jy.value) - 32768) / 100)
    
    #test raw values, edit if there is stick drift occuring
    #print (x, y)
    
    #format joystick input for simple logic
    if x > 24:
        x = 2 #left
    elif x < -24:
        x = 0 #right
    else:
        x = 1 #center
    if y > 24:
        y = 0 #up
    elif y < -24:
        y = 2 #down
    else: 
        y = 1 #center
    
    #test values
    print(x, "," , y)
        
    #check if current direction is same as previous, if so skips entire branch
    if (prevX, prevY) != (x, y):
        
        kbd.release_all()
        
        #HID ouputs using adafruit_hid library
        #x, y inputs
        if x == 0 and y == 0:
            kbd.press(Keycode.LEFT_ARROW, Keycode.UP_ARROW)
        elif x == 0 and y == 2:
            kbd.press(Keycode.LEFT_ARROW, Keycode.DOWN_ARROW)
        elif x == 2 and y == 0:
            kbd.press(Keycode.RIGHT_ARROW, Keycode.UP_ARROW)
        elif x == 2 and y == 2:
            kbd.press(Keycode.RIGHT_ARROW, Keycode.DOWN_ARROW)
        else:
            if x == 0:
                kbd.press(Keycode.LEFT_ARROW)
            elif x == 2:
                kbd.press(Keycode.RIGHT_ARROW)
            elif y == 0:
                kbd.press(Keycode.UP_ARROW)
            elif y == 2:
                kbd.press(Keycode.DOWN_ARROW)
                
    #button input
    if not button.value:
        kbd.press(Keycode.SPACE)
        kbd.release(Keycode.SPACE)
    prevX, prevY = x, y
        
    time.sleep(0.01)