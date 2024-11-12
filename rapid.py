# def change_volume(direction, delta_volume):
#     # Adjust volume using osascript (macOS specific)
#     if platform.system() == 'Darwin':
#         if delta_volume > 0:#direction == 'up':
#             osascript_command = f'osascript -e "set volume output volume ((output volume of (get volume settings)) + {delta_volume})"'
#         else:
#             delta_volume *= -1
#             osascript_command = f'osascript -e "set volume output volume ((output volume of (get volume settings)) - {delta_volume})"'
#
#         if DEBUG_MODE: print(osascript_command)
#         subprocess.run(osascript_command, shell=True)
#     else:
#         print("Volume adjustment is only supported on macOS.")
#
#
# def pinch_volume():
#     x1, y1, x2, y2 = 0, 0, 0, 0
#     last_volume_change_time = time.time()  # Track the last volume adjustment time
#     volume_change_interval = 0.2  # Set cooldown period (in seconds) between adjustments
#
#     webcam = cv2.VideoCapture(0)
#     my_hands = mp.solutions.hands.Hands()
#     drawing_utils = mp.solutions.drawing_utils
#
#     old_dist = curr_dist = 0
#
#     while True:
#         _, frame = webcam.read()
#         frame_height, frame_width, _ = frame.shape
#         frame = cv2.flip(frame, 1)
#         rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         output = my_hands.process(rgb_image)
#         hands = output.multi_hand_landmarks
#
#         if hands:
#             for hand in hands:
#                 drawing_utils.draw_landmarks(frame, hand)
#                 landmarks = hand.landmark
#                 for id, landmark in enumerate(landmarks):
#                     x = int(landmark.x * frame_width)
#                     y = int(landmark.y * frame_height)
#
#                     if INDEX_FINGER_TIP == id:
#                         cv2.circle(img=frame, center=(x, y), radius=8, color=(0, 255, 0), thickness=3)
#                         x1, y1 = x, y
#                     if THUMB_TIP == id:
#                         cv2.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0), thickness=3)
#                         x2, y2 = x, y
#
#                     curr_dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 // 4
#                     cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
#
#                     current_time = time.time()
#                     delta = curr_dist - old_dist
#                     if current_time - last_volume_change_time >= volume_change_interval and delta != 0:
#                         change_volume('up', delta)
#                         # if curr_dist > 50:
#                         #     change_volume('up', delta)
#                         # else:
#                         #     change_volume('down', delta)
#                         last_volume_change_time = current_time  # Update last change time
#                         old_dist = curr_dist  # updates for a new loop
#
#         cv2.imshow('Video', frame)
#         key = cv2.waitKey(1)
#         if 27 == key:
#             break
#
#
#     # out of while loop
#     webcam.release()
#     cv2.destroyAllWindows()