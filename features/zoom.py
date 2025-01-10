import subprocess

from utils.common import DEBUG_MODE
from utils.hand_constants import *

def app_zoom_in():
    subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 24 using {command down}'])

def app_zoom_out():
    subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 27 using {command down}'])

def thumb_ring_pinky_fingers_closed(handLandmarks):
    if (handLandmarks[THUMB_TIP][0] > handLandmarks[THUMB_MCP][0] and
        handLandmarks[RING_FINGER_TIP][1] > handLandmarks[RING_FINGER_PIP][1] and
        handLandmarks[PINKY_FINGER_TIP][1] > handLandmarks[PINKY_FINGER_PIP][1]):

        return True

    return False

def do_zoom(left_hand_landmarks, right_hand_landmarks, frame):
#     Zoom in:
    if right_hand_landmarks[INDEX_FINGER_TIP][1] < right_hand_landmarks[INDEX_FINGER_PIP][1] \
            and right_hand_landmarks[MIDDLE_FINGER_TIP][1] < right_hand_landmarks[MIDDLE_FINGER_PIP][1]:  #  index and middle finger together raised
        if thumb_ring_pinky_fingers_closed(right_hand_landmarks):
            if DEBUG_MODE: print("[DEBUG] zoom in")
            app_zoom_in()

#     Zoom out:
    if left_hand_landmarks[INDEX_FINGER_TIP][1] < left_hand_landmarks[INDEX_FINGER_PIP][1] \
            and left_hand_landmarks[MIDDLE_FINGER_TIP][1] < left_hand_landmarks[MIDDLE_FINGER_PIP][1]:  #  index and middle finger together raised
        if thumb_ring_pinky_fingers_closed(left_hand_landmarks):
            if DEBUG_MODE: print("[DEBUG] zoom out")
            app_zoom_out()
