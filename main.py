#!/opt/homebrew/bin/python3

import subprocess
import pyautogui
from pynput import keyboard

distant = 10
keyPressed = {}
width = pyautogui.size().width
height = pyautogui.size().height
 
def moveWindow(x,y):
    subprocess.run(['osascript', '-e', f'''
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
        tell process frontApp
            set frontWindow to first window
            set position of frontWindow to {x, y} -- New position for the window
        end tell
    end tell'''])

def resizeWindow(x,y):
    subprocess.run(['osascript', '-e', f'''
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
        tell process frontApp
            set frontWindow to first window
            set size of frontWindow to {x, y} -- New size for the window
        end tell
    end tell'''])

def on_activate_up():
    moveWindow(distant,distant)
    resizeWindow(width - 2*distant,height/2 - 2*distant)

def on_activate_down():
    moveWindow(distant, distant + height/2)
    resizeWindow(width - 2*distant,height/2 - 2*distant)

def on_activate_left():
    moveWindow(distant,distant)
    resizeWindow(width/2-2*distant,height-2*distant)

def on_activate_right():
    moveWindow(distant + width/2, distant)
    resizeWindow(width/2-2*distant,height-2*distant)

def on_activate_full():
    moveWindow(distant, distant)
    resizeWindow(width-2*distant,height-2*distant)

with keyboard.GlobalHotKeys({
    '<cmd>+<shift_l>+w': on_activate_up,
    '<cmd>+<shift_l>+s': on_activate_down,
    '<cmd>+<shift_l>+a': on_activate_left,
    '<cmd>+<shift_l>+d': on_activate_right,
    '<cmd>+<shift_l>+z': on_activate_full
}) as h:
    h.join()
