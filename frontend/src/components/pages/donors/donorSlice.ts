import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "../../../shared/axios";

interface DonorState {
  status: "idle" | "pending" | "succeeded" | "failed";
  error: string | null;
}

const initialState = {
  status: "idle",
  error: null,
} as DonorState;

export const importCSV = createAsyncThunk(
  "home/importCSV",
  async (fileList: FileList) => {
    let formData = new FormData();
    let files = Array.from(fileList);
    // placeholder for now as current user system has not been implemented
    // TODO: Modify added_by argument when login system and current user system has been implemented
    formData.append("added_by", "3f3f54d2-caf4-456c-a6f7-63c0ede8e3ed");
    files.forEach((file) => {
      formData.append("files", file);
    });
    const response = await axios.post("/donation/csv", formData, {
      headers: {
        "content-type": "multipart/form-data",
      },
    });
    return response.data;
  }
);

export const donorSlice = createSlice({
  name: "donor",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(importCSV.pending, (state, _) => {
        state.status = "pending";
      })
      .addCase(importCSV.fulfilled, (state, _) => {
        state.status = "succeeded";
      })
      .addCase(importCSV.rejected, (state, _) => {
        state.status = "failed";
      });
  },
});
