# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import cv2
from werkzeug.utils import secure_filename
from detector import process_frame  # corrected import name

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
MAX_FRAMES = 10

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ping')
def ping():
    return "pong"

@app.route('/analyze', methods=['POST'])
def analyze_posture():
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file part'}), 400

        posture_type = request.form.get('postureType', 'squat').lower()  # fix key name
        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
            file.save(save_path)

            cap = cv2.VideoCapture(save_path)
            frame_feedback = []
            frame_count = 0
            feedback_set = set()

            while frame_count < MAX_FRAMES:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_count += 1
                _, feedbacks = process_frame(frame, posture_type)
                if feedbacks:
                    primary_feedback = feedbacks[0]  # Only one feedback per frame
                    frame_feedback.append({
                        "frame": frame_count,
                        "feedback": [primary_feedback]
                    })
                    feedback_set.add(primary_feedback)

            cap.release()
            os.remove(save_path)

            return jsonify({
                "summary": list(feedback_set),
                "analysis": frame_feedback
            })

        return jsonify({'error': 'Invalid file format'}), 400

    except Exception as e:
        print("❌ Backend error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
