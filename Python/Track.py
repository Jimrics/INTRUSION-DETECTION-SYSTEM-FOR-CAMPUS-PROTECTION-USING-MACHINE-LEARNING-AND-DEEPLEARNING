import cv2
import numpy as np
import onnxruntime as ort
from ultralytics import YOLO
from sklearn.metrics.pairwise import cosine_similarity
from scipy.optimize import linear_sum_assignment

# Kalman filter class
class KalmanTracker:
    def __init__(self, initial_box):
        self.kalman = cv2.KalmanFilter(4, 2)
        self.kalman.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]], np.float32)
        self.kalman.transitionMatrix = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]], np.float32)
        self.kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03
        self.kalman.statePre[:2, 0] = initial_box[:2]
        self.kalman.statePre[2:, 0] = 0

    def update(self, bbox_center):
        measurement = np.array([[np.float32(bbox_center[0])], [np.float32(bbox_center[1])]])
        self.kalman.correct(measurement)
        pred = self.kalman.predict()
        return int(pred[0]), int(pred[1])

# Load OSNet model
def load_osnet(model_path='osnet_model.onnx'):
    return ort.InferenceSession(model_path)

# Extract feature embedding using OSNet
def extract_osnet_embedding(session, image):
    image = cv2.resize(image, (128, 256))
    image = image.astype(np.float32) / 255.0
    image = image.transpose(2, 0, 1)[None]
    inputs = {session.get_inputs()[0].name: image}
    return session.run(None, inputs)[0][0]

# Process one video and get person's embeddings + box tracks
def process_video(video_path, osnet_session, yolo_model):
    cap = cv2.VideoCapture(video_path)
    track = None
    features = []
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret: break

        results = yolo_model(frame)[0]
        persons = [det for det in results.boxes.data.cpu().numpy() if int(det[5]) == 0]

        if len(persons) == 0:
            frames.append(frame)
            continue

        # Pick closest (largest) person
        persons.sort(key=lambda x: (x[2] - x[0]) * (x[3] - x[1]), reverse=True)
        x1, y1, x2, y2, conf, cls = persons[0].astype(int)
        crop = frame[y1:y2, x1:x2]

        # Track person center using Kalman filter
        center = ((x1 + x2)//2, (y1 + y2)//2)
        if track is None:
            track = KalmanTracker(center)
        pred_center = track.update(center)

        # Draw
        cv2.circle(frame, pred_center, 5, (0, 255, 0), -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, "Person 1", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

        emb = extract_osnet_embedding(osnet_session, crop)
        features.append(emb)
        frames.append(frame)
    cap.release()
    return np.array(features), frames

# Match two embedding sets using cosine similarity
def match_embeddings(feats1, feats2):
    avg1 = np.mean(feats1, axis=0).reshape(1, -1)
    avg2 = np.mean(feats2, axis=0).reshape(1, -1)
    score = cosine_similarity(avg1, avg2)[0][0]
    return score

# Save video
def save_video(frames, path, fps=20):
    h, w = frames[0].shape[:2]
    out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
    for f in frames:
        out.write(f)
    out.release()

# Main
def main(video1_path, video2_path):
    yolo = YOLO('yolov8n.pt')  # assumes you downloaded this
    osnet = load_osnet('osnet_model.onnx')  # you must download this too

    print("[INFO] Processing Video 1...")
    emb1, frames1 = process_video(video1_path, osnet, yolo)

    print("[INFO] Processing Video 2...")
    emb2, frames2 = process_video(video2_path, osnet, yolo)

    sim_score = match_embeddings(emb1, emb2)
    print(f"[MATCHING SIMILARITY SCORE]: {sim_score:.4f}")

    save_video(frames1, 'output_video1_tracked.mp4')
    save_video(frames2, 'output_video2_tracked.mp4')
    print("[INFO] Tracking videos saved.")

if __name__ == '__main__':
    main('video1.mp4', 'video2.mp4')
