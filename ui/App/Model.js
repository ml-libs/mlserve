import "whatwg-fetch";
import React, { Component } from "react";
import {
  Button,
  Card,
  CardText,
  CardTitle,
  CardBody,
  Collapse,
  Container,
  FormGroup
} from "reactstrap";
import Form from "react-jsonschema-form";
import {
  XAxis,
  YAxis,
  VerticalGridLines,
  HorizontalGridLines,
  LineMarkSeries,
  DiscreteColorLegend,
  FlexibleWidthXYPlot
} from "react-vis";

const reformatPlot = (target, rawPlot) =>
  target.map(t => [t, rawPlot.map((pl, idx) => ({ y: pl[t], x: idx }))]);

export default class Model extends Component {
  state = {
    model: {
      schema: { schema: {}, ui_schema: {}, example_data: {} },
      description: "",
      target: []
    },
    predictions: [],
    plot: [],
    collapse: false,
    counter: 0
  };
  modelName = this.props.match.params.modelName;

  fetchStats = () => {
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
  };

  componentDidMount() {
    this.fetchStats();
  }

  handleSubmit = data => {
    fetch(`/api/v1/models/${this.modelName}/predict`, {
      method: "POST",
      body: JSON.stringify([data.formData])
    })
      .then(response => response.text())
      .then(jsonData => JSON.parse(jsonData))
      .then(payload => {
        const point = payload[0];
        this.setState({
          predictions: payload[0],
          plot: [...this.state.plot, point]
        });
      });
  };

  handleChange = data => {
    this.setState({ formData: data.formData });
  };

  handleError = err => {
    console.log(err);
  };

  toggle = () => {
    this.setState({ collapse: !this.state.collapse });
  };

  render() {
    return (
      <Container>
        <React.Fragment>
          <h2>Model {this.modelName}</h2>
          <p>Model {this.state.model.description}</p>
          <div>
            <FlexibleWidthXYPlot height={300}>
              <VerticalGridLines />
              <HorizontalGridLines />
              <XAxis />
              <YAxis />

              {reformatPlot(this.state.model.target, this.state.plot).map(
                item => {
                  const [_, series] = item;
                  return (
                    <LineMarkSeries
                      className="linemark-series-example"
                      style={{ strokeWidth: "1px" }}
                      data={series}
                    />
                  );
                }
              )}
            </FlexibleWidthXYPlot>
          </div>
          <div className="legend">
            <DiscreteColorLegend items={this.state.model.target} />
          </div>
          <p>
            <Button color="primary" onClick={this.toggle}>
              curl example
            </Button>
          </p>
          <Collapse isOpen={this.state.collapse}>
            <Card>
              <CardBody>
                <CardText>
                  <code>
                    curl --header "Content-Type: application/json" --request
                    POST --data '[{JSON.stringify(
                      this.state.model.schema.example_data
                    )}]' {window.location.origin}/api/v1/models/{this.modelName}/predict
                  </code>
                </CardText>
              </CardBody>
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
            onError={this.handleError}
          />
          <Card>
            <CardBody>
              <CardTitle>{this.state.model.target.join(", ")}</CardTitle>
              <CardText>{JSON.stringify(this.state.predictions)}</CardText>
            </CardBody>
          </Card>
        </React.Fragment>
      </Container>
    );
  }
}
