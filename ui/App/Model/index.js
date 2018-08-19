import "whatwg-fetch";
import React, { Component } from "react";
import {
  Badge,
  Button,
  Card,
  CardText,
  CardTitle,
  Col,
  Collapse,
  Container,
  FormGroup,
  Label,
  Row
} from "reactstrap";
import Form from "react-jsonschema-form";


const log = type => console.log.bind(console, type);
export default class Model extends Component {
  constructor(props) {
    super(props);

    this.state = {
      model: {
        schema: { schema: {}, ui_schema: {}, example_data: {} },
        description: "",
        target: [],
      },
      predictions: [],
      collapse: false,
    };
    this.handleFetch = this.handleFetch.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.modelName = props.match.params.modelName;
    this.toggle = this.toggle.bind(this);
  }

  fetchStats() {
    fetch(`/api/v1/models/${this.modelName}`, {
      method: "GET"
    })
      .then(response => response.text())
      .then(jsonData => JSON.parse(jsonData))
      .then(payload => {
        this.setState({
          model: payload,
          formData: payload.schema.example_data
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

  toggle() {
    this.setState({ collapse: !this.state.collapse });
  }

  render() {
    return (
      <div>
        <Container>
          <Row>
            <Col>
              <h2>Model {this.modelName}</h2>
              <p>Model {this.state.model.description}</p>
              <Button
                color="primary"
                onClick={this.toggle}
              >
                curl example
              </Button>
              <Collapse isOpen={this.state.collapse}>
                <Card body>
                  <CardText>
                    <code>
                      curl --header "Content-Type: application/json" --request
                      POST --data '[{JSON.stringify(
                        this.state.model.schema.example_data
                      )}]' {window.location.origin}/api/v1/models/{
                        this.modelName
                      }/predict
                    </code>
                  </CardText>
                </Card>
              </Collapse>

              <FormGroup />
              <h2>Predict With WEB UI</h2>
              <Form
                schema={this.state.model.schema.schema || {}}
                uiSchema={this.state.model.schema.ui_schema || {}}
                formData={this.state.formData || {}}
                onChange={this.handleChange}
                onSubmit={this.handleSubmit}
                onError={log("errors")}
              />
              <Card body>
                <CardTitle>{this.state.model.target.join(", ")}</CardTitle>
                <CardText>{JSON.stringify(this.state.predictions)}</CardText>
              </Card>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}
