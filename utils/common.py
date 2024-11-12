import platform, cv2, subprocess, time
import mediapipe as mp
from utils import hand_constants

DEBUG_MODE = False
ENABLED_SCREEN = True
ENABLED_VOLUME_FEATURE = False
ENABLED_SHUTDOWN_FEATURE = True

RGB_RED = (255, 0, 0)
RGB_GREEN = (0, 255, 0)
RGB_BLUE = (0, 0, 255)
RGB_YELLOW = (255, 255, 0)

BGR_RED = (0, 0, 255)
BGR_GREEN = (0, 255, 0)
BGR_BLUE = (255, 0, 0)