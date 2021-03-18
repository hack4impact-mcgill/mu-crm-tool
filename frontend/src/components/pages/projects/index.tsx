import React from 'react';
import InProgress from "./components/inProgress";
import Completed from "./components/completed";


const Projects: React.FC = () => {
    return (
        <div> 
            <h1>In Progress</h1>
            <InProgress/>
            <h1>Completed</h1>
            <Completed/>
            <p>Tarbarnak</p>
        </div>
    )
}

export default Projects;
