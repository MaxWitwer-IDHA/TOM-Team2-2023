import cv2
import mediapipe as mp

# mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh

# Initialize Mediapipe Face Detection and Face Mesh
# face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.2, min_tracking_confidence=0.2)

cap = cv2.VideoCapture(0)

def get_points():
	ret, image = cap.read()
	image = cv2.flip(image, 1)
	image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	results_mesh = face_mesh.process(image_rgb)

	if results_mesh.multi_face_landmarks:
		return results_mesh.multi_face_landmarks[0].landmark, image

	else:
		return None, image
