import React, { Component } from "react";
import SearchBar from "./SearchBar";
import DATA from "./data.json";
import Graph from "./graph.jsx";

class Master_Detail extends Component {
  constructor(props) {
    super(props);
    this.state = {
      search: 'default',
      graph: 'false',
      data: {},
      chartData: {},
      seed: 6
    };
    this.getChartData.bind(this);
  }

  
 
// in order to work 'Math.seed' must NOT be undefined,
// so in any case, you HAVE to provide a Math.seed
  seededRandom = function(max, min) {
      max = max || 1;
      min = min || 0;
      var temp = this.state.seed;
      var seed = (temp * 9301 + 49297) % 233280;
      var rnd = seed / 233280;
      this.setState({seed: temp*20})
      return min + rnd * (max - min);
  }
  getChartData () {
    var news = Object.keys(this.state.data);
    var sentimentValues = Object.values(this.state.data);
    var colors = [];
    for (var i = 0; i < news.length; i++) {
      var r = Math.floor(this.seededRandom(0, 256));          // Random between 0-255
      var g = Math.floor(this.seededRandom(0, 256));           // Random between 0-255
      var b = Math.floor(this.seededRandom(0, 256));           // Random between 0-255
      var a = 0.8;
      var rgba = 'rgba(' + r + ', ' + g + ', ' + b + ', ' + a +')'; // Collect all to a string
      colors.push(rgba);
    }

    

    this.setState({
      chartData: {
				labels: news.map(function(x){ return x.toUpperCase()}),
				datasets: [
					{
						label: 'Sentiment',
						data: sentimentValues,
						backgroundColor: colors
					}
				]
      },
      graph: 'true'
    });
    // this.componentDidUpdate("chartData").bind(this);
  }

  // componentDidUpdate(type) {
  //   if (type === "chartData") {
  //     console.log(this.state.ch)
  //   }
  // }
  // Get the sample data from the back end
  // componentDidMount() {
  // }

  // handleWarningClose() {
  // }

  async onSubmit(searchVal) {
    // const Http = new XMLHttpRequest();
    // const url='https://cors-anywhere.herokuapp.com/http://getsentiment.azurewebsites.net/api/getSentimentScores?code=eqw4D4mESqPNR1El1RGXuCXhsaLyZvXVyxGjdQe5iop1/HQrMmwwgg==&name=Aman';
    // Http.open("GET", url);
    // Http.send();
    // Http.onreadystatechange = (e) => {
    //   console.log(Http.responseText)
    // }

    var queries = DATA.by_query;
    var articles;
    for (var i = 0; i < queries.length; i++) {
      if (queries[i].query.toLowerCase() === searchVal.toLowerCase()) {
        articles = queries[i].articles;
        break;
      }
    }

    if (articles[0].query.toLowerCase() === searchVal.toLowerCase()) {
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
        average[key] = (dict[key] / counts[key]).toFixed(2);
      }
      await this.setState({data: average});
      await this.getChartData();
    } else {
      console.log("invalid query");
    }
  } 

  render() {
    console.log(this.state.graph);
    console.log(this.state.chartData);
    if (this.state.graph === 'false' || this.state.chartData == undefined) {
      return (
        <div style={{display: 'flexbox', flexdirection: 'column', background: 'black', height: '80vh', margin: '78px auto'}}>
          <h1 style={{color: 'white', textAlign: 'center', fontFamily: 'PT Sans Narrow', fontSize: '48px', position: 'relative', top: '200px'}}>See what people are saying about: </h1>
          <SearchBar submit={this.onSubmit.bind(this)}></SearchBar>
        </div>
      );
    } else {
      return (
        <div style={{display: 'flexbox', flexdirection: 'column', background: 'black', height: '100vh', margin: '78px auto'}}>
          <div style={{position: 'relative', top: '100px'}}>
            <Graph data={this.state.chartData}/>
          </div>
          <SearchBar submit={this.onSubmit.bind(this)} style={{position: 'static'}}></SearchBar>
        </div>
      );   
    }
    
  }
}

export default Master_Detail;
