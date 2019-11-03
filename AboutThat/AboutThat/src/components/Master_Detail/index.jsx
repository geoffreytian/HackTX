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
      <div>
        <SearchBar submit={this.onSubmit.bind(this)}></SearchBar>
      </div>
    );
  }
}

export default Master_Detail;
