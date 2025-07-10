# posture.py (Updated Rule-Based Posture Detection)
import cv2
import math
import numpy as np
import tensorflow as tf
from config_reader import config_reader
from scipy.ndimage.filters import gaussian_filter
from model import get_testing_model
import util
import os
import requests

# Load config
params, model_params = config_reader()

# TensorFlow 1.x session setup
graph = tf.compat.v1.get_default_graph()
sess = tf.compat.v1.Session()
tf.compat.v1.keras.backend.set_session(sess)

# Dropbox model download logic
model_path = './model/keras/model.h5'
dropbox_url = 'https://www.dropbox.com/scl/fi/k4wtwzpnqiwh54noo0j7y/model.h5?rlkey=sldakr0dtjtoayzp75v5y94l2&st=zc9cvlym&dl=1'

if not os.path.exists(model_path):
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    print("Downloading model.h5 from Dropbox...")
    try:
        r = requests.get(dropbox_url)
        r.raise_for_status()  # Raise error if download failed
        with open(model_path, 'wb') as f:
            f.write(r.content)
        print("Download complete.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download model: {e}")
else:
    print("Model already exists, skipping download.")

# Load model
with graph.as_default():
    with sess.as_default():
        model = get_testing_model()
        model.load_weights(model_path)

# Calculate angle between two points
def calc_angle(a, b):
    ax, ay = a
    bx, by = b
    return math.atan2(by - ay, bx - ax)

# Calculate vertical difference
def vertical_distance(a, b):
    return abs(a[1] - b[1]) if a and b else 0

# Rule-based posture evaluator
def evaluate_posture(all_peaks, posture_type):
    def get_point(i):
        return all_peaks[i][0][0:2] if all_peaks[i] else None

    nose = get_point(0)
    neck = get_point(1)
    r_shoulder = get_point(2)
    l_shoulder = get_point(5)
    r_hip = get_point(8)
    l_hip = get_point(11)
    r_knee = get_point(9)
    r_ankle = get_point(10)

    feedback = []
    bad_conditions = []

    if posture_type == "squat":
        if r_hip and r_shoulder and (r_hip[1] > r_shoulder[1] + 30):
            pass
        else:
            bad_conditions.append("Hip not low enough")

        if neck and r_hip:
            back_angle = abs(math.degrees(calc_angle(neck, r_hip)))
            if back_angle < 70 or back_angle > 180:
                bad_conditions.append(f"Back angle abnormal ({round(back_angle)}°)")

        if r_knee and r_ankle and r_knee[0] > r_ankle[0] + 40:
            bad_conditions.append("Knee goes too far forward")

        if bad_conditions:
            feedback.append("❌ Bad squat posture: " + ", ".join(bad_conditions))
        else:
            feedback.append("✅ Good squat posture")

    elif posture_type == "desk":
        if nose and neck and abs(nose[0] - neck[0]) > 35:
            bad_conditions.append("Slouching: head too forward")

        if nose and nose[1] < 180:
            bad_conditions.append("Head too high - might be hair forward")

        if neck and r_shoulder and l_shoulder:
            neck_y = neck[1]
            avg_shoulder_y = (r_shoulder[1] + l_shoulder[1]) / 2
            if neck_y < avg_shoulder_y - 20:
                bad_conditions.append("Neck above shoulders - slouching")

            shoulder_width = abs(r_shoulder[0] - l_shoulder[0])
            if shoulder_width > 250:
                bad_conditions.append("Shoulders too wide – forward leaning")

        if neck and r_hip:
            horiz_diff = abs(neck[0] - r_hip[0])
            vert_diff = abs(neck[1] - r_hip[1])
            if horiz_diff > vert_diff * 0.4:
                bad_conditions.append("Back not vertically aligned")

        if bad_conditions:
            feedback.append("❌ Bad sitting posture: " + ", ".join(bad_conditions))
        else:
            feedback.append("✅ Good sitting posture")

    return feedback

def process_frame(frame, posture_type):
    global model, graph, sess
    with graph.as_default():
        with sess.as_default():
            multiplier = [x * model_params['boxsize'] / frame.shape[0] for x in params['scale_search']]
            heatmap_avg = np.zeros((frame.shape[0], frame.shape[1], 19))
            paf_avg = np.zeros((frame.shape[0], frame.shape[1], 38))

            for scale in multiplier:
                imageToTest = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
                imageToTest_padded, pad = util.padRightDownCorner(
                    imageToTest, model_params['stride'], model_params['padValue']
                )
                input_img = np.transpose(np.float32(imageToTest_padded[:, :, :, np.newaxis]), (3, 0, 1, 2))
                output_blobs = model.predict(input_img)
                heatmap = np.squeeze(output_blobs[1])
                paf = np.squeeze(output_blobs[0])

                heatmap = cv2.resize(heatmap, (0, 0), fx=model_params['stride'], fy=model_params['stride'])
                heatmap = heatmap[:imageToTest_padded.shape[0] - pad[2],
                                  :imageToTest_padded.shape[1] - pad[3], :]
                heatmap = cv2.resize(heatmap, (frame.shape[1], frame.shape[0]))

                paf = cv2.resize(paf, (0, 0), fx=model_params['stride'], fy=model_params['stride'])
                paf = paf[:imageToTest_padded.shape[0] - pad[2],
                          :imageToTest_padded.shape[1] - pad[3], :]
                paf = cv2.resize(paf, (frame.shape[1], frame.shape[0]))

                heatmap_avg += heatmap / len(multiplier)
                paf_avg += paf / len(multiplier)

            all_peaks = []
            peak_counter = 0

            for part in range(18):
                map_ori = heatmap_avg[:, :, part]
                map = gaussian_filter(map_ori, sigma=1)

                peaks_binary = (
                    (map >= np.roll(map, 1, axis=0)) &
                    (map >= np.roll(map, -1, axis=0)) &
                    (map >= np.roll(map, 1, axis=1)) &
                    (map >= np.roll(map, -1, axis=1)) &
                    (map > 0.1)
                )
                peaks = list(zip(np.nonzero(peaks_binary)[1], np.nonzero(peaks_binary)[0]))
                peaks_with_score = [x + (map_ori[x[1], x[0]],) for x in peaks]
                ids = range(peak_counter, peak_counter + len(peaks))
                peaks_with_score_and_id = [peaks_with_score[i] + (ids[i],) for i in range(len(ids))]
                all_peaks.append(peaks_with_score_and_id)
                peak_counter += len(peaks)

            return frame, evaluate_posture(all_peaks, posture_type)
