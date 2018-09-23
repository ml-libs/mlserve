import React from "react";

import "bootstrap/dist/css/bootstrap.min.css";

import AggStats from "./AggStats";
import ModelList from "./ModelList";

const Home = () => {
  return (
    <React.Fragment>
      <AggStats />
      <ModelList />
    </React.Fragment>
  );
};

export default Home;
