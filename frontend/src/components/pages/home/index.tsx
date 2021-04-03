import React from 'react';
import Button from '@material-ui/core/Button'
import { useAppSelector, useAppDispatch } from '../../../redux/hooks'
import { decrement, increment, selectHome } from './homeSlice'


const Home: React.FC = () => {
    const count = useAppSelector(selectHome)
    const dispatch = useAppDispatch()

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
        </div>
    )
}

export default Home;
