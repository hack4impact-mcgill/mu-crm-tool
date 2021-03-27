import React from 'react';
import InProgress from "./components/in_progress";
import Completed from "./components/completed";
import Header from "./components/header";


const Projects: React.FC = () => {
    return (
        <div>
            <Header title="In Progress" showFilter={true}/>
            <InProgress />
            <Header title="Completed" showFilter={ false }/>
            <Completed/>
        </div>
    )
}

export default Projects;
