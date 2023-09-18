#!/opt/homebrew/bin/python3

import subprocess
import pyautogui
from pynput import keyboard

distant = 10
keyPressed = {}
width = pyautogui.size().width
height = pyautogui.size().height

import subprocess

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
                set currentOrigin to position of frontWindow
                set size of frontWindow to {{{x}, {y}}}
                set position of frontWindow to currentOrigin
            end tell
        end tell'''])
    except:
        pass

def on_activate_up():
    moveWindow("",distant)
    resizeWindow("",height/2 - 1.5*distant)

def on_activate_down():
    moveWindow("", distant/2 + height/2)
    resizeWindow("",height/2 - 1.5*distant)

def on_activate_left():
    moveWindow(distant,"")
    resizeWindow(width/2-1.5*distant,"")

def on_activate_right():
    moveWindow(distant/2 + width/2, "")
    resizeWindow(width/2-1.5*distant,"")

def on_activate_full():
    moveWindow(distant, distant)
    resizeWindow(width-2*distant,height-2*distant)

with keyboard.GlobalHotKeys({
    '<cmd>+<shift_l>+w': on_activate_up,
    '<cmd>+<shift_l>+s': on_activate_down,
    '<cmd>+<shift_l>+a': on_activate_left,
    '<cmd>+<shift_l>+d': on_activate_right,
    '<cmd>+<shift_l>+z': on_activate_full,
}) as h:
    h.join()
