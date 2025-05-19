// src/components/Tracking.jsx
import React from "react";
import "./styles.css";

function Tracking() {
  const videoStyle = {
    width: "300px",
    height: "200px",
    margin: "10px"
  };

  const videoGroupStyle = {
    display: "flex",
    justifyContent: "center",
    marginBottom: "30px",
    flexWrap: "wrap"
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    // Placeholder for future processing
    console.log("Uploaded file:", file);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Tracking Module</h2>
      <input type="file" accept="video/mp4" onChange={handleFileUpload} />

      {/* Group 1: Video 1 and Video 2 */}
      <div style={videoGroupStyle}>
        <div>
          <h3>Tracking Video 1</h3>
          <video style={videoStyle} controls autoPlay loop muted>
            <source src="/videos/output_part1-converted.mp4" type="video/mp4" />
          </video>
        </div>

        <div>
          <h3>Tracking Video 2</h3>
          <video style={videoStyle} controls autoPlay loop muted>
            <source src="/videos/output_part2-converted.mp4" type="video/mp4" />
          </video>
        </div>
      </div>

      {/* Group 2: Video 3 and Video 4 */}
      <div style={videoGroupStyle}>
        <div>
          <h3>Tracking Video 3</h3>
          <video style={videoStyle} controls autoPlay loop muted>
            <source src="/videos/output_part2 (2)-converted.mp4" type="video/mp4" />
          </video>
        </div>

        <div>
          <h3>Tracking Video 4</h3>
          <video style={videoStyle} controls autoPlay loop muted>
            <source src="/videos/output_video3-converted.mp4" type="video/mp4" />
          </video>
        </div>
      </div>
    </div>
  );
}

export default Tracking;
