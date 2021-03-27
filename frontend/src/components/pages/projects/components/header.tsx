import React from 'react';
import Select from '@material-ui/core/Select';
import Filters from "./filters";
interface Prop{
    title: String
    showFilter:Boolean
}

const Header: React.FC<Prop> = ({ title, showFilter }:Prop) => {
    
    return (
        <div>
            <p>{title}</p>
            {/* only render show filters on top */}
            { showFilter && <Filters/>}
            <hr></hr>
        </div>
    )
}
export default Header;