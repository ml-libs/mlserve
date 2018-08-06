import React, { Component } from "react";
import { Container } from "reactstrap";

import "bootstrap/dist/css/bootstrap.min.css";

import AggStats from "../AggStats";
import ModelsList from "../ModelsList";

class Home extends Component {
  render() {
    return (
      <div>
        <AggStats />
        <ModelsList />
      </div>
    );
  }
}

export default Home;
