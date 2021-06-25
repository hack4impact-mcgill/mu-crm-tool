import React from "react";
import Chip from "@material-ui/core/Chip";
import "./projectCard.css";

type ProjectCardProps = {
  title: string;
  neighbourhood: string;
  type: string;
};

const ProjectCard: React.FC<ProjectCardProps> = ({
  title,
  neighbourhood,
  type,
}: ProjectCardProps) => {
  return (
    <div>
      <img
        src="https://assets.bonappetit.com/photos/5c62e4a3e81bbf522a9579ce/5:4/w_2815,h_2252,c_limit/milk-bread.jpg"
        alt="filler"
      ></img>
      <div className="description-box">
        <p>{title}</p>
        <div className="chips">
          <Chip label={neighbourhood} className="neighbourhood" />
          <Chip label={type} className="type" />
        </div>
      </div>
    </div>
  );
};

export default ProjectCard;
