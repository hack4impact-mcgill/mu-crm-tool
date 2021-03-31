import React from "react";
import "./App.css";
import "./LogIn.css";
import LogIn from "./LogIn";

const App = () => {
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
};

export default App;
