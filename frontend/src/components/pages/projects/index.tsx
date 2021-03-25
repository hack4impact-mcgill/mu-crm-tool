import React from 'react';
import InProgress from "./components/in_progress";
import Completed from "./components/completed";


const Projects: React.FC = () => {
    return (
        <div>
            <InProgress/>
            <Completed/>
        </div>
    )
}

export default Projects;
