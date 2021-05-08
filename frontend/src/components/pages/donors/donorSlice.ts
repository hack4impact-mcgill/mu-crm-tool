import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import type { RootState } from "../../../redux/store";
import axios from "../../../shared/axios";
import { Donor } from "./index";

interface DonorState {
  donors: Donor[];
  status: "idle" | "pending" | "succeeded" | "failed";
  error: string | null;
}

const initialState = {
  donors: [],
  status: "idle",
  error: null,
} as DonorState;

const listDonors = [
  // dummy data
  { name: "Jerry", amount: 23.0, returning: false, email: "jerry@gmail.com" },
  { name: "Curtis", amount: 12.0, returning: true, email: "curtis@gmail.com" },
  { name: "Celine", amount: 34.0, returning: false, email: "celine@gmail.com" },
  { name: "Jerry", amount: 23.0, returning: false, email: "jerry@gmail.com" },
  { name: "Curtis", amount: 12.0, returning: true, email: "curtis@gmail.com" },
  { name: "Celine", amount: 34.0, returning: false, email: "celine@gmail.com" },
  { name: "Jerry", amount: 23.0, returning: false, email: "jerry@gmail.com" },
  { name: "Curtis", amount: 12.0, returning: true, email: "curtis@gmail.com" },
  { name: "Celine", amount: 34.0, returning: false, email: "celine@gmail.com" },
  { name: "Jerry", amount: 23.0, returning: false, email: "jerry@gmail.com" },
  { name: "Curtis", amount: 12.0, returning: true, email: "curtis@gmail.com" },
  { name: "Celine", amount: 34.0, returning: false, email: "celine@gmail.com" },
  { name: "Jerry", amount: 23.0, returning: false, email: "jerry@gmail.com" },
  { name: "Curtis", amount: 12.0, returning: true, email: "curtis@gmail.com" },
  { name: "Celine", amount: 34.0, returning: false, email: "celine@gmail.com" },
  { name: "Jerry", amount: 23.0, returning: false, email: "jerry@gmail.com" },
  { name: "Curtis", amount: 12.0, returning: true, email: "curtis@gmail.com" },
  { name: "Celine", amount: 34.0, returning: false, email: "celine@gmail.com" },
  { name: "Jerry", amount: 23.0, returning: false, email: "jerry@gmail.com" },
  { name: "Curtis", amount: 12.0, returning: true, email: "curtis@gmail.com" },
  { name: "Celine", amount: 34.0, returning: false, email: "celine@gmail.com" },
  { name: "Jerry", amount: 23.0, returning: false, email: "jerry@gmail.com" },
  { name: "Curtis", amount: 12.0, returning: true, email: "curtis@gmail.com" },
  { name: "Celine", amount: 34.0, returning: false, email: "celine@gmail.com" },
  { name: "Jerry", amount: 23.0, returning: false, email: "jerry@gmail.com" },
  { name: "Curtis", amount: 12.0, returning: true, email: "curtis@gmail.com" },
  { name: "Celine", amount: 34.0, returning: false, email: "celine@gmail.com" },
];

export const getDonors = createAsyncThunk("donors/getDonors", async () => {
  //   const response = await axios.get("/project");
  return listDonors;
});

export const donorSlice = createSlice({
  name: "donor",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getDonors.pending, (state, _) => {
        state.status = "pending";
      })
      .addCase(getDonors.fulfilled, (state, action) => {
        state.donors = action.payload;
        state.status = "succeeded";
      })
      .addCase(getDonors.rejected, (state, _) => {
        state.status = "failed";
      });
  },
});

export const selectDonors = (state: RootState) => state.donor.donors;

export default donorSlice.reducer;
