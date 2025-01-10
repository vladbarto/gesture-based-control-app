# reference: https://stackoverflow.com/questions/281133/how-to-control-the-mouse-in-mac-using-python
import threading

from pynput.mouse import Button, Controller
import cv2
from utils.common import BGR_YELLOW, euclidean_distance
from utils.hand_constants import THUMB_TIP, INDEX_FINGER_PIP, INDEX_FINGER_TIP
import os, subprocess, glob, time

mouse = Controller()

def launch_preview(selected_file):
    if selected_file:
        osascript_command = f'tell application "Preview" to open "{selected_file}"'
        subprocess.run(["osascript", "-e", osascript_command])
        # Display metadata using mdls
        metadata = subprocess.run(["mdls", selected_file], capture_output=True, text=True).stdout
        print(metadata)
    else:
        print("[DEBUG] No file selected.")


def get_selected_files(directory, file_extensions=("*.jpg", "*.png", "*.jpeg")):
    files = []
    for ext in file_extensions:
        files.extend(glob.glob(os.path.join(directory, ext)))
    return files


def get_first_selected_file(directory, file_extensions=("*.jpg", "*.png", "*.jpeg")):
    for ext in file_extensions:
        files = glob.glob(os.path.join(directory, ext))
        if files:
            return files[0]  # Return the first matching file
    return None


"""
handLandmarks[a][b]
- a = accesezi una dintre cele 21 de constante definite in utils.hand_constants
   deci poti avea acces la diferite componente din aratator, deget mare sau orice alt deget, + incheietura
- b = pozitionarea componentei "a" in fereastra
   0 = x
   1 = y
"""
def mouse_interact(handLandmarks):
    point1 = (x_thumb, y_thumb) = (handLandmarks[THUMB_TIP][0], handLandmarks[THUMB_TIP][1])
    point2 = (x_index, y_index) = (handLandmarks[INDEX_FINGER_PIP][0], handLandmarks[INDEX_FINGER_PIP][1])
    point3 = (x_index_tip, y_index_tip) = (handLandmarks[INDEX_FINGER_TIP][0], handLandmarks[INDEX_FINGER_TIP][1])

    dist = euclidean_distance(point1, point2)
    dist2 = euclidean_distance(point2, point3)

    if dist < 0.04:
        print("[DEBUG] Left click")
        mouse.click(Button.left, 1)

    print(dist2)
    if dist2 < 0.045:
        mouse.click(Button.left, 2)
    else:
        mouse.release(Button.left)
        directory = subprocess.run(["pwd"], capture_output=True, text=True).stdout.strip()
        selected_files = get_selected_files(directory)
        selected_file = get_first_selected_file(directory)
        if selected_file:
            mouse.click(Button.left, 2)  # Double click to open file in Preview
            time.sleep(0.5)
        else:
            print("[DEBUG] No file selected.")

def move_mouse(x, y, frame):
    # Read pointer position
    print('The current pointer position is {0}'.format(mouse.position))

    cv2.circle(img=frame, center=(x, y), radius=8, color=BGR_YELLOW, thickness=3)

    mouse.position = (x, y)

def do_jerry_mouse(x, y, frame, handLandmarks):
    t1_mouse_interact = threading.Thread(target=mouse_interact, args=(handLandmarks,))
    t2_mouse_movement = threading.Thread(target=move_mouse, args=(x, y, frame))

    t1_mouse_interact.start()
    t2_mouse_movement.start()

    t1_mouse_interact.join()
    t2_mouse_movement.join()