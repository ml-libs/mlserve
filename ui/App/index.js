import ReactDOM from "react-dom";
import React, { Component } from "react";
import {
  Navbar,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  Container
} from "reactstrap";

import Form from "react-jsonschema-form";
import "bootstrap/dist/css/bootstrap.min.css";

import AggStats from "./AggStats";
import ModelsList from "./ModelsList";

class App extends Component {
  render() {
    return (
      <div>
        <Navbar color="dark" dark expand="md">
          <NavbarBrand href="/"> mlserve</NavbarBrand>
          <Nav className="ml-auto" navbar>
            <NavItem>
              <NavLink href="/components/">Components</NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="https://github.com/jettify/mlserve">
                Github
              </NavLink>
            </NavItem>
          </Nav>
        </Navbar>
        <AggStats />
        <Container>
          <ModelsList />
        </Container>
      </div>
    );
  }
}

export default App;
ReactDOM.render(<App />, document.getElementById("app"));
