# 🧍‍♂️ Posture Detector (Squat & Desk Sitting)

A web app that analyzes posture from video uploads using a pre-trained **OpenPose** model and **rule-based logic**.  
It consists of:
- ✅ **Flask backend** (video processing & posture evaluation)
- ⚛️ **React frontend** (upload UI & feedback display)
- 🧠 Posture rules for **squat** and **desk-sitting** poses

---

## 🖼 Preview

### React Frontend – Video Upload & Feedback  
![Frontend UI screenshot](/Front_end/src/screenshot_frontend.png)

---

## 📂 Project Structure

```
Posture_detetcor/
├── Front_end/           # React app  
│   ├── src/             # Frontend source code (App.js, components, CSS)  
│   ├── public/  
│   └── package.json  
├── Back_end/            # Flask server  
│   ├── app.py            # REST API  
│   ├── posture.py        # Pose evaluation logic  
│   ├── util.py, model.py, config_reader.py  
│   ├── model/            # OpenPose weights (`model.h5`)  
│   ├── uploads/          # (Temporary video storage)  
│   └── requirements.txt  
├── README.md            # Project overview (this file)  
└── .gitignore           # Excluded files/folders  
```

---

## 🔧 Technology Stack

| Frontend | Backend | Model         | Rule Logic |
|---------|---------|---------------|------------|
| React.js | Flask (Python) | TensorFlow 1.x OpenPose model | Custom angle & position checks |

---

## 🧠 How It Works

1. **Video Upload** via React UI.  
2. React sends it to Flask via `/analyze` POST.  
3. Flask reads up to 10 frames using OpenCV.  
4. Each frame goes through **OpenPose**, identifying 18 keypoints (nose, neck, shoulders, hips, knees, ankles, etc.).  
5. `posture.py` uses conditional **rules** to evaluate posture:

   ### Squat Rules  
   - **Hip below shoulders** – ensures proper depth  
   - **Back angle between 70°–180°** – for natural forward lean  
   - **Knee not ahead of ankle** – to prevent improper knee placement  

   ### Desk Sitting Rules  
   - **Neck & head alignment** – detects forward head slouch  
   - **Hair/head too high** – indicates slouching or leaning forward  
   - **Neck above shoulders** or **shoulders wide** – signs of slouching  
   - **Vertical spine alignment** – neck vs hip alignment check  

6. For each frame, feedback is returned:
   - ✅ *Good posture*  
   - ❌ *Bad posture* + explanation  

7. React shows:
   - Summary popup of all detected issues  
   - Frame-wise feedback as a list

---## 🔗 Live Demo & Video

- 🌐 **Hosted App**: [Click to Try](https://posture-detetcor.vercel.app/)
- 📹 **Demo Video**: [Watch Demo](https://drive.google.com/file/d/1e_QDBDeYiNkOXFkdGD7BOXdr7_NQrYs1/view?usp=drivesdk)

---
---

## ⚙️ Setup Guide

### 🛠 Backend (Flask)
```bash
cd Back_end
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python app.py
```

### 🛠 Frontend (React)
```bash
cd Front_end
npm install
npm start
```
- Browse to `http://localhost:3000`, upload a video, and choose posture type.

---

## 📋 `.gitignore` Contents

```gitignore
# Front_end
node_modules/

# Back_end
__pycache__/
uploads/
.env
```

---

## ✅ Supported Formats

- Video formats: `.mp4`, `.avi`, `.mov`, `.mkv`
- Max frames evaluated per upload: **10**
- Pose types: `"squat"` or `"desk"`

---

## 🔍 Enhancement Ideas

- 📸 Webcam live stream posture analysis  
- 🎯 Threshold tuning using multiple sample videos  
- 📝 Add corrective suggestions (like “straighten back”)  
- 🧩 Extend to other poses (push-ups, lunges, yoga)  
- 📈 Visual overlay of keypoint skeleton & angles  

---

## 👨‍💻 About the Author

**Kamesh S (kameshkgm)**  
Software Engineer specializing in Full Stack, ML-based computer vision.  
GitHub: [@kameshkgm](https://github.com/kameshkgm)

---

## 🌟 Show your support!

If you find this project useful, please **⭐ star** it on GitHub! 🎉  
