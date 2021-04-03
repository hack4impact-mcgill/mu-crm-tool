import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import type { RootState } from '../../../redux/store'

interface HomeState {
    count: number
}

const initialState: HomeState = {
    count: 0
}

export const homeSlice = createSlice({
    name: 'home',
    initialState,
    reducers: {
        increment: state => {
            console.log('hi')
            state.count += 1
        },
        decrement: state => {
            state.count -= 1
        },
        incrementByAmount: (state, action: PayloadAction<number>) => {
            state.count += action.payload
        },
    },
})

export const { increment, decrement, incrementByAmount } = homeSlice.actions

export const selectHome = (state: RootState) => state.home.count

export default homeSlice.reducer
