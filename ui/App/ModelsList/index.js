import "whatwg-fetch";
import React, { Component } from "react";
import { ListGroupItem, ListGroup, Badge } from "reactstrap";

export default class ModelsList extends Component {
  constructor(props) {
    super(props);

    this.state = { models: [] };
    this.handleFetch = this.handleFetch.bind(this);
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

  handleFetch(event) {
    event.preventDefault();
    this.fetchStats();
  }
  componentDidMount() {
    this.fetchStats();
  }

  render() {
    return (
      <div>
        <h2> Available Models</h2>
        <ListGroup>
          {this.state.models.map(model => {
            return (
              <ListGroupItem>
                <a href="/models/{model.name}">{model.name}</a> predicts{" "}
                <Badge color="secondary">{model.target}</Badge>
              </ListGroupItem>
            );
          })}
        </ListGroup>
      </div>
    );
  }
}
