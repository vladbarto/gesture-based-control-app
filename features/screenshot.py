import subprocess

import cv2

from utils.hand_constants import INDEX_FINGER_TIP, THUMB_TIP
from utils.common import euclidean_distance, BGR_GREEN

def trigger_screenshot():
    # subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 20 using {command down, shift down, control down}'])
    subprocess.run(["screencapture", "screenshot.png"])
    print("[DEBUG] Screenshot triggered")

def do_screenshot(left_hand_landmarks, right_hand_landmarks, frame):
    # Extract points
    point_stg_sus = (left_hand_landmarks[INDEX_FINGER_TIP][0], left_hand_landmarks[INDEX_FINGER_TIP][1])
    point_stg_jos = (left_hand_landmarks[THUMB_TIP][0], left_hand_landmarks[THUMB_TIP][1])

    point_drt_sus = (right_hand_landmarks[INDEX_FINGER_TIP][0], right_hand_landmarks[INDEX_FINGER_TIP][1])
    point_drt_jos = (right_hand_landmarks[THUMB_TIP][0], right_hand_landmarks[THUMB_TIP][1])

    # Compute distances
    dist_sus = euclidean_distance(point_stg_sus, point_drt_sus)
    dist_jos = euclidean_distance(point_stg_jos, point_drt_jos)
    dist_stg = euclidean_distance(point_stg_sus, point_stg_jos)
    dist_drt = euclidean_distance(point_drt_sus, point_drt_jos)

    point_stg_sus = (
        int(left_hand_landmarks[INDEX_FINGER_TIP][0]),
        int(left_hand_landmarks[INDEX_FINGER_TIP][1])
    )
    point_stg_jos = (
        int(left_hand_landmarks[THUMB_TIP][0]),
        int(left_hand_landmarks[THUMB_TIP][1])
    )

    point_drt_sus = (
        int(right_hand_landmarks[INDEX_FINGER_TIP][0]),
        int(right_hand_landmarks[INDEX_FINGER_TIP][1])
    )
    point_drt_jos = (
        int(right_hand_landmarks[THUMB_TIP][0]),
        int(right_hand_landmarks[THUMB_TIP][1])
    )

    # Debugging: print distances
    print(f"dist_sus: {dist_sus}, dist_jos: {dist_jos}, dist_stg: {dist_stg}, dist_drt: {dist_drt}")

    # Check conditions for screenshot
    if 0.17 < dist_sus < 0.23 and 0.17 < dist_jos < 0.23 \
            and 0.10 < dist_stg < 0.15 and 0.10 < dist_drt < 0.15:
        print("DA - Screenshot Triggered")
        trigger_screenshot()

        # Draw green lines when conditions are met
        color = (0, 255, 0)  # Green color in BGR
    else:
        print("Distances not correct - Red Lines")
        # Draw red lines when conditions are not met
        color = (0, 0, 255)  # Red color in BGR
        # Draw lines between corresponding points
        cv2.line(img=frame, pt1=point_stg_sus, pt2=point_stg_jos, color=color, thickness=3)  # Left hand
        cv2.line(img=frame, pt1=point_drt_sus, pt2=point_drt_jos, color=color, thickness=3)  # Right hand


