import cv2
import csv
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np

from pynput.mouse import Controller
mouse = Controller()

# mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh

# Initialize Mediapipe Face Detection and Face Mesh
# face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.2, min_tracking_confidence=0.2)

cap = cv2.VideoCapture(0)

# Initialize plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()

ax.set_xlim(0, 100)  # Set x-axis limits
ax.set_ylim(0, 3.1415)    # Set y-axis limits

# Generate random data for initial plot
x_plot_data = np.arange(0, 100)
y_data = np.zeros(100)
x_data = np.zeros(100)

line_x, = ax.plot(x_plot_data, x_data)
line_y, = ax.plot(x_plot_data, y_data)

previous_sample = [0, 0]


def find_average_anchor_point(anchor_points):
	average_point = np.zeros(3)
	for idx, landmark in enumerate(anchor_points):

		average_point[0] += landmark.x
		average_point[1] += landmark.y
		average_point[2] += landmark.z

	average_point /= len(anchor_points)
	return average_point


def find_unit(vect):
	return vect / (np.linalg.norm(vect) + 0.000001)

def find_orthoginal(point1, point2, point3):
	difference_vector_1 = point1-point2
	difference_vector_2 = point1-point3

	orthoginal_vect = np.cross(difference_vector_1, difference_vector_2)

	return find_unit(orthoginal_vect)

def find_orthoginal_vect(v1, v2):
	orthoginal_vect = np.cross(v1, v2)

	return find_unit(orthoginal_vect)

def find_angle(v1, v2):
	v1_u = find_unit(v1)
	v2_u = find_unit(v2)

	return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def load_indexes_from_csv(file_path):
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    
    header = data[0]
    indexes = list(map(list, zip(*[[int(value) for value in row] for row in data[1:]])))
    
    return {
        header[0]: indexes[0],
        header[1]: indexes[1],
        header[2]: indexes[2],
        header[3]: indexes[3]
    }

extreme_points = load_indexes_from_csv("extreme_points.csv")

def move_mouse(angle_x, angle_y, speed=50, threshold=0.1):

	if np.sqrt(angle_x**2 + angle_y**2) > threshold:
		y_offset = angle_y
		x_offset = angle_x
		current_x, current_y = mouse.position
		new_x = current_x - x_offset*speed
		new_y = current_y - y_offset*speed
		mouse.position = (new_x, new_y)

# def move_mouse(angle, speed):
#     mouse = Controller()
#     radian_angle = math.radians(angle)
#     x_offset = speed * math.cos(radian_angle)
#     y_offset = speed * math.sin(radian_angle)
#     current_x, current_y = mouse.position
#     new_x = current_x + x_offset
#     new_y = current_y + y_offset
#     mouse.position = (new_x, new_y)

