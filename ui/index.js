import "babel-polyfill";
import ReactDOM from "react-dom";
import React from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import "bootstrap/dist/css/bootstrap.min.css";

import AppHeader from "./App/AppHeader";
import Home from "./App/Home";
import Model from "./App/Model";
import { ModelsProvider } from "./App/ModelsContext";

const App = () => (
  <ModelsProvider>
    <AppHeader />
    <Switch>
      <Route exact path="/" component={Home} />
      <Route path="/models/:modelName" component={Model} />
    </Switch>
  </ModelsProvider>
);

ReactDOM.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>,
  document.getElementById("app")
);
