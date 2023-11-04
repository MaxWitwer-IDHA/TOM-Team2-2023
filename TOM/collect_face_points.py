import cv2
import csv
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np

# mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh

# Initialize Mediapipe Face Detection and Face Mesh
# face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.2, min_tracking_confidence=0.2)


# Read in the image
image_path = 'sample.jpg'  # Replace with the actual path of your image
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

results_mesh = face_mesh.process(image_rgb)

landmarks = []
for landmark_elements in results_mesh.multi_face_landmarks:
	for point in landmark_elements.landmark:
		landmarks.append((point.x, point.y, point.z))

def get_extreme_points(point_list, n):
    # Extract x and y coordinates
    x_coords = [point[0] for point in point_list]
    y_coords = [point[1] for point in point_list]
    
    # Get the indexes of the n highest and lowest points in x and y
    lowest_x = sorted(range(len(x_coords)), key=lambda i: x_coords[i])[-n:]
    highest_x = sorted(range(len(x_coords)), key=lambda i: x_coords[i])[:n]
    
    lowest_y = sorted(range(len(y_coords)), key=lambda i: y_coords[i])[-n:]
    highest_y = sorted(range(len(y_coords)), key=lambda i: y_coords[i])[:n]
    
    return highest_x, lowest_x, highest_y, lowest_y

def save_indexes_to_csv(indexes, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['x_max', 'x_min', 'y_max', 'y_min']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for entry in zip(*indexes):
            writer.writerow({'x_max': entry[0], 'x_min': entry[1], 'y_max': entry[2], 'y_min': entry[3]})

#save_to_csv(get_extreme_points(landmarks, 50), "extreme_points.csv")
save_indexes_to_csv(get_extreme_points(landmarks, 100), "extreme_points.csv")




