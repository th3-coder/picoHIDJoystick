import serial
import pydirectinput

# serial input from arduino. change COM port to wherever your arduino is connected
arduino = serial.Serial('COM4', 115200, timeout=0.1)

pydirectinput.PAUSE = 0

keysDown = {}  # list of currently pressed keys


def keyDown(key):  # what to do if key pressed. takes value from handleJoyStickAsArrowKeys
    keysDown[key] = True  # adds key to KeysDown list
    pydirectinput.keyDown(key)  # runs pydirectinput using key from (argument)
    # print('Down: ', key)       #remove '#' from print to test data stream


def keyUp(key):  # what to do if key released. takes value from handleJoyStickAsArrowKeys
    if key in keysDown:
        del (keysDown[key])  # remove key from KeysDown
        pydirectinput.keyUp(key)  # runs pydirectinput using key from (argument)
        # print('Up: ', key)         #remove '#' from print to test data stream


def handleJoyStickAsArrowKeys(y, x):
    if y == 2:  # 0 is up on joystick
        keyDown('down')  # add up key to keyDown (argument)
        keyUp('up')  # add down key to keyUp (argument), as you can't press up and down together
    elif y == 0:  # 2 is down on joystick
        keyDown('up')
        keyUp('down')
    else:  # 1 is neutral on joystick
        keyUp('up')
        keyUp('down')

    if x == 0:  # 1 is right on joystick
        keyDown('left')
        keyUp('right')
    elif x == 2:  # -1 is left on joystick
        keyDown('right')
        keyUp('left')
    else:  # 0 is neutral on joystick
        keyUp('left')
        keyUp('right')


while True:
    rawdata = arduino.readline()  # read serial data from arduino one line at a time
    data = str(rawdata.decode('utf-8'))  # decode the raw byte data into UTF-8
    if data.startswith("S"):  # make sure the read starts in the correct place
        dx = int(data[1])  # X direction is second digit in data (data[0] is 'S')
        dy = int(data[3])  # Y direction is fourth digit in data
        # print(dx, dy, JSButton)            #remove '#' from print to test data stream
        handleJoyStickAsArrowKeys(dx, dy)  # run body of code using dx, dy and JSButton as inputs
