from utils import landmark_utils, algo_utils, utils
from pynput.mouse import Button
# from mouse_utils import stream_helper
import time
import numpy as np



hold_counter = 0
threshold = 35  # Set your desired threshold here (number of time steps)

extreme_points = utils.load_indexes_from_csv("./data/extreme_points.csv")

calibration_values = utils.read_from_json("./data/calibration_data.json")
x_center = calibration_values[0]
y_center = calibration_values[1]
x_range = calibration_values[2]
y_range = calibration_values[3]

collector = []
glob_start = time.time()
while True:
    start = time.time()
    landmarks, _ = landmark_utils.get_points()

    if landmarks:
        x_angle, y_angle, _ = algo_utils.run_face_orthag(landmarks, extreme_points)

        utils.move_mouse((x_angle-x_center)/x_range, (y_angle-y_center)/y_range)

    end = time.time()



    if landmarks:
        collector.append(end-start)

    # bluetooth_dump = stream.pull_data()
    # button_state = bluetooth_dump[-1]

    # if button_state == 1:  # Assuming 1 represents a button press
    #     mouse.press(Button.left)  # Press the left mouse button
    #     hold_counter += 1
    # else:
    #     mouse.release(Button.left)  # Release the left mouse button
    #     if hold_counter >= threshold:
    #         mouse.click(Button.right, 1)  # Simulate a right mouse click
    #     hold_counter = 0  # Reset the counter

print(time.time()-glob_start)
print(len(collector))
print(1/np.mean(collector))