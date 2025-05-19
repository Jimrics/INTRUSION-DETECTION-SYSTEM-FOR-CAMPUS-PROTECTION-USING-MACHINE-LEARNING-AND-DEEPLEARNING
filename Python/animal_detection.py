import sys
import os
import cv2
from ultralytics import YOLO

model_path = r"C:\Users\JIM\My Drive\MCA\Semester 4 Project Work\Tresspassing\Leopard\best.pt"  
model = YOLO(model_path)

input_path = sys.argv[1]
output_folder = sys.argv[2]
filename = os.path.basename(input_path)
output_path = os.path.join(output_folder, f"detected_{filename}")

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

    results = model.predict(frame, conf=0.5)

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = box.conf[0].item()
        label = int(box.cls[0].item())
        label_text = f"{model.names[label]} {confidence:.2f}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    out.write(frame)

cap.release()
out.release
