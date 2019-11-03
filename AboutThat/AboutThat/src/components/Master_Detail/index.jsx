import React, { Component } from "react";
import SearchBar from "./SearchBar";

class Master_Detail extends Component {
  constructor(props) {
    super();
    this.state = {
      search: 'default',
    };
  }

  // Get the sample data from the back end
  // componentDidMount() {
  // }

  // handleWarningClose() {
  // }

  onSubmit(searchVal) {
    this.setState({search: searchVal});
    alert(searchVal);
    console.log(searchVal);
  } 

  render() {
    return (
      <div style={{display: 'flexbox', flexdirection: 'column', background: 'black', height: '80vh', margin: '78px auto'}}>
        <h1 style={{color: 'white', textAlign: 'center', fontFamily: 'PT Sans Narrow', fontSize: '48px', position: 'relative', top: '200px'}}>See what people are saying about: </h1>
        <SearchBar submit={this.onSubmit.bind(this)}></SearchBar>
      </div>
    );
  }
}

export default Master_Detail;
