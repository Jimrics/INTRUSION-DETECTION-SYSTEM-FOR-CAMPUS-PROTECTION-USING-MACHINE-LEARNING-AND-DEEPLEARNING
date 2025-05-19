import React, { useState } from "react";

const VideoSection = ({ title, originalVideoPath, processedVideoPath }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [newVideoPath, setNewVideoPath] = useState(null); // Stores uploaded video path

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("video", selectedFile);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      setNewVideoPath(result.videoPath); // Update new video display
      alert(result.message);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div style={{ marginBottom: "30px", border: "1px solid #ccc", padding: "15px", borderRadius: "10px" }}>
      <h2>{title}</h2>

      {/* First Box - Original Video */}
      <div>
        <h3>Original Video</h3>
        <video width="500" controls>
          <source src={originalVideoPath} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>

      {/* Second Box - Processed Video */}
      <div>
        <h3>Processed Video</h3>
        <video width="500" controls>
          <source src={processedVideoPath} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>

      {/* Upload Section */}
      <div>
        <input type="file" accept="video/*" onChange={handleFileChange} style={{ margin: "10px" }} />
        <button onClick={handleUpload} style={{ padding: "10px", cursor: "pointer", background: "blue", color: "white", border: "none", borderRadius: "5px" }}>
          Upload & Detect
        </button>
      </div>

      {/* Third Box - New Uploaded Video (Appears only after upload) */}
      {newVideoPath && (
        <div>
          <h3>Newly Uploaded Video</h3>
          <video width="500" controls>
            <source src={newVideoPath} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
};

export default VideoSection;
