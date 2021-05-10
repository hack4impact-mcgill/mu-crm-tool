import React from "react";
import ImageFiller from "../../../../shared/icons/image_filler.png";
import Chip from "@material-ui/core/Chip";
import "./project.css";

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
            <img src={ImageFiller} alt="" className="image" />
            <div className="descriptionContainer">
                <h3>{name}</h3>
                <div className="chips">
                    <Chip
                        size="medium"
                        label={neighbourhood}
                        style={{
                            backgroundColor: "#59f7d5",
                            borderRadius: 3,
                            fontWeight: "bold",
                            marginRight: 20,
                        }}
                    />
                    <Chip
                        size="medium"
                        label={type}
                        style={{
                            backgroundColor: "#ffba60",
                            borderRadius: 3,
                            fontWeight: "bold",
                        }}
                    />
                </div>
            </div>
        </div>
    );
};
export default ProjectDisplay;
