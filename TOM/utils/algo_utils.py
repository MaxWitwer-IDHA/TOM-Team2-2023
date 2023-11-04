import numpy as np

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

def run_face_orthag(landmarks, anchor_points):
	x_min_avg = find_average_anchor_point([landmarks[i] for i in anchor_points["x_min"]])
	x_max_avg = find_average_anchor_point([landmarks[i] for i in anchor_points["x_max"]])
	y_min_avg = find_average_anchor_point([landmarks[i] for i in anchor_points["y_min"]])
	y_max_avg = find_average_anchor_point([landmarks[i] for i in anchor_points["y_max"]])

	x_dist_vect = x_min_avg-x_max_avg
	y_dist_vect = y_min_avg-y_max_avg

	orthag_vect = find_orthoginal_vect(y_dist_vect, x_dist_vect)

	#anchored_planar_vector_x = find_unit([x_dist_vect[0], x_dist_vect[1], 0])
	#anchored_planar_vector_y = find_unit([y_dist_vect[0], y_dist_vect[1], 0])

	#x_angle = find_angle(orthag_vect, anchored_planar_vector_x)
	#y_angle = find_angle(orthag_vect, anchored_planar_vector_y)
	x_angle = find_angle(orthag_vect, [1, 0, 0])
	y_angle = find_angle(orthag_vect, [0, 1, 0])

	return x_angle, y_angle, orthag_vect

