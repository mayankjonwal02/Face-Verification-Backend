import cv2
import mediapipe as mp
import numpy as np


def is_face_front_center(image_path):
    # Read the image
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to read image at img")
        return False

    # Convert the BGR image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and find faces
    results = face_mesh.process(rgb_image)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Get specific landmarks
            nose_tip = face_landmarks.landmark[4]
            left_eye = face_landmarks.landmark[33]
            right_eye = face_landmarks.landmark[263]
            left_mouth = face_landmarks.landmark[61]
            right_mouth = face_landmarks.landmark[291]

            # Calculate face direction
            horizontal_direction = ""
            vertical_direction = ""
            
            # Check horizontal direction
            eye_distance = right_eye.x - left_eye.x
            nose_to_left = nose_tip.x - left_eye.x
            nose_to_right = right_eye.x - nose_tip.x
            
            if nose_to_left < 0.45 * eye_distance:
                horizontal_direction = "Left"
            elif nose_to_right < 0.45 * eye_distance:
                horizontal_direction = "Right"
            else:
                horizontal_direction = "Front"

            # Check vertical direction
            eye_y = (left_eye.y + right_eye.y) / 2
            mouth_y = (left_mouth.y + right_mouth.y) / 2
            vertical_range = mouth_y - eye_y
            
            if nose_tip.y < eye_y + 0.15 * vertical_range:
                vertical_direction = "Up"
            elif nose_tip.y > mouth_y - 0.15 * vertical_range:
                vertical_direction = "Down"
            else:
                vertical_direction = "Center"

            face_direction = f"{horizontal_direction} {vertical_direction}"
            print(face_direction)

            # Return True if face direction is "Front Center", False otherwise
            return face_direction == "Front Center"

    # If no face is detected, return False
    return False

        