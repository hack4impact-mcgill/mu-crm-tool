import React from "react";
import Button from "@material-ui/core/Button";
import { useAppDispatch } from "../../../redux/hooks";
import { importCSV } from "./donorSlice";

const DonorPage: React.FC = () => {
  const dispatch = useAppDispatch();
  const onUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(importCSV(e.target.files!));
  };

  return (
    <div>
      <div>donor placeholder</div>
      <Button variant="contained" color="primary" component="label">
        Import CSV File
        <input type="file" hidden multiple onChange={onUpload} />
      </Button>
    </div>
  );
};

export default DonorPage;
