import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Type{
    type: string;
}
interface NeighbourHood{
    neighbourhood: string;
}

const Filters: React.FC = () => {
    
    // need an endpoint to get all neighbourhood
    const [types, setTypes] = useState<Type[]>([]);
    const [boroughs, setBoroughs] = useState<NeighbourHood[]>([]);

    // some helpers
    const getNeighbourhoods = () => {
        axios.get('/project/neighbourhoods').then((response) => {
            setBoroughs(response.data);
        })
    }
    const getTypes = () => {
        axios.get('/project/types').then((response) => {
            setTypes(response.data);
        })
    }

    // set things on start up
    useEffect(() => {
        getTypes();
        getNeighbourhoods;
    },[]
    )

    return (
        <div>   
            
        </div>
    );
}
export default Filters;