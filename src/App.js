// src/App.js
import React from "react";
import Animal from "./Animal";
import Weapon from "./Weapon";
import Tracking from "./Tracking";
import Face from "./Face";

function App() {
  return (
    <div style={{ padding: "20px" }}>
      <h2>Intrusion Detection system to protect campus environmenst using machine learning and deep learning techniques</h2>
      <h2>Module 1: Animal Threat detection</h2>
      <Animal />

      <hr style={{ margin: "40px 0" }} />

      <h2>Module2: Armed intrusion Detection</h2>
      <Weapon />

      <hr style={{ margin: "40px 0" }} />

      <h2> Tracking module</h2>
      <Tracking />

      <hr style={{ margin: "40px 0" }} />

      <h2>Face Authorization module</h2>
      <Face />
    </div>
  );
}

export default App;
