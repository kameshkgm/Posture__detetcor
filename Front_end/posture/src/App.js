// Updated React Frontend Code (App.js)
import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [postureType, setPostureType] = useState('squat');
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState([]);
  const [frameWise, setFrameWise] = useState([]);
  const [showSummaryPopup, setShowSummaryPopup] = useState(false);
  const [showFrameWisePopup, setShowFrameWisePopup] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert('Please select a video file!');
      return;
    }

    const formData = new FormData();
    formData.append('video', file);
    formData.append('postureType', postureType);

    setLoading(true);
    setSummary([]);
    setFrameWise([]);

    try {
      const response = await axios.post('http://localhost:5000/analyze', formData);
      const analysis = response.data.analysis || [];

      const summaryMap = new Map();
      analysis.forEach(frame => {
        frame.feedback.forEach(msg => summaryMap.set(msg, true));
      });

      setSummary(Array.from(summaryMap.keys()));
      setFrameWise(analysis);
      setShowSummaryPopup(true);
    } catch (error) {
      alert('Error analyzing posture.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1 className="header">Posture Recognizer</h1>
      <div className="box">
        <form onSubmit={handleSubmit}>
          <select value={postureType} onChange={(e) => setPostureType(e.target.value)}>
            <option value="squat">Squat</option>
            <option value="desk">Desk Sitting</option>
          </select>
          <input type="file" accept="video/*" onChange={handleFileChange} />
          <button type="submit">Analyze</button>
        </form>
        {loading && <div className="loader"></div>}
      </div>

      {showSummaryPopup && (
        <div className="popup" onClick={() => setShowSummaryPopup(false)}>
          <div className="popup-content" onClick={(e) => e.stopPropagation()}>
            <div className="close-btn" onClick={() => setShowSummaryPopup(false)}>✖</div>
            <h3>Posture Summary</h3>
            {summary.length > 0 ? (
              <ul className="feedback-list">
                {summary.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            ) : (
              <p>No posture issues detected 🎉</p>
            )}
            <button onClick={() => setShowFrameWisePopup(true)}>View Frame-wise Feedback</button>
          </div>
        </div>
      )}

      {showFrameWisePopup && (
        <div className="popup" onClick={() => setShowFrameWisePopup(false)}>
          <div className="popup-content" onClick={(e) => e.stopPropagation()}>
            <div className="close-btn" onClick={() => setShowFrameWisePopup(false)}>✖</div>
            <h3>Frame-wise Feedback</h3>
            <ul className="framewise-list">
              {frameWise.map((frame, index) => (
                <li key={index}>
                  <strong>Frame {frame.frame}:</strong> {frame.feedback[0]}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;