import React from "react";
import "./App.css";
import LogIn from "./LogIn";

function App() {
  return (
    <div className="App">
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
        }}
      >
        <LogIn />
      </div>
    </div>
  );
}

export default App;
