import platform, subprocess, cv2, time
from utils.hand_constants import THUMB_TIP, INDEX_FINGER_TIP
from utils.common import DEBUG_MODE
from utils.common import BGR_RED, BGR_GREEN, BGR_BLUE

def change_volume(delta_volume):
    # Adjust volume using osascript (macOS specific)
    if platform.system() == 'Darwin':
        if delta_volume > 0:
            osascript_command = f'osascript -e "set volume output volume ((output volume of (get volume settings)) + {delta_volume})"'
        else:
            delta_volume *= -1
            osascript_command = f'osascript -e "set volume output volume ((output volume of (get volume settings)) - {delta_volume})"'

        if DEBUG_MODE: print(f"[DEBUG] {osascript_command}")
        subprocess.run(osascript_command, shell=True)
    else:
        print("Volume adjustment is only supported on macOS.")


def pinch_volume(frame, id, x, y, x1, x2, y1, y2, old_dist, last_volume_change_time):
    volume_change_interval = 0.2  # Set cooldown period (in seconds) between adjustments

    if INDEX_FINGER_TIP == id:
        cv2.circle(img=frame, center=(x, y), radius=8, color=BGR_GREEN, thickness=3)
        x1, y1 = x, y
    if THUMB_TIP == id:
        cv2.circle(img=frame, center=(x, y), radius=10, color=BGR_BLUE, thickness=3)
        x2, y2 = x, y

    curr_dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 // 4
    cv2.line(frame, (x1, y1), (x2, y2), BGR_RED, 2)

    current_time = time.time()
    delta = curr_dist - old_dist
    if current_time - last_volume_change_time >= volume_change_interval and delta != 0:
        change_volume(delta)
        last_volume_change_time = current_time  # Update last change time
        old_dist = curr_dist  # updates for a new loop

    return last_volume_change_time, old_dist, x1, x2, y1, y2