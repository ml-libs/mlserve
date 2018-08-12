import "whatwg-fetch";
import React, { Component } from "react";
import {
  Badge,
  Container,
  Row,
  Col,
  Label,
  FormGroup,
  Card,
  CardText
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

    this.state = {
      model: {
        schema: { schema: {}, ui_schema: {}, example_data: {} },
        description: ""
      },
      predictions: []
    };
    this.handleFetch = this.handleFetch.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
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
          model: data,
          formData: data.schema.example_data
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

  handleChange(data) {
    this.setState({ formData: data.formData });
  }

  render() {
    return (
      <div>
        <Container>
          <Row>
            <Col>
              <h2> Model {this.modelName}</h2>
              <p> Model {this.state.model.description || ""}</p>
              <h2>Predict With Command Line</h2>
              Just copy following <i>curl</i> command and excute in your
              terminal:
              <Card body>
                <CardText>
                  <code>
                    curl --header "Content-Type: application/json" --request
                    POST --data '[{JSON.stringify(
                      this.state.model.schema.example_data
                    )}]' {window.location.origin}/api/v1/models/{this.modelName}/predict
                  </code>
                </CardText>
              </Card>
              <FormGroup />
              <h2>Predict With WEB UI</h2>
              <Form
                schema={this.state.model.schema.schema || {}}
                uiSchema={this.state.model.schema.ui_schema || {}}
                formData={this.state.formData || {}}
                onChange={this.handleChange}
                onSubmit={this.handleSubmit}
                onError={log("errors")}
                ObjectFieldTemplate={ObjectFieldTemplate}
              />
              <Card body>
                <CardText>{JSON.stringify(this.state.predictions)}</CardText>
              </Card>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}
