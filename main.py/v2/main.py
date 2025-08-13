import time
import board
import analogio
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_debouncer import Debouncer
        
#buffer VALUES
ARCADE = 210
FIGHTING = 60
buffer = ARCADE

#HID member 
kbd = Keyboard(usb_hid.devices)

#joystick pins
jy = analogio.AnalogIn(board.A1)
jx = analogio.AnalogIn(board.A0)

#led flash
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

#button, debounce library to ensure accurate button presses
pin = digitalio.DigitalInOut(board.GP21)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP
button = Debouncer(pin)

#declare global variable to store previous input and check with current
prevX = None
prevY = None
prevButton = None
calibC = 0
xCalib, yCalib = 0, 0
xsum, ysum = 0, 0
cled = 0
#to determine voltage at analog pins
def get_voltage(raw):
    return (raw * 3.3) / 65536

while True:
    time.sleep(0.015) #sleep to avoid reduce cpu usage
    #must call every iteration to get updated button state
    button.update()

    cled += 1
    if cled == 15:
        led.value = 0
    elif cled == 45:
        #reset so int dooes not take more space than necessary
        led.value = 1
    cled = 0 if cled == 60 else cled
    #print(f"LED: {cled}")     
    #read joystick inputs inputs
    x = int(((jx.value) - 32768) / 100)
    y = int(((jy.value) - 32768) / 100)
    
    #calibration setting, hold button for 4.5 seconds
    if not button.value:
        calibC += 1
        print(f'Counter {calibC}')
        if calibC >= 200:
            print("Calibrating, hold joystick in center position")
            xsum = xsum + x
            ysum = ysum + y
            #print(f'Sum(x,y): {xsum} {ysum}')
            if calibC == 300:
                #print(f'Calibration: {xavg} {yavg}')
                xavg = int(xsum/(300-200))
                yavg = int(ysum/(300-200))
                xCalib = -xavg
                yCalib = -yavg
                calibC = 0
                print(f'Calibration Values(x,y): {xCalib} {yCalib} ')
                kbd.release(Keycode.TAB)
                time.sleep(3.3)
                print("Calibrated!")
            continue

    else:
        xsum, ysum, xavg, yavg, calibC = 0, 0, 0, 0, 0
    
    #print(f'Calibration --- Counter:{calibC} x:{xCalib} y:{yCalib}')
    ####uncomment to test raw values, edit if there is stick drift occuring (make auto calibration or GUI)###
    #print("x raw:", jx.value, "y raw:", jy.value)
    #print(f"X: {x} Y: {y}")    
    xtemp = x
    ytemp = y
    x = x + xCalib
    y = y + yCalib
    #format joystick input for simple logic
    if x > buffer:
        x = 2 #right
    elif x < -buffer:
        x = 0 #left
    else:
        x = 1 #center
    if y > buffer:
        y = 0 #up
    elif y < -buffer:
        y = 2 #down
    else: 
        y = 1 #center
    
    #check if current direction is same as previous, if so skips entire branch
    if (prevX, prevY) != (x, y):
        
        kbd.release_all()
        #print (f'X: {xtemp} Y: {ytemp}')
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
    if prevButton != button.value: 
        if not button.value:
            kbd.press(Keycode.TAB)
        else:
            kbd.release(Keycode.TAB)
            
    #store previous values
    prevButton = button.value
    prevX, prevY = x, y
    
