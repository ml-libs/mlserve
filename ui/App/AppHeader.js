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
import { withRouter } from "react-router-dom";
import { ModelsConsumer } from "./ModelsContext";

export default withRouter(
  class AppHeader extends React.Component {
    state = {
      isOpen: false,
      models: []
    };

    toggle = () => {
      this.setState({
        isOpen: !this.state.isOpen
      });
    };

    handleModelSelect = (modelName) => {
      this.props.history.push(`/models/${modelName}`);
    };

    render() {
      return (
        <header>
          <Navbar color="dark" dark expand="md">
            <NavbarBrand href="/">mlserve</NavbarBrand>
            <NavbarToggler onClick={this.toggle} />
            <Collapse isOpen={this.state.isOpen} navbar>
              <Nav className="ml-auto" navbar>
                <NavItem>
                  <NavLink href="https://mlserve.rtfd.com">Docs</NavLink>
                </NavItem>
                <NavItem>
                  <NavLink href="https://github.com/ml-libs/mlserve">
                    GitHub
                  </NavLink>
                </NavItem>
                <UncontrolledDropdown nav inNavbar>
                  <DropdownToggle nav caret>
                    Models
                  </DropdownToggle>
                  <DropdownMenu right>
                    <ModelsConsumer>
                      {models =>
                        models.map(model => (
                          <DropdownItem
                            onClick={() => this.handleModelSelect(model.name)}
                          >
                            {model.name}
                          </DropdownItem>
                        ))
                      }
                    </ModelsConsumer>
                  </DropdownMenu>
                </UncontrolledDropdown>
              </Nav>
            </Collapse>
          </Navbar>
        </header>
      );
    }
  }
);
