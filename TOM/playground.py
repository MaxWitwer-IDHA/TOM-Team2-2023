from utils import landmark_utils, algo_utils, utils
import time
import numpy as np

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

print(time.time()-glob_start)
print(len(collector))
print(1/np.mean(collector))