import React, { useEffect, useState } from "react";
import { useAppSelector, useAppDispatch } from "../../../redux/hooks";
import { getProjects, selectProjects } from "./homeSlice";
import ProjectCard from "./projectCard";
import { Select, FormControl, InputLabel, MenuItem } from "@material-ui/core";
import "./index.css";

// not fully typed, add things into this for your usage
interface Project {
  name: string;
  neighbourhood: string;
  type: string;
  is_completed: boolean;
}
const Home: React.FC = () => {
  const projects = useAppSelector(selectProjects);
  const dispatch = useAppDispatch();
  const [inProgressProjects, setInProgressProjects] = useState<Project[]>([]);
  const [completedProjects, setCompletedProjects] = useState<Project[]>([]);
  useEffect(() => {
    dispatch(getProjects());
  }, [dispatch]);

  useEffect(() => {
    setInProgressProjects(
      projects.filter((project, _) => project.is_completed === true)
    );
    setCompletedProjects(
      projects.filter((project, _) => project.is_completed === false)
    );
  }, [projects]);
  return (
    <div>
      <div className="project-parent-box">
        <div className="title-box">
          <h1>In Progress</h1>
          <FormControl variant="outlined">
            <InputLabel>Boroughs</InputLabel>
            <Select
              labelId="demo-simple-select-outlined-label"
              id="demo-simple-select-outlined"
              label="Boroughs"
            ></Select>
          </FormControl>
        </div>
        <hr></hr>
        <div className="project-card-box">
          {inProgressProjects.map((project, _) => (
            <div className="project-card">
              <ProjectCard
                title={project.name}
                neighbourhood={project.neighbourhood}
                type={project.type}
              />
            </div>
          ))}
        </div>
        <br></br>
      </div>

      <div className="project-parent-box">
        <h1>Completed</h1>
        <hr></hr>
        <div className="project-card-box">
          {completedProjects.map((project, _) => (
            <div className="project-card">
              <ProjectCard
                title={project.name}
                neighbourhood={project.neighbourhood}
                type={project.type}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;
