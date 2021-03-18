import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Projects } from "./completed";


const InProgress: React.FC = () => {
    // Array of incomplete projects
    const [inProgressProjects, setInProgressProjects] = useState<Projects>([]);
    useEffect(() => {
        axios.get<Projects>('"/project?is-completed=false').then((response) => {
            setInProgressProjects(response.data);
        });
    }, []);
    
    return (
        <>
            <ul>
                {
                    inProgressProjects.map(project => 
                        <li>
                            {project.name}
                        </li>)
                }
            </ul>
        </>
    )
};
export default InProgress;