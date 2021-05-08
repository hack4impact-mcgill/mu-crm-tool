import React from "react";
import ImageFiller from "../../../../shared/icons/image_filler.jpg";
import Chip from "@material-ui/core/Chip";

interface Project {
    name: string;
    type: string;
    neighbourhood: string;
}
const ProjectDisplay: React.FC<Project> = ({
    name,
    type,
    neighbourhood,
}: Project) => {
    return (
        <div>
            <img src={ImageFiller} alt="filler" />
            <h2>{name}</h2>
            <Chip size="small" label={type} color="primary" />
            <Chip size="small" label={neighbourhood} color="secondary" />
        </div>
    );
};
export default ProjectDisplay;
