#!/opt/homebrew/bin/python3

import subprocess
import pyautogui
import os
from os import system as osys
from pynput import keyboard

osys("clear")
print('''
$$\                                                     $$\                     
$$ |                                                    $$ |                    
$$$$$$$\  $$\   $$\  $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$$ | $$$$$$\   $$$$$$\  
$$  __$$\ $$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$ |$$  __$$\ $$  __$$\ 
$$ |  $$ |$$ |  $$ |$$ /  $$ |$$$$$$$$ |$$ |  \__|$$ /  $$ |$$ /  $$ |$$ /  $$ |
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$   ____|$$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ |
$$ |  $$ |\$$$$$$$ |$$$$$$$  |\$$$$$$$\ $$ |      \$$$$$$$ |\$$$$$$  |\$$$$$$$ |
\__|  \__| \____$$ |$$  ____/  \_______|\__|       \_______| \______/  \____$$ |
          $$\   $$ |$$ |                                              $$\   $$ |
          \$$$$$$  |$$ |                                              \$$$$$$  |
           \______/ \__|                                               \______/ 

made by mrdog233o5 (William Chen)''')

try:
    confFile = eval(open(os.path.expanduser('~')+"/.config/hyperdog/config.json", 'r').read())
    distant = confFile["distant"]
    gridSize = confFile["grid size"]

except:
    print("ERROR >>> config file error, READ THE FRIENDLY MANUAL!!!!! DO NOT ASK ME HOW!!!!!")
    exit(1)

keyPressed = {}
gridX = []
gridY = []
width = pyautogui.size().width
height = pyautogui.size().height
gridWidth = width // gridSize[0]
gridHeight = height // gridSize[1]

for i in range(gridSize[0]+1):
    gridX.append(gridWidth*i)
for i in range(gridSize[1]+1):
    gridY.append(gridHeight*i)

def find_closest_value(number, number_list):
    closest_value = min(number_list, key=lambda x: abs(x - number))
    if number >= number_list[len(number_list)-1]:
        closest_value = number_list[len(number_list)-1]
    return closest_value

def get_active_window_pos():
    script = 'tell application "System Events" to get position of window 1 of (process 1 where frontmost is true)'
    command = ['osascript', '-e', script]
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip()
    
    if result.returncode == 0 and output != "":
        window_pos = output.split(", ")
        window_x = int(window_pos[0])
        window_y = int(window_pos[1])
        return window_x, window_y
    else:
        return None

def get_active_window_size():
    script = 'tell application "System Events" to get size of window 1 of (process 1 where frontmost is true)'
    command = ['osascript', '-e', script]
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip()
    
    if result.returncode == 0 and output != "":
        window_size = output.split(", ")
        window_width = int(window_size[0])
        window_height = int(window_size[1])
        if window_width == 0:
            window_width = width
        if window_height == 0:
            window_height == height
        return window_width, window_height
    else:
        return None


def moveWindow(x,y):
    try:
        pos = get_active_window_pos()
        window_x, window_y = pos
        if x == "": x = window_x
        if y == "": y = window_y
        subprocess.run(['osascript', '-e', f'''
        tell application "System Events"
            set frontApp to name of first application process whose frontmost is true
            tell process frontApp
                set frontWindow to first window
                set position of frontWindow to {x, y} -- New position for the window
            end tell
        end tell'''])
    except:
        pass

def resizeWindow(x,y):
    try:
        size = get_active_window_size()
        window_width, window_height = size
        if x == "": x = window_width
        if y == "": y = window_height
        subprocess.run(['osascript', '-e', f'''
        tell application "System Events"
            set frontApp to name of first application process whose frontmost is true
            tell process frontApp
                set frontWindow to first window
                set currentBounds to size of frontWindow
                set size of frontWindow to {{{x}, {y}}}
            end tell
        end tell'''])
    except:
        pass

def on_activate_up():
    moveWindow("",distant)
    resizeWindow("",gridY[len(gridY)//2] - 2*distant)

def on_activate_down():
    moveWindow("", distant + gridY[len(gridY)//2])    
    resizeWindow("",height - gridY[len(gridY)//2] - 2*distant)

def on_activate_left():
    moveWindow(distant,"")
    resizeWindow(gridX[len(gridX)//2]-2*distant,"")

def on_activate_right():
    moveWindow(distant + gridX[len(gridX)//2], "")
    resizeWindow(width - gridX[len(gridX)//2]-2*distant,"")

def on_activate_full():
    moveWindow(distant, distant)
    resizeWindow(width-2*distant,height-2*distant)

def on_activate_init():
    x,y = get_active_window_pos()
    widthWin,heightWin = get_active_window_size()
    closestPos = [find_closest_value(x,gridX), find_closest_value(y,gridY)]
    closestSize = [find_closest_value(widthWin+x,gridX)-x, find_closest_value(heightWin+y,gridY)-y]
    moveWindow(closestPos[0]+distant,closestPos[1]+distant)
    resizeWindow(closestSize[0]-1*distant,closestSize[1]-1*distant)

with keyboard.GlobalHotKeys({
    '<ctrl>+<alt>+w': on_activate_up,
    '<ctrl>+<alt>+s': on_activate_down,
    '<ctrl>+<alt>+a': on_activate_left,
    '<ctrl>+<alt>+d': on_activate_right,
    '<ctrl>+<alt>+f': on_activate_full,
    '<ctrl>+<alt>+i': on_activate_init,
}) as h:
    h.join()
