// src/components/Face.jsx
import React, { useState } from "react";
import axios from "axios";
import "./styles.css";

function Face() {
  const [processedVideoUrl, setProcessedVideoUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const videoStyle = {
    width: "300px",
    height: "200px",
    margin: "10px"
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("video", file);

    try {
      setLoading(true);
      const response = await axios.post("http://localhost:5000/face-detect", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });

      const { output_path } = response.data;
      setProcessedVideoUrl(`http://localhost:5000${output_path}`);
    } catch (err) {
      alert("Error uploading video for face detection.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <input type="file" accept="video/mp4" onChange={handleUpload} />
      {loading && <p>Processing video... ⏳</p>}

      <div style={{ marginTop: "30px", display: "flex", gap: "30px", flexWrap: "wrap", justifyContent: "center" }}>
        <div>
          <h3>Input Video</h3>
          <video style={videoStyle} controls autoPlay loop muted>
            <source src="./videos/3_people_walking.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>

        <div>
          <h3>Sample Face Output</h3>
          <video style={videoStyle} controls autoPlay loop muted>
            <source src="./videos/face_output_video.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      </div>

      {processedVideoUrl && (
        <div style={{ marginTop: "30px" }}>
          <h3>🔍 Processed Output</h3>
          <video style={videoStyle} controls autoPlay loop muted>
            <source src={processedVideoUrl} type="video/mp4" />
          </video>
        </div>
      )}
    </div>
  );
}

export default Face;
