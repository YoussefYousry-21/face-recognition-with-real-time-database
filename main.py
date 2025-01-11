import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone

# Directory for local images
local_image_dir = "local_images"

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Load the background image
imgBackground = cv2.imread("Resources/background.png")
if imgBackground is None:
    print("Error: Background image not found. Check the 'Resources' folder.")
    exit()

# Load encodings
print("Loading Encode File...")
with open("EncodeFile.p", 'rb') as file:
    encode_data = pickle.load(file)

known_encodings, known_ids = encode_data
print("Encode File Loaded")

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image from webcam.")
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # Scale down for faster processing
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect faces and compute encodings
    detected_faces = face_recognition.face_locations(imgS)
    detected_encodings = face_recognition.face_encodings(imgS, detected_faces)

    # Overlay the camera feed onto the background
    imgBackground[162:162 + 480, 55:55 + 640] = img

    if detected_faces:
        for face_encoding, face_location in zip(detected_encodings, detected_faces):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            # Find the best match
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                # Get the matched ID
                matched_id = known_ids[best_match_index]
                print(f"Face matched with ID: {matched_id}")

                # Draw bounding box around the detected face
                y1, x2, y2, x1 = face_location
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Scale back up
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=1)

                # Load and display the matched face image
                matched_image_path = os.path.join(local_image_dir, f"{matched_id}.jpg")
                if os.path.exists(matched_image_path):
                    img_matched_face = cv2.imread(matched_image_path)
                    img_matched_face_resized = cv2.resize(img_matched_face, (216, 216))
                    imgBackground[175:175 + 216, 909:909 + 216] = img_matched_face_resized
                else:
                    print(f"Image not found for ID: {matched_id}")
            else:
                print("Face detected but no match found.")

    else:
        print("No faces detected.")

    # Display the updated background
    cv2.imshow("Face Recognition System", imgBackground)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
