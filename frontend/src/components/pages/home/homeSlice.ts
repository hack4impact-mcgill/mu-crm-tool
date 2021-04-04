import { createAsyncThunk, createSlice, PayloadAction } from '@reduxjs/toolkit'
import type { RootState } from '../../../redux/store'
import axios from '../../../api/axios'

interface HomeState {
    count: number,
    projects: any[]
    status: 'idle' | 'pending' | 'succeeded' | 'failed',
    error: string | null
}

const initialState = {
    count: 0,
    projects: [],
    status: 'idle',
    error: null
} as HomeState

export const getProjects = createAsyncThunk(
    'home/getProjects',
    async () => {
        const response = await axios.get('/project')
        return response.data
    }
)

export const homeSlice = createSlice({
    name: 'home',
    initialState,
    reducers: {
        increment: state => {
            state.count += 1
        },
        decrement: state => {
            state.count -= 1
        },
        incrementByAmount: (state, action: PayloadAction<number>) => {
            state.count += action.payload
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(getProjects.pending,  (state, _) => {
                state.status = 'pending'
            })
            .addCase(getProjects.fulfilled, (state, action) => {
                state.projects = action.payload
                state.status = 'succeeded'
            })
            .addCase(getProjects.rejected, (state, _) => {
                state.status = 'failed'
            })
    },
})

export const { increment, decrement, incrementByAmount } = homeSlice.actions

export const selectHome = (state: RootState) => state.home.count
export const selectProjects = (state: RootState) => state.home.projects

export default homeSlice.reducer
