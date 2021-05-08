import React, { useEffect, useState } from "react";
import { useAppSelector, useAppDispatch } from "../../../redux/hooks";
import ProjectDisplay from "./components/project";
import SimpleSelect from "./components/dropdown";

import {
    getProjects,
    getBoroughs,
    getTypes,
    selectProjects,
    selectBoroughs,
    selectTypes,
} from "./homeSlice";

const Home: React.FC = () => {
    const projects = useAppSelector(selectProjects);
    const boroughs = useAppSelector(selectBoroughs);
    const types = useAppSelector(selectTypes);

    // sets initial states
    const [completedProjects, setCompletedProjects] = useState(() =>
        projects.filter((project) => project.is_completed === "True")
    );
    const [inProgressProjects, setInProgressProjects] = useState(() =>
        projects.filter((project) => project.is_completed === "False")
    );

    const dispatch = useAppDispatch();
    useEffect(() => {
        dispatch(getProjects());
        dispatch(getBoroughs());
        dispatch(getTypes());
    }, [dispatch]);

    return (
        <div>
            <h2>In Progress</h2>
            <SimpleSelect
                label="Boroughs"
                items={boroughs}
                selected="None"
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    e.target.value === "None"
                        ? setCompletedProjects(
                              projects.filter(
                                  (project) => project.is_completed === "False"
                              )
                          )
                        : (setCompletedProjects(
                              completedProjects.filter(
                                  (completedProject) =>
                                      completedProject.boroughs ===
                                      e.target.value
                              )
                          ),
                          setInProgressProjects(
                              inProgressProjects.filter(
                                  (inProgressProject) =>
                                      inProgressProject.boroughs ===
                                      e.target.value
                              )
                          ))
                }
            />
            <SimpleSelect
                label="Project Type"
                items={types}
                selected="None"
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    e.target.value === "None"
                        ? setCompletedProjects(
                              projects.filter(
                                  (project) => project.is_completed === "True"
                              )
                          )
                        : (setCompletedProjects(
                              completedProjects.filter(
                                  (completedProject) =>
                                      completedProject.type === e.target.value
                              )
                          ),
                          setInProgressProjects(
                              inProgressProjects.filter(
                                  (inProgressProject) =>
                                      inProgressProject.type === e.target.value
                              )
                          ))
                }
            />
            <hr />
            <div>
                {inProgressProjects.map((inProgressProject) => (
                    <ProjectDisplay
                        name={inProgressProject.name}
                        type={inProgressProject.type}
                        neighbourhood={inProgressProject.neighbourhood}
                    />
                ))}
            </div>
            <h2>Completed</h2>
            <hr />
            <div>
                {completedProjects.map((completedProject) => (
                    <ProjectDisplay
                        name={completedProject.name}
                        type={completedProject.type}
                        neighbourhood={completedProject.neighbourhood}
                    />
                ))}
            </div>
        </div>
    );
};

export default Home;
