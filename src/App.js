import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {

  componentWillMount() {
    fetch('skidom.herokuapp.com/api/resorts').then(results => {
      this.setState({
        results: results
      });
    });
  };

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
          { this.state.results.toString() }
        </p>
      </div>
    );
  }
}

export default App;