while True:

	ret, image = cap.read()
	image = cv2.flip(image, 1)
	image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# Detect facial landmarks
	results_mesh = face_mesh.process(image_rgb)
	ih, iw, _ = image.shape
	if results_mesh.multi_face_landmarks:

		for face_landmarks in results_mesh.multi_face_landmarks:


			#selected_landmarks = [60, 99, 97, 290, 328, 326, 2, 1, 4, 5, 98, 327, 51, 281]
			#anchor_points = [face_landmarks.landmark[i] for i in selected_landmarks]

			nose_idx = [60, 99, 97, 290, 328, 326, 2, 1, 4, 5, 98, 327, 51, 281]
			nose_idx = [97, 2, 326, 167, 164, 393]

			right_eye_idx = [24, 23, 22, 228, 229, 231]
			left_eye_idx = [252, 253, 254, 450, 449, 448]

			nose_landmarks = [face_landmarks.landmark[i] for i in nose_idx]
			right_eye_landmarks = [face_landmarks.landmark[i] for i in right_eye_idx]
			left_eye_landmarks = [face_landmarks.landmark[i] for i in left_eye_idx]

			nose  = find_average_anchor_point(nose_landmarks)
			right_eye = find_average_anchor_point(right_eye_landmarks)
			left_eye = find_average_anchor_point(left_eye_landmarks)

			x_min_avg = find_average_anchor_point([face_landmarks.landmark[i] for i in extreme_points["x_min"]])
			x_max_avg = find_average_anchor_point([face_landmarks.landmark[i] for i in extreme_points["x_max"]])
			y_min_avg = find_average_anchor_point([face_landmarks.landmark[i] for i in extreme_points["y_min"]])
			y_max_avg = find_average_anchor_point([face_landmarks.landmark[i] for i in extreme_points["y_max"]])

			min_point_x = (int(x_min_avg[0] * iw), int(x_min_avg[1] * ih))
			max_point_x = (int(x_max_avg[0] * iw), int(x_max_avg[1] * ih))
			#cv2.line(image, min_point_x, max_point_x, (255, 0, 0), 2)

			min_point_y = (int(y_min_avg[0] * iw), int(y_min_avg[1] * ih))
			max_point_y = (int(y_max_avg[0] * iw), int(y_max_avg[1] * ih))
			#cv2.line(image, min_point_y, max_point_y, (255, 0, 0), 2)

			orthag_vect = find_orthoginal_vect(y_min_avg-y_max_avg, x_min_avg-x_max_avg)*500

			nose_point = (int(nose[0] * iw), int(nose[1] * ih))
			end_point = (int(nose_point[0]+orthag_vect[0]), int(nose_point[1]+orthag_vect[1]))

			cv2.line(image, nose_point, end_point, (255, 0, 0), 2)

			x_angle = find_angle(orthag_vect, [1, 0, 0])
			y_angle = find_angle(orthag_vect, [0, 1, 0])


			# cx, cy = int(right_eye[0] * iw), int(right_eye[1] * ih)
			# cv2.circle(image, (cx, cy), 2, (255, 0, 0), -1)

			# cx, cy = int(left_eye[0] * iw), int(left_eye[1] * ih)
			# cv2.circle(image, (cx, cy), 2, (255, 0, 0), -1)

			# cx, cy = int(nose[0] * iw), int(nose[1] * ih)
			# cv2.circle(image, (cx, cy), 2, (255, 0, 0), -1)

			# orthag_vect = find_orthoginal(nose, left_eye, right_eye)*500


			# nose_point = (int(nose[0] * iw), int(nose[1] * ih))
			# end_point = (int(nose_point[0]+orthag_vect[0]), int(nose_point[1]+orthag_vect[1]))

			# cv2.line(image, nose_point, end_point, (0, 0, 255), 2)


			anchor_points = face_landmarks.landmark #[face_landmarks.landmark[idx] for idx in extreme_points["x_min"]]
			for idx, landmark in enumerate(anchor_points):
				cx, cy = int(landmark.x * iw), int(landmark.y * ih)
				cv2.circle(image, (cx, cy), 2, (0, 0, 0), -1)


			move_mouse(x_angle-1.5, y_angle-1.5)



	cv2.imshow('Face Tracking', image)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	delta_position = [np.clip(previous_sample[0] - x_angle, -1.0, 1.0), 
					  np.clip(previous_sample[1] - y_angle, -1.0, 1.0)]
	previous_sample = [x_angle, y_angle]

	# mouse_coords = list(pyautogui.position())

	# if np.abs(delta_position[0]) > 0.25:
	# 	mouse_coords[0] += delta_position[0]*500

	# if np.abs(delta_position[1]) > 0.3:
	# 	mouse_coords[1] += delta_position[1]*500

	# pyautogui.moveTo(mouse_coords[0], mouse_coords[1])

	#print(mouse_coords)

	# Update plot data
	y_data = np.roll(y_data, -1)
	y_data[-1] = y_angle
	line_y.set_ydata(y_data)

	x_data = np.roll(x_data, -1)
	x_data[-1] = x_angle
	line_x.set_ydata(x_data)



	# Redraw the plot
	fig.canvas.draw()
	fig.canvas.flush_events()



cap.release()
cv2.destroyAllWindows()

# Turn off interactive mode when the script ends
plt.ioff()
