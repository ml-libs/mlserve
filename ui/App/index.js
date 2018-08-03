import ReactDOM from "react-dom";
import React, { Component } from "react";
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  Container,
  Row,
  Col,
  Jumbotron,
  Button,
  Card,
  CardImg,
  CardText,
  CardBody,
  CardLink,
  CardTitle,
  CardSubtitle,
  ListGroupItem,
  ListGroup
} from "reactstrap";

import "bootstrap/dist/css/bootstrap.min.css";

class App extends Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.state = {
      isOpen: false
    };
  }
  toggle() {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }
  render() {
    return (
      <div>
        <Navbar color="dark" dark expand="md">
          <NavbarBrand href="/"> mlserve</NavbarBrand>
          <NavbarToggler onClick={this.toggle} />
          <Collapse isOpen={this.state.isOpen} navbar>
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
          </Collapse>
        </Navbar>

        <Container>
          <Col>Server stats. Refresh</Col>
          <Row>
            <Col>
              <Card body className="text-center">
                <CardTitle>Requests</CardTitle>
                <CardText>
                  <h1>100</h1>
                </CardText>
              </Card>
            </Col>
            <Col>
              <Card body className="text-center">
                <CardTitle>Mean Response Time</CardTitle>
                <CardText>
                  <h1>100</h1>
                </CardText>
              </Card>
            </Col>
            <Col>
              <Card body className="text-center">
                <CardTitle>Errors</CardTitle>
                <CardText>
                  <h1>5</h1>
                </CardText>
              </Card>
            </Col>
          </Row>
          <Row>
            <Col>
              <h3> Models </h3>
              <ListGroup>
                <ListGroupItem> <NavLink href="/models/model1">model1</NavLink> target=target</ListGroupItem>
                <ListGroupItem> <NavLink href="/models/model2">model2</NavLink> </ListGroupItem>
                <ListGroupItem> <NavLink href="/models/model3">model3</NavLink> </ListGroupItem>
              </ListGroup>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default App;
ReactDOM.render(<App />, document.getElementById("app"));
