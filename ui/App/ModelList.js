import "whatwg-fetch";
import React, { Component } from "react";
import { ListGroupItem, ListGroup, Badge, Container } from "reactstrap";
import { Link } from "react-router-dom";
import { ModelsConsumer } from "./ModelsContext";

export default class ModelsList extends Component {
  render() {
    return (
      <Container>
        <h2>Available Models</h2>
        <ListGroup>
          <ModelsConsumer>
            {models =>
              models.map(model => (
                <ListGroupItem>
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center"
                    }}
                  >
                    <Link to={`/models/${model.name}`}>{model.name}</Link>
                    <Badge color="secondary">{model.target.join(", ")}</Badge>
                  </div>
                </ListGroupItem>
              ))
            }
          </ModelsConsumer>
        </ListGroup>
      </Container>
    );
  }
}
