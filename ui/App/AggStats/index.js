import "whatwg-fetch";
import React, { Component } from "react";
import {
  Container,
  Row,
  Col,
  Button,
  Card,
  CardImg,
  CardText,
  CardBody,
  CardLink,
  CardTitle
} from "reactstrap";

export default class AggStats extends Component {
  constructor(props) {
    super(props);

    this.state = {
      success: 0,
      error: 0,
      mean_resp_time: 0
    };
    this.handleFetch = this.handleFetch.bind(this);
  }

  fetchStats() {
    fetch("/api/v1/agg_stats", {
      method: "GET"
    })
      .then(response => response.text())
      .then(jsonData => JSON.parse(jsonData))
      .then(data => {
        this.setState({
          success: data.success,
          error: data.error,
          mean_resp_time: data.mean_resp_time
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
      <Container>
        <Col>
          Server stats.{" "}
          <Button color="link" onClick={this.handleFetch}>
            Refresh
          </Button>
        </Col>
        <Row>
          <Col>
            <Card body className="text-center">
              <CardTitle>Succeses</CardTitle>
              <CardText>
                <h1>{this.state.success}</h1>
              </CardText>
            </Card>
          </Col>
          <Col>
            <Card body className="text-center">
              <CardTitle>Mean Response Time</CardTitle>
              <CardText>
                <h1>{this.state.mean_resp_time}</h1>
              </CardText>
            </Card>
          </Col>
          <Col>
            <Card body className="text-center">
              <CardTitle>Errors</CardTitle>
              <CardText>
                <h1>{this.state.error}</h1>
              </CardText>
            </Card>
          </Col>
        </Row>
      </Container>
    );
  }
}
