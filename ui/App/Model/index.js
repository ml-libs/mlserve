import "whatwg-fetch";
import React, { Component } from "react";
import {
  Badge,
  Container,
  Row,
  Col
} from "reactstrap";
import Form from "react-jsonschema-form";

function ObjectFieldTemplate({ TitleField, properties, title, description }) {
  return (
    <div>
      <TitleField title={title} />
      <div className="row">
        {properties.map(prop => (
          <div
            className="col-lg-2 col-md-4 col-sm-6 col-xs-12"
            key={prop.content.key}
          >
            {prop.content}
          </div>
        ))}
      </div>
      {description}
    </div>
  );
}

const log = type => console.log.bind(console, type);
export default class Model extends Component {
  constructor(props) {
    super(props);

    this.state = { model: { schema: {}, description: "" } };
    this.handleFetch = this.handleFetch.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.modelName = props.match.params.modelName;
  }

  fetchStats() {
    fetch(`/api/v1/models/${this.modelName}`, {
      method: "GET"
    })
      .then(response => response.text())
      .then(jsonData => JSON.parse(jsonData))
      .then(data => {
        this.setState({
          model: data
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

  handleSubmit(data) {
    fetch(`/api/v1/models/${this.modelName}/predict`, {
      method: "POST",
      body: JSON.stringify([data.formData])
    })
      .then(response => response.text())
      .then(jsonData => JSON.parse(jsonData))
      .then(data => {
        this.setState({
          predictions: data[0]
        });
      });
  }

  render() {
    return (
      <div>
        <Container>
          <Row>
            <Col>
              <h2> Model {this.modelName}</h2>
              <p> Model {this.state.model.description || ""}</p>
              <Form
                schema={this.state.model.schema || {}}
                onChange={log("changed")}
                onSubmit={this.handleSubmit}
                onError={log("errors")}
                ObjectFieldTemplate={ObjectFieldTemplate}
              />
            </Col>
          </Row>
          <p> {JSON.stringify(this.state.predictions)}</p>
        </Container>
      </div>
    );
  }
}
