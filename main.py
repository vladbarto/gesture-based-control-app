import cv2, time, mediapipe as mp

from features.shutdown import do_shutdown
from features.volume import pinch_volume
from utils.common import (ENABLED_VOLUME_FEATURE,
                          DEBUG_MODE,
                          ENABLED_SCREEN,
                          ENABLED_SHUTDOWN_FEATURE)

finger_count = 0

def start_system():
    get_out = False
    webcam = cv2.VideoCapture(0)
    my_hands = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    x1, y1, x2, y2, old_dist = 0, 0, 0, 0, 0

    last_volume_change_time = time.time()  # Track the last volume adjustment time

    while not get_out:
        _, frame = webcam.read()
        frame_height, frame_width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = my_hands.process(rgb_image)

        hands = output.multi_hand_landmarks
        handedness = output.multi_handedness  # Get the handedness (left/right) info

        if hands and handedness:
            for (hand, hand_info) in zip(hands, handedness):

                hand_label = hand_info.classification[0].label  # "Left" or "Right"
                if DEBUG_MODE: print(f'[DEBUG] Hand detected: {hand_label}')

                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                handLandmarks = []

                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    handLandmarks.append([landmark.x, landmark.y])

                    if ENABLED_VOLUME_FEATURE:
                        if "Right" == hand_label:
                            last_volume_change_time, old_dist, x1, x2, y1, y2 = pinch_volume(frame, id, x, y, x1, x2, y1, y2, old_dist, last_volume_change_time)

                """
                handLandmarks[a][b]
                - a = accesezi una dintre cele 21 de constante definite in utils.hand_constants
                    deci poti avea acces la diferite componente din aratator, deget mare sau orice alt deget, + incheietura
                - b = pozitionarea componentei "a" in fereastra
                    0 = x
                    1 = y 
                """
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

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
