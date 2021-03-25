import React from 'react';
import MuIcon from "../../../statics/MuIcon.jpg";
import { Project } from "./completed";
import Chip from '@material-ui/core/Chip';

const IndividualBlock: React.FC<Project>= ({name, type, neighbourhood}: Project) => {
    {
        return (
            <div>
                <img src={MuIcon}></img>
                <h2>{name}</h2>
                <Chip size="small" label={type} color="primary"/>
                <Chip size="small" label={neighbourhood} color = "secondary"/>
            </div>
        );
    }
}
export default IndividualBlock;