import "whatwg-fetch";
import React, { Component } from "react";
import { Container, Row, Col, Button, Card, CardTitle } from "reactstrap";

export default class AggStats extends Component {
  state = {
    success: 0,
    error: 0,
    mean_resp_time: 0
  };

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

  handleFetch = event => {
    event.preventDefault();
    this.fetchStats();
  };

  componentDidMount() {
    this.fetchStats();
  }

  render() {
    return (
      <Container style={{ marginBottom: 8 }}>
        <Button color="link" onClick={this.handleFetch}>
          Refresh
        </Button>
        <Row>
          <Col
            sm="12"
            md="4"
            lg="4"
            xl="4"
            size="auto"
            style={{ marginBottom: 8 }}
          >
            <Card body className="text-center">
              <CardTitle>Successes</CardTitle>
              <h1>{this.state.success}</h1>
            </Card>
          </Col>
          <Col
            sm="12"
            md="4"
            lg="4"
            xl="4"
            size="auto"
            style={{ marginBottom: 8 }}
          >
            <Card body className="text-center">
              <CardTitle>Mean Response Time</CardTitle>
              <h1>{this.state.mean_resp_time}</h1>
            </Card>
          </Col>
          <Col
            sm="12"
            md="4"
            lg="4"
            xl="4"
            size="auto"
            style={{ marginBottom: 8 }}
          >
            <Card body className="text-center">
              <CardTitle>Errors</CardTitle>
              <h1>{this.state.error}</h1>
            </Card>
          </Col>
        </Row>
      </Container>
    );
  }
}
