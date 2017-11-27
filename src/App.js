import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentWillMount() {
    fetch('skidom-api.herokuapp.com/api/resorts')
      .then(response => {
        var contentType = response.headers.get("content-type");
        if(contentType && contentType.includes("application/json")) {
          return response.json();
        }
        throw new TypeError("Oops, we haven't got JSON!")
      })
      .then(json => {
        this.setState({
          resorts: json
        });
      });
  };

  render() {
    console.log(this.state);
    const resorts = this.state.resorts
      ? this.state.resorts.toString()
      : '';
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
          { resorts }
        </p>
      </div>
    );
  }
}

export default App;
