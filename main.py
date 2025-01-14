import cv2, time, mediapipe as mp

from features.play_pause import do_play_pause
from features.shutdown import do_shutdown
from features.volume import pinch_volume
from features.mouse import do_jerry_mouse
from features.screenshot import do_screenshot
from features.zoom import do_zoom
from utils.common import (ENABLED_VOLUME_FEATURE,
                          DEBUG_MODE,
                          ENABLED_SCREEN,
                          ENABLED_SHUTDOWN_FEATURE, ENABLED_MOUSE_MOVE_FEATURE, ENABLED_SCREENSHOT_FEATURE,
                          ENABLED_ZOOM_FEATURE, ENABLED_PLAY_PAUSE_FEATURE)
from utils.hand_constants import PINKY_FINGER_TIP, INDEX_FINGER_TIP, MIDDLE_FINGER_TIP

finger_count = 0

def start_system():
    get_out = False
    webcam = cv2.VideoCapture(0)
    my_hands = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    x1, y1, x2, y2, old_dist = 0, 0, 0, 0, 0

    last_volume_change_time = time.time()  # Track the last volume adjustment time

    while not get_out:
        # time.sleep(1)
        _, frame = webcam.read()
        frame_height, frame_width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = my_hands.process(rgb_image)

        hands = output.multi_hand_landmarks
        handedness = output.multi_handedness  # Get the handedness (left/right) info

        left_hand_landmarks = None
        right_hand_landmarks = None


        if hands and handedness:
            for (hand, hand_info) in zip(hands, handedness):

                hand_label = hand_info.classification[0].label  # "Left" or "Right"
                if DEBUG_MODE: print(f'[DEBUG] Hand detected: {hand_label}')

                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                handLandmarks = []

                x_index, y_index = 0, 0

                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    handLandmarks.append([landmark.x, landmark.y])

                    if ENABLED_VOLUME_FEATURE:
                        if "Left" == hand_label:
                            last_volume_change_time, old_dist, x1, x2, y1, y2 = pinch_volume(frame, id, x, y, x1, x2, y1, y2, old_dist, last_volume_change_time)

                    if ENABLED_MOUSE_MOVE_FEATURE:
                        if "Right" == hand_label:
                            if INDEX_FINGER_TIP == id:
                                x_index, y_index = x, y
                            if INDEX_FINGER_TIP == id:
                                do_jerry_mouse(x_index, y_index, frame, handLandmarks)

                    if ENABLED_PLAY_PAUSE_FEATURE:
                        if "Right" == hand_label:
                            if PINKY_FINGER_TIP == id:
                                do_play_pause(right_hand_landmarks)

                    # Store landmarks based on hand label
                    if hand_label == "Left":
                        left_hand_landmarks = handLandmarks
                    else:
                        right_hand_landmarks = handLandmarks


                if ENABLED_SCREENSHOT_FEATURE:
                    if left_hand_landmarks and right_hand_landmarks:
                        do_screenshot(left_hand_landmarks, right_hand_landmarks, frame)

                if ENABLED_ZOOM_FEATURE:
                    if left_hand_landmarks and right_hand_landmarks:
                        do_zoom(left_hand_landmarks, right_hand_landmarks, frame);

                if ENABLED_SHUTDOWN_FEATURE:
                    get_out = do_shutdown(handLandmarks)



        if ENABLED_SCREEN: cv2.imshow('Video', frame)
        key = cv2.waitKey(1)
        if 27 == key or get_out:
            break

    # out of while loop
    webcam.release()
    cv2.destroyAllWindows()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')
    start_system()

