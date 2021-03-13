import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      {/* render the projects into the two different sections and 
      display the project name, borough and project type 
      with the last two using 
      https://material-ui.com/components/chips/#chip like in the 
      figma prototype */}
      <h1>Landing page</h1>

      <div className="In Progress">
          <h1>In Progress</h1>
      </div>
      <div className="Completed">
        <h1>Completed</h1>
      </div>

    </div>
  );
}

export default App;
