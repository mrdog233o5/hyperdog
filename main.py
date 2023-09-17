#!/opt/homebrew/bin/python3
import subprocess

# Define the AppleScript code to set the size of a Finder window
applescript_code = '''
tell application "Finder"
    activate -- Bring Finder to the front
end tell

tell application "System Events"
    tell process "Finder"
        set frontmost to true
        tell window 1
            set size to {800, 600} -- New size for the window
            set position to {100, 100} -- New position for the window
        end tell
    end tell
end tell
'''

# Execute the AppleScript code using osascript
subprocess.run(['osascript', '-e', applescript_code])
