# reference: https://github.com/m3mentomor1/Raised-Finger-Counter-With-MediaPipe/blob/main/finger_counter.py

from utils.common import DEBUG_MODE
from utils.hand_constants import MIDDLE_FINGER_TIP, MIDDLE_FINGER_PIP, THUMB_TIP, THUMB_MCP, INDEX_FINGER_TIP, \
    INDEX_FINGER_PIP, RING_FINGER_TIP, RING_FINGER_PIP, PINKY_FINGER_TIP, PINKY_FINGER_PIP

"""
handLandmarks[a][b]
- a = accesezi una dintre cele 21 de constante definite in utils.hand_constants
   deci poti avea acces la diferite componente din aratator, deget mare sau orice alt deget, + incheietura
- b = pozitionarea componentei "a" in fereastra
   0 = x
   1 = y
"""

def all_other_fingers_closed(handLandmarks):
    if (handLandmarks[THUMB_TIP][0] > handLandmarks[THUMB_MCP][0] and
        handLandmarks[INDEX_FINGER_TIP][1] > handLandmarks[INDEX_FINGER_PIP][1] and
        handLandmarks[RING_FINGER_TIP][1] > handLandmarks[RING_FINGER_PIP][1] and
        handLandmarks[PINKY_FINGER_TIP][1] > handLandmarks[PINKY_FINGER_PIP][1]):

        return True

    return False


def do_shutdown(handLandmarks):
    if handLandmarks[MIDDLE_FINGER_TIP][1] < handLandmarks[MIDDLE_FINGER_PIP][1]:  # Left & Right Middle finger
        if all_other_fingers_closed(handLandmarks):
            if DEBUG_MODE: print("[DEBUG] middle finger, whatever side")
            return True

    return False
