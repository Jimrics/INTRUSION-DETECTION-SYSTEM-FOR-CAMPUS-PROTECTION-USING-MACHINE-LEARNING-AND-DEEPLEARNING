// src/components/Animal.jsx
import React, { useState } from "react";
import "./styles.css";


function Animal() {
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
      const res = await fetch("http://localhost:5000/upload", {
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
        <div>
          <h3>Video 1</h3>
          <video style={videoStyle} controls autoPlay loop muted>
            <source src="./videos/detected_Leopard at police station_format.mp4" type="video/mp4" />
          </video>
        </div>
        <div>
          <h3>Video 2</h3>
          <video style={videoStyle} controls autoPlay loop muted>
            <source src="./videos/elephant_output_detected.mp4" type="video/mp4" />
          </video>
        </div>
        <div>
          <h3>Video 3</h3>
          <video style={videoStyle} controls autoPlay loop muted>
            <source src="./videos/detected_Security guard naps as leopard_format.mp4" type="video/mp4" />
          </video>
        </div>

        {processedVideoUrl && (
          <div>
            <h3>🔍 Processed Video</h3>
            <video style={videoStyle} controls autoPlay loop muted>
              <source src={processedVideoUrl} type="video/mp4" />
            </video>
          </div>
        )}
      </div>
    </div>
  );
}

export default Animal;
