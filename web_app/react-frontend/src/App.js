import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Selection from './components/Selection';
import Details from './components/Details';

class App extends Component {
    
  constructor(props) {
    super(props);
    this.state = {
        retrievedData: []
    };
  }
    
  handlePrediction = (data) => {
      this.setState({retrievedData: data});
  }
  
  render() {
    return (
      <div className="main-app">
        <nav className="App-header">
            <img src={logo} className="App-logo"></img>
            <span className="App-title">Deforestation - Image Recognition</span>
        </nav>
        <div className="container">
            <div className="row">
                <div className="col-sm-5">
                    <Selection onRetrieveData={this.handlePrediction}/>
                </div>
                <div className="col-sm-7">
                    <Details hasData={this.state.retrievedData}/>
                </div>
            </div>
        </div>
      </div>
    );
  }
}

export default App;
