#!/opt/homebrew/bin/python3
import subprocess
import pyautogui
from pynput import keyboard

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

moveWindow(0,0)

def on_activate_left():
    moveWindow(0,0)

def on_activate_right():
    moveWindow(width/2, 0)

with keyboard.GlobalHotKeys({
        '<cmd>+<shift_l>+a': on_activate_left,
        '<cmd>+<shift_l>+d': on_activate_right}) as h:
    h.join()
