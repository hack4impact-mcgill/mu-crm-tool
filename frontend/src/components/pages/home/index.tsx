import React, { useEffect, useState } from "react";
import { useAppSelector, useAppDispatch } from "../../../redux/hooks";
import ProjectDisplay from "./components/project";
import SimpleSelect from "./components/dropdown";
import "./index.css";

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
        <div className="projects">
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
                label="ProjectTypes"
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
            <div className="projectContainer">
                {/* testers */}
                <div className="projectDisplay">
                    <ProjectDisplay
                        name="Project 1"
                        neighbourhood="Borough"
                        type="Project Type"
                    />
                </div>
                <div className="projectDisplay">
                    <ProjectDisplay
                        name="Project 2"
                        neighbourhood="Borough"
                        type="Project Type"
                    />
                </div>
                <div className="projectDisplay">
                    <ProjectDisplay
                        name="Project 3"
                        neighbourhood="Borough"
                        type="Project Type"
                    />
                </div>
                <div className="projectDisplay">
                    <ProjectDisplay
                        name="Project 4"
                        neighbourhood="Borough"
                        type="Project Type"
                    />
                </div>
                {/* tester end */}
                {inProgressProjects.map((inProgressProject) => (
                    <div className="projectDisplay">
                        <ProjectDisplay
                            name={inProgressProject.name}
                            neighbourhood={inProgressProject.type}
                            type={inProgressProject.neighbourhood}
                        />
                    </div>
                ))}
            </div>
            <h2>Completed</h2>
            <hr />
            <div className="projectContainer">
                {completedProjects.map((completedProject) => (
                    <div className="projectDisplay">
                        <ProjectDisplay
                            name={completedProject.name}
                            neighbourhood={completedProject.type}
                            type={completedProject.neighbourhood}
                        />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Home;
