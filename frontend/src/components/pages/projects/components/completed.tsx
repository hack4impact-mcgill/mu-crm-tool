import axios from 'axios';
import React, { Component, useEffect, useState } from 'react';
// import IndividualBlock from "./IndividualBlock.tsx"
import IndividualBlock from "./individual_block";

export interface Project{
    name: string;
    type: string;
    neighbourhood: string;
}

export type Projects = Project[];

const Completed: React.FC = () => {
    // Array of incomplete projects
    const [completedProjects, setCompletedProjects] = useState<Projects>([]);

    // basically onMount
    useEffect(() => {
        axios.get<Projects>('"/project?is-completed=true').then((response) => {
            setCompletedProjects(response.data);
        });
    }, []);
    
    return (
        <>
            <div>
                {
                    completedProjects.map(project => 
                            <IndividualBlock name={project.name} type={project.type} neighbourhood={ project.neighbourhood}/>)
                }
            </div>
        </>
    )
};
export default Completed;