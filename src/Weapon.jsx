// src/components/Weapon.jsx
import React, { useState } from "react";
import "./styles.css";

function Weapon() {
  const [processedVideoUrl, setProcessedVideoUrl] = useState(null);

  const videoStyle = {
    width: "300px",
    height: "200px",
    margin: "10px"
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("video", file);

    try {
      const res = await fetch("http://localhost:5000/weapon-detect", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      setProcessedVideoUrl(`http://localhost:5000${data.output_path}`);
    } catch (err) {
      console.error("Upload failed:", err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      
      <input type="file" accept="video/mp4" onChange={handleFileUpload} />

      <div style={{ marginTop: "30px", display: "flex", justifyContent: "center", flexWrap: "wrap" }}>
        {/* 🔁 Example video 1 */}
        <div>
          <h3>Sample Weapon Detection 1</h3>
          <video style={videoStyle} controls autoPlay loop muted>
            <source src="/videos/gun_detected_videoplayback.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>

        {/* 🔁 Example video 2 */}
        <div>
          <h3>Sample Weapon Detection 2</h3>
          <video style={videoStyle} controls autoPlay loop muted>
            <source src="/videos/detected_gun_store.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>

        {/* 🔁 Processed uploaded video */}
        {processedVideoUrl && (
          <div>
            <h3>🔍 Processed Uploaded Video</h3>
            <video style={videoStyle} controls autoPlay loop muted>
              <source src={processedVideoUrl} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        )}
      </div>
    </div>
  );
}

export default Weapon;
