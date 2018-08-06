import React from "react";
import { Switch, Route } from "react-router-dom";
import Home from "../Home";
import Model from "../Model";
import ModelsList from "../ModelsList";

const Main = () => (
  <main>
    <Switch>
      <Route exact path="/" component={Home} />
      <Route exact path="/models" component={ModelsList} />
      <Route path="/models/:modelName" component={Model} />
    </Switch>
  </main>
);

export default Main;
