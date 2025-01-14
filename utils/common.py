import math

DEBUG_MODE = True
ENABLED_SCREEN = False
ENABLED_VOLUME_FEATURE = False
ENABLED_SHUTDOWN_FEATURE = True
ENABLED_MOUSE_MOVE_FEATURE = False
ENABLED_SCREENSHOT_FEATURE = False
ENABLED_ZOOM_FEATURE = True
ENABLED_PLAY_PAUSE_FEATURE = True

RGB_RED = (255, 0, 0)
RGB_GREEN = (0, 255, 0)
RGB_BLUE = (0, 0, 255)
RGB_YELLOW = (255, 255, 0)

BGR_RED = (0, 0, 255)
BGR_GREEN = (0, 255, 0)
BGR_BLUE = (255, 0, 0)
BGR_YELLOW = (33, 222, 255)

def euclidean_distance(point1, point2):
    (x1, y1), (x2, y2) = point1, point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)