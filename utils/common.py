import platform, cv2, subprocess, time
import mediapipe as mp
from utils import hand_constants

DEBUG_MODE = True
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)