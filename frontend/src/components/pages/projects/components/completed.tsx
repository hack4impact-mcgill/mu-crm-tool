import axios from 'axios';
import React, { Component, useEffect, useState } from 'react';

export interface Project{
    name: string;
    type: string;
    neighbourhood: string;
}
export type Projects = Project[];
const Completed: React.FC = () => {
    // Array of incomplete projects
    const [completedProjects, setCompletedProjects] = useState<Projects>([]);
    useEffect(() => {
        axios.get<Projects>('"/project?is-completed=true').then((response) => {
            setCompletedProjects(response.data);
        });
    }, []);
    
    return (
        <>
            <ul>
                {
                    completedProjects.map(project => 
                        <li>
                            {project.name}
                        </li>)
                }
            </ul>
        </>
    )
};
export default Completed;