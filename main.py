import cv2, time, mediapipe as mp
from features.volume import pinch_volume
DEBUG_MODE = True

def start_system():
    webcam = cv2.VideoCapture(0)
    my_hands = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    x1, y1, x2, y2, old_dist = 0, 0, 0, 0, 0

    last_volume_change_time = time.time()  # Track the last volume adjustment time

    while True:
        _, frame = webcam.read()
        frame_height, frame_width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = my_hands.process(rgb_image)
        hands = output.multi_hand_landmarks

        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)

                    last_volume_change_time, old_dist, x1, x2, y1, y2 = pinch_volume(frame, id, x, y, x1, x2, y1, y2, old_dist, last_volume_change_time)

        cv2.imshow('Video', frame)
        key = cv2.waitKey(1)
        if 27 == key:
            break

    # out of while loop
    webcam.release()
    cv2.destroyAllWindows()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')
    start_system()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
