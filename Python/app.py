from flask import Flask, request, jsonify, send_from_directory
import os
import subprocess
from werkzeug.utils import secure_filename
from flask_cors import CORS
from twilio.rest import Client
from weapon_detect import run_weapon_detection  # ✅ direct import

# Initialize Flask and CORS
app = Flask(__name__)
CORS(app)

# Define folders
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ✅ Twilio configuration
TWILIO_ACCOUNT_SID = "ACec708d3f94bd222c466d50"
TWILIO_AUTH_TOKEN = "eebd80b54124dfb873ea3a59e"
TWILIO_FROM_NUMBER = "+187822552"
TWILIO_TO_NUMBER = "+919172"

def send_sms_alert(message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=TWILIO_TO_NUMBER
        )
        print("✅ SMS sent")
    except Exception as e:
        print(f"❌ SMS failed: {e}")

def convert_to_browser_compatible(input_path, output_path):
    try:
        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-c:v", "libx264",
            "-c:a", "libmp3lame",
            "-preset", "fast",
            "-movflags", "+faststart",
            output_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] ffmpeg conversion failed: {e}")
        raise

# 🐾 Animal Detection Route
@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video = request.files["video"]
    if video.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(video.filename)
    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    video.save(upload_path)
    print(f"[DEBUG] Saved uploaded video to: {upload_path}")

    result = subprocess.run(
        ["python", "animal_detection.py", upload_path, OUTPUT_FOLDER],
        capture_output=True,
        text=True
    )
    print("[DEBUG] animal_detection.py stdout:", result.stdout)
    print("[DEBUG] animal_detection.py stderr:", result.stderr)

    if result.returncode != 0:
        return jsonify({"error": "Processing failed", "details": result.stderr}), 500

    detected_filename = f"detected_{filename}"
    raw_output_path = os.path.join(OUTPUT_FOLDER, detected_filename)
    converted_filename = f"converted_{filename}"
    converted_output_path = os.path.join(OUTPUT_FOLDER, converted_filename)

    try:
        convert_to_browser_compatible(raw_output_path, converted_output_path)
    except:
        return jsonify({"error": "Video conversion failed"}), 500

    send_sms_alert("Threat detected in the campuses. Please raise the alarm. Check footages.")

    return jsonify({"output_path": f"/outputs/{converted_filename}"})


# 🔫 Weapon Detection Route (✅ UPDATED)
@app.route("/weapon-detect", methods=["POST"])
def weapon_detect():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video = request.files["video"]
    if video.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(video.filename)
    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    video.save(upload_path)
    print(f"[DEBUG] Saved uploaded video to: {upload_path}")

    detected_filename = f"detected_{filename}"
    raw_output_path = os.path.join(OUTPUT_FOLDER, detected_filename)
    converted_filename = f"converted_{filename}"
    converted_output_path = os.path.join(OUTPUT_FOLDER, converted_filename)

    try:
        run_weapon_detection(upload_path, raw_output_path)
        print("[DEBUG] run_weapon_detection executed successfully")
    except Exception as e:
        print(f"[ERROR] Weapon detection failed: {e}")
        return jsonify({"error": "Weapon detection failed", "details": str(e)}), 500

    try:
        convert_to_browser_compatible(raw_output_path, converted_output_path)
    except:
        return jsonify({"error": "Video conversion failed"}), 500

    send_sms_alert("Armed intrusion detected in campus. Signal alert")

    return jsonify({"output_path": f"/outputs/{converted_filename}"})


# 👤 Face Detection Route
@app.route("/face-detect", methods=["POST"])
def face_detect():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video = request.files["video"]
    if video.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(video.filename)
    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    video.save(upload_path)
    print(f"[DEBUG] Saved uploaded video to: {upload_path}")

    result = subprocess.run(
        ["python", "face_detection.py", upload_path, OUTPUT_FOLDER],
        capture_output=True,
        text=True
    )
    print("[DEBUG] face_detect.py stdout:", result.stdout)
    print("[DEBUG] face_detect.py stderr:", result.stderr)

    if result.returncode != 0:
        return jsonify({"error": "Face detection failed", "details": result.stderr}), 500

    detected_filename = f"detected_{filename}"
    raw_output_path = os.path.join(OUTPUT_FOLDER, detected_filename)
    converted_filename = f"converted_{filename}"
    converted_output_path = os.path.join(OUTPUT_FOLDER, converted_filename)

    try:
        convert_to_browser_compatible(raw_output_path, converted_output_path)
    except:
        return jsonify({"error": "Video conversion failed"}), 500

    send_sms_alert("Intrusion of unauthorised individual detected. Check output.")

    return jsonify({"output_path": f"/outputs/{converted_filename}"})


# 🔄 Serve output video
@app.route("/outputs/<path:filename>")
def serve_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
