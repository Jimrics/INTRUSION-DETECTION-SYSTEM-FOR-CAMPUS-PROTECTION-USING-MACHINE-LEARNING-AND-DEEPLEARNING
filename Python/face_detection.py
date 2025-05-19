import face_recognition
import cv2
import os
import numpy as np
import time
import subprocess
import sys


# Arguments from Flask: input video, output folder, authorized folder
input_video = sys.argv[1]
output_folder = sys.argv[2]
authorized_faces_folder = r"C:\Users\JIM\My Drive\MCA\Semester 4 Project Work\Tresspassing\Face\detected_faces2"  # pre-defined or manually uploaded

print(f"[INFO] Input Video: {input_video}")
print(f"[INFO] Output Folder: {output_folder}")

# Create folders
os.makedirs(authorized_faces_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Output paths
filename = os.path.basename(input_video)
raw_output_path = os.path.join(output_folder, f"detected_{filename}")
converted_output_path = os.path.join(output_folder, f"converted_{filename}")

# Load authorized faces
known_face_encodings = []
known_face_names = []

for filename in os.listdir(authorized_faces_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        path = os.path.join(authorized_faces_folder, filename)
        try:
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])
        except Exception:
            continue

if not known_face_encodings:
    raise ValueError("No valid faces found in authorized faces folder")

# Open video
video_capture = cv2.VideoCapture(input_video)
if not video_capture.isOpened():
    raise ValueError(f"Could not open video file: {input_video}")

# Get video properties
fps = video_capture.get(cv2.CAP_PROP_FPS)
width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Write output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(raw_output_path, fourcc, fps, (width, height))

last_beep_time = 0
cooldown = 2  # seconds

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    unauthorized_detected = False

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.45)
        name = "Unauthorized"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        else:
            unauthorized_detected = True

        face_names.append(name)

    # Optional: beep on unauthorized (disabled in backend version)
    # if unauthorized_detected and (time.time() - last_beep_time > cooldown):
    #     winsound.Beep(1000, 500)
    #     last_beep_time = time.time()

    # Draw rectangles
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        color = (0, 255, 0) if name != "Unauthorized" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

    out.write(frame)

video_capture.release()
out.release()

# Convert to H.264 + MP3 (MP4)
subprocess.run([
    "ffmpeg", "-y", "-i", raw_output_path,
    "-c:v", "libx264", "-c:a", "libmp3lame",
    "-preset", "fast", "-movflags", "+faststart",
    converted_output_path
])
