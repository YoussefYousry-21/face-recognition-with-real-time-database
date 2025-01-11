import cv2
import face_recognition
import pickle
import os

# Define the folder to save images locally
local_image_dir = "local_images"
os.makedirs(local_image_dir, exist_ok=True)

# Importing student images
folder = "Images"
path_list = os.listdir(folder)
image_list = []
student_ids = []

for path in path_list:
    image = cv2.imread(os.path.join(folder, path))
    image_list.append(image)
    sid = path.split(".")[0]
    student_ids.append(sid)

    # Save the image locally
    local_filename = os.path.join(local_image_dir, path)
    cv2.imwrite(local_filename, image)

print(len(image_list))


def findEncoding(imgList):
    encode_list = []
    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if encode:  # Check if encoding was found
            encode_list.append(encode[0])  # Take the first encoding
        else:
            print("No face found in image.")
    return encode_list
    
print("Encoding Started.....")
encodeListKnown = findEncoding(image_list)
encodeListKnownWithIds = [encodeListKnown, student_ids]
print("Encoding Completed.....")

# Save the encodings to a file
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")