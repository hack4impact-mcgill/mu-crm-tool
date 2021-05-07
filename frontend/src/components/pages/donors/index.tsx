import React, { useState, useEffect } from "react";

function clickMe() {
  alert("You clicked me!");
}
const DonorPage: React.FC = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);

  const [postsPerPage, setPostsPerPage] = useState(10);

  //setPosts(data here)

  return (
    <div>
      <button onClick={clickMe}>Button</button>
    </div>
  );
};

export default DonorPage;
