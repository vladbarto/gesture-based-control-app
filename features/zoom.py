import subprocess

def app_zoom_in():
    subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 24 using {command down}'])

def app_zoom_out():
    subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 27 using {command down}'])

def do_zoom(left_hand_landmarks, right_hand_landmarks, frame):
    print("ceva")
