from utils import landmark_utils, algo_utils, utils
import numpy as np
import cv2

extreme_points = utils.load_indexes_from_csv("./data/extreme_points.csv")

point_collector = []
angle_collector = []

# Define calibration text
text = 'DRAW CIRCLES'
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 5
font_thickness = 10
font_color = (0, 0, 0)  # BGR color format

for i in range(150):
    landmarks, image = landmark_utils.get_points()

    ih, iw, _ = image.shape

    # Get the size of the text
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)

    # Calculate the position to center the text
    text_x = (image.shape[1] - text_width) // 2
    text_y = (image.shape[0] + text_height) // 2

    position = (text_x, text_y)

    # Use putText() to draw the text on the image
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_color, font_thickness, lineType=cv2.LINE_AA)

    if landmarks:
        x_angle, y_angle, orthag_vect = algo_utils.run_face_orthag(landmarks, extreme_points)
        angle_collector.append((x_angle, y_angle))

        center = algo_utils.find_average_anchor_point([element for element in landmarks])
        center_image = (int(center[0]*iw), int(center[1]*ih))
        end_image = (int(center_image[0]+orthag_vect[0]*500), int(center_image[1]+orthag_vect[1]*500))
        cv2.line(image, center_image, end_image, (255, 0, 0), 2)
        point_collector.append(end_image)

        for idx, landmark in enumerate(landmarks):
            cx, cy = int(landmark.x * iw), int(landmark.y * ih)
            cv2.circle(image, (cx, cy), 2, (0, 0, 0), -1)

        for point in point_collector:
            cv2.circle(image, point, 5, (255, 255, 255), -1)

        

    cv2.imshow('Face Tracking', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()


def get_n_max_min_point_indices(points, n):
    sorted_by_x_indices = sorted(range(len(points)), key=lambda i: points[i][0])
    sorted_by_y_indices = sorted(range(len(points)), key=lambda i: points[i][1])

    max_x_indices = sorted_by_x_indices[-n:]
    min_x_indices = sorted_by_x_indices[:n]

    max_y_indices = sorted_by_y_indices[-n:]
    min_y_indices = sorted_by_y_indices[:n]

    return max_x_indices, min_x_indices, max_y_indices, min_y_indices

max_x, min_x, max_y, min_y = get_n_max_min_point_indices(point_collector, 10)


x_angles, y_angles = zip(*angle_collector)

max_x_angles = [x_angles[idx] for idx in max_x]
min_x_angles = [x_angles[idx] for idx in min_x]
max_y_angles = [y_angles[idx] for idx in max_y]
min_y_angles = [y_angles[idx] for idx in min_y]

x_range = np.abs(np.mean(max_x_angles) - np.mean(min_x_angles))
y_range = np.abs(np.mean(max_y_angles) - np.mean(min_y_angles))

x_center = np.mean(max_x_angles+min_x_angles) 
y_center = np.mean(max_y_angles+min_y_angles)

utils.save_to_json([x_center, y_center, x_range, y_range], "./data/calibration_data.json")






