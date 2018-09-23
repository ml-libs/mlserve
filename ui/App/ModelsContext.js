import React from "react";

const ModelsContext = React.createContext({});

class ModelsProvider extends React.Component {
  state = { models: [], target: [] };

  async componentDidMount() {
    const response = await fetch("/api/v1/models", { method: "GET" });
    const jsonData = await response.text();
    const data = JSON.parse(jsonData);
    this.setState({ models: data });
  }

  render() {
    return (
      <ModelsContext.Provider value={this.state.models}>
        {this.props.children}
      </ModelsContext.Provider>
    );
  }
}

const ModelsConsumer = ModelsContext.Consumer;
export { ModelsConsumer, ModelsProvider };
