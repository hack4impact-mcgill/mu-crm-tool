import React, { Component } from "react";
import "./App.css";
import LogIn from "./LogIn";

class App extends Component {
  state = {
    // the state of the app can be printed
    // only two fields: email and password
    fields: {},
  };

  // only gets one value
  onChange = (updatedValue) => {
    // passes in the fields, then the updated value that's passed in from the form
    // keep the original fields with ...this.state.fields
    this.setState({ fields: { ...this.state.fields, ...updatedValue } });
  };

  render() {
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
          <LogIn onChange={(updatedValue) => this.onChange(updatedValue)} />
        </div>
      </div>
    );
  }
}

export default App;
