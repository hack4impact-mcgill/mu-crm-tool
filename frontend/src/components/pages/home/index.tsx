import React, { useEffect } from 'react';
import Button from '@material-ui/core/Button'
import { useAppSelector, useAppDispatch } from '../../../redux/hooks'
import { 
    decrement, 
    increment, 
    getProjects, 
    selectHome,
    selectProjects
} from './homeSlice'


const Home: React.FC = () => {
    const count = useAppSelector(selectHome)
    const projects = useAppSelector(selectProjects)
    const dispatch = useAppDispatch()
    useEffect(() => {
        dispatch(getProjects())
    }, [dispatch])

    const onIncrement = () => {
        dispatch(increment())
    }

    const onDecrement = () => {
        dispatch(decrement())
    }

    return (
        <div>
            <Button
                variant='contained'
                color='primary'
                onClick={onIncrement}
            >
                increment
            </Button>
            {count}
            <Button
                variant='contained'
                color='primary'
                onClick={onDecrement}
            >
                decrement
            </Button>
            {projects.map((project, _) => (
                <div>
                    {project.id}
                </div>
            ))}
        </div>
    )
}

export default Home;
