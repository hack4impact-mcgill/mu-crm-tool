import { ListProps } from "@material-ui/core";
import React, { useState, useEffect } from "react";
import { useAppSelector, useAppDispatch } from "../../../redux/hooks";
import { getDonors, selectDonors } from "./donorSlice";

export interface Donor {
  name: string;
  amount: number;
  returning: boolean;
  email: string;
}

interface DonorProp {
  donors: Donor[];
}

const Donors: React.FC<DonorProp> = ({ donors }) => {
  return (
    <ul>
      {donors.map((donor) => (
        <li key={donor.name}>
          {donor.name}
          {donor.email}
          {donor.returning ? "returning" : "new"}
        </li>
      ))}
    </ul>
  );
};

interface PaginationProp {
  donorsPerPage: number;
  totalDonors: number;
  paginate: Function;
}

const Pagination: React.FC<PaginationProp> = ({
  donorsPerPage,
  totalDonors,
  paginate,
}) => {
  const pageNumbers = [];

  for (let i = 1; i <= Math.ceil(totalDonors / donorsPerPage); i++) {
    pageNumbers.push(i);
  }

  return (
    <nav>
      <ul>
        {pageNumbers.map((number) => (
          <li key={number}>
            <a onClick={() => paginate(number)} href="!#">
              {number}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
};

const DonorPage: React.FC = () => {
  const donors = useAppSelector(selectDonors);
  const dispatch = useAppDispatch();
  useEffect(() => {
    dispatch(getDonors());
  }, [dispatch]);

  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);

  const [donorsPerPage, setDonorsPerPage] = useState(15);

  const indexOfLastDonor = currentPage * donorsPerPage;
  const indexOfFirstDonor = indexOfLastDonor - donorsPerPage;
  const currentDonors = donors.slice(indexOfFirstDonor, indexOfLastDonor);

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber);

  return (
    <div>
      <Donors donors={currentDonors} />
      <Pagination
        donorsPerPage={donorsPerPage}
        totalDonors={donors.length}
        paginate={paginate}
      />
    </div>
  );
};

export default DonorPage;
