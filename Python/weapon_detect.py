# weapon_detect.py (Updated)
import os
import cv2
import numpy as np
from ultralytics import YOLO
from joblib import load

YOLO_MODEL_PATH = 'models/best (5)Gun.pt'
SVM_MODEL_PATH = 'models/svm_model.joblib'

model = YOLO(YOLO_MODEL_PATH)
svm_clf = load(SVM_MODEL_PATH)

def extract_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (64, 64))
    feature_vector = resized.flatten()
    return feature_vector.reshape(1, -1)

def run_weapon_detection(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0]
            label = results.names[int(box.cls[0])]

            if confidence >= 0.35:
                cropped_img = frame[y1:y2, x1:x2]
                if cropped_img.size != 0:
                    features = extract_features(cropped_img)
                    prediction = svm_clf.predict(features)
                    svm_label = "Weapon" if prediction[0] == 1 else "Safe"
                    color = (0, 0, 255) if svm_label == "Weapon" else (0, 255, 0)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"{label} {confidence:.2f} | {svm_label}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        out.write(frame)

    cap.release()
    out.release()
