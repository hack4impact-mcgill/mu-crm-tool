import React from 'react';
import Select from '@material-ui/core/Select';
interface Prop{
    title: String
}

const Header:React.FC<Prop> = ({title}:Prop) => {
    
    return (
        <div>
            <p>{title}</p>
            <br></br> 
        </div>
    )
}
export default Header;