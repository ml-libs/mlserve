import "whatwg-fetch";
import React from "react";
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  UncontrolledDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem
} from "reactstrap";
import { Link } from "react-router-dom";

export default class MainNav extends React.Component {
  constructor(props) {
    super(props);

    this.handleFetch = this.fetchStats.bind(this);
    this.toggle = this.toggle.bind(this);
    this.state = {
      isOpen: false,
      models: []
    };
  }
  toggle() {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }

  fetchStats() {
    fetch("/api/v1/models", {
      method: "GET"
    })
      .then(response => response.text())
      .then(jsonData => JSON.parse(jsonData))
      .then(data => {
        this.setState({
          models: data
        });
      });
  }

  componentDidMount() {
    this.fetchStats();
  }

  render() {
    return (
      <div>
        <Navbar color="light" light expand="md">
          <NavbarBrand href="/">reactstrap</NavbarBrand>
          <NavbarToggler onClick={this.toggle} />
          <Collapse isOpen={this.state.isOpen} navbar>
            <Nav className="ml-auto" navbar>
              <NavItem>
                <NavLink href="https://mlserve.rtfd.com">Docs</NavLink>
              </NavItem>
              <NavItem>
                <NavLink href="https://github.com/jettify/mlserve">
                  GitHub
                </NavLink>
              </NavItem>
              <UncontrolledDropdown nav inNavbar>
                <DropdownToggle nav caret>
                  Models
                </DropdownToggle>
                <DropdownMenu right>
                  {this.state.models.map(model => {
                    return (
                      <DropdownItem>
                        <Link to={`/models/${model.name}`}>{model.name}</Link> {" "}
                      </DropdownItem>
                    );
                  })}
                </DropdownMenu>
              </UncontrolledDropdown>
            </Nav>
          </Collapse>
        </Navbar>
      </div>
    );
  }
}
