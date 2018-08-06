import ReactDOM from "react-dom";
import React, { Component } from "react";
import { BrowserRouter } from "react-router-dom";
import {
  Container
} from "reactstrap";

import Form from "react-jsonschema-form";
import "bootstrap/dist/css/bootstrap.min.css";

import MainNav from "./MainNav";
import Main from "./Main";

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div>
          <MainNav/>
          <Main/>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
ReactDOM.render(<App />, document.getElementById("app"));
