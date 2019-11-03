import React, { Component } from "react";
import SearchBar from "./SearchBar";
import DATA from "./data.json";

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
    var articles = DATA.articles;
    if (articles[0].query.toLowerCase() == searchVal.toLowerCase()) {
      var dict = {};
      var counts = {};
      articles.forEach(calculate);

      function calculate(value) {
        if (value.source in dict) {
          dict[value.source] += value.sentiment;
          counts[value.source] += 1;
        } else {
          dict[value.source] = value.sentiment;
          counts[value.source] = 1;
        }
      }
      var average = {};
      for(var key in dict) {
        average[key] = dict[key] / counts[key];
      }

      console.log(average);
    } else {
      console.log("invalid query");
    }
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
