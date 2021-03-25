import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Projects } from "./completed";
import IndividualBlock from "./individual_block";


const InProgress: React.FC = () => {
    // Array of incomplete projects
    const [inProgressProjects, setInProgressProjects] = useState<Projects>([]);
    useEffect(() => {
        axios.get<Projects>('/project?is-completed=false').then((response) => {
            setInProgressProjects(response.data);
        });
    }, []);
    
    return (
        <>
            <div>
                {
                    inProgressProjects.map(project => 
                            <IndividualBlock name={project.name} type={project.type} neighbourhood={ project.neighbourhood}/>)
                }
            </div>
        </>
    )
};
export default InProgress;