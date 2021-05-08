import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import type { RootState } from "../../../redux/store";
import axios from "../../../shared/axios";

interface HomeState {
    // lazy implementation
    projects: any[];
    boroughs: any[];
    types: any[];
    status: "idle" | "pending" | "succeeded" | "failed";
    error: string | null;
}

const initialState = {
    projects: [],
    boroughs: [],
    types: [],
    status: "idle",
    error: null,
} as HomeState;

export const getProjects = createAsyncThunk("home/getProjects", async () => {
    const response = await axios.get("/project");
    return response.data;
});

export const getBoroughs = createAsyncThunk("home/getBoroughs", async () => {
    const response = await axios.get("/boroughs");
    return response.data;
});

export const getTypes = createAsyncThunk("home/getTypes", async () => {
    const response = await axios.get("/types");
    return response.data;
});

export const homeSlice = createSlice({
    name: "home",
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(getProjects.pending, (state, _) => {
                state.status = "pending";
            })
            .addCase(getProjects.fulfilled, (state, action) => {
                state.projects = action.payload;
                state.status = "succeeded";
            })
            .addCase(getProjects.rejected, (state, _) => {
                state.status = "failed";
            })
            .addCase(getBoroughs.pending, (state, _) => {
                state.status = "pending";
            })
            .addCase(getBoroughs.fulfilled, (state, action) => {
                state.boroughs = action.payload;
                state.status = "succeeded";
            })
            .addCase(getBoroughs.rejected, (state, _) => {
                state.status = "failed";
            })
            .addCase(getTypes.pending, (state, _) => {
                state.status = "pending";
            })
            .addCase(getTypes.fulfilled, (state, action) => {
                state.types = action.payload;
                state.status = "succeeded";
            })
            .addCase(getTypes.rejected, (state, _) => {
                state.status = "failed";
            });
    },
});

export const selectProjects = (state: RootState) => state.home.projects;
export const selectBoroughs = (state: RootState) => state.home.boroughs;
export const selectTypes = (state: RootState) => state.home.types;

export default homeSlice.reducer;
