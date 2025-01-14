import subprocess

from utils.hand_constants import THUMB_TIP, THUMB_MCP, INDEX_FINGER_TIP, INDEX_FINGER_PIP, RING_FINGER_TIP, \
    PINKY_FINGER_TIP, RING_FINGER_PIP, PINKY_FINGER_PIP, MIDDLE_FINGER_TIP, MIDDLE_FINGER_PIP


import time
from AppKit import NSEvent, NSSystemDefined
from Quartz import CGEventPost, kCGHIDEventTap

def press_media_key(key_code):
    """Press a media key using pyobjc."""
    event = NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
        NSSystemDefined,  # Event type
        (0, 0),           # Location
        0xA00,            # Modifier flags
        time.time(),      # Timestamp
        0,                # Window number
        None,             # Context
        8,                # Subtype for media keys
        (key_code << 16) | (0xA << 8),  # Encoded key code and flags
        -1                # Data2 (unused)
    )
    CGEventPost(kCGHIDEventTap, event.CGEvent())  # Post the event to the system

# Constants for media key codes
PLAY_PAUSE_KEY = 16

def press_play_pause():
    """Press the play/pause key."""
    press_media_key(PLAY_PAUSE_KEY)


def hand_fisted(handLandmarks) -> bool:
    if handLandmarks[THUMB_TIP][0] > handLandmarks[THUMB_MCP][0] and \
         handLandmarks[INDEX_FINGER_TIP][1] > handLandmarks[INDEX_FINGER_PIP][1] and \
         handLandmarks[MIDDLE_FINGER_TIP][1] > handLandmarks[MIDDLE_FINGER_PIP][1] and \
         handLandmarks[RING_FINGER_TIP][1] > handLandmarks[RING_FINGER_PIP][1] and \
         handLandmarks[PINKY_FINGER_TIP][1] > handLandmarks[PINKY_FINGER_PIP][1]:

        return True
    return False

def do_play_pause(right_hand_landmarks):
    if hand_fisted(right_hand_landmarks):
        print("ACTIVATED")
        press_play_pause()
        time.sleep(1)
