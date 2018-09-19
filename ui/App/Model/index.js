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

import "../../../node_modules/react-vis/dist/style.css";
import {
  XYPlot,
  XAxis,
  YAxis,
  VerticalGridLines,
  HorizontalGridLines,
  LineMarkSeries,
  DiscreteColorLegend,
  FlexibleWidthXYPlot
} from "react-vis";

const reformatPlot = function(target, rawPlot) {
  return target.map(function(t) {
    return [
      t,
      rawPlot.map(function(pl, idx) {
        return { y: pl[t], x: idx };
      })
    ];
  });
};

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

  handleFetch = (event) => {
    event.preventDefault();
    this.fetchStats();
  };

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
      .then(payload => {
        const point = payload[0];
        this.setState({
          predictions: payload[0],
          plot: [...this.state.plot, point]
        });
      });
  }

  handleChange = (data) => {
    this.setState({ formData: data.formData });
  };

  handleError = (err) => {
    console.log(err);
  };

  toggle = () => {
    this.setState({ collapse: !this.state.collapse });
  };

  render() {
    return (
      <div>
        <Container>
          <Row>
            <Col>
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
              <Button color="primary" onClick={this.toggle}>
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
                onError={this.handleError}
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
