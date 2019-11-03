import React, { Component } from "react";
import SearchBar from "./SearchBar";

export default class Master_Detail extends Component {
  constructor(props) {
    super(props);

    // this.state = {
    //   currentDisplayTabIndex: 0,
    //   masterDetailText: [
    //     {
    //       shortDescription: "",
    //       longDescription: "",
    //       title: "",
    //       status: "",
    //       shipTo: "",
    //       orderTotal: 0.0,
    //       orderDate: "",
    //       id: 0
    //     }
    //   ]
    // };
  }

  // Get the sample data from the back end
  // componentDidMount() {
  // }

  // handleWarningClose() {
  // }

  onSubmit = (searchVal) => {
    alert(searchVal);
    console.log(searchVal);
  } 

  render() {
    return (
      <main id="mainContent">
        <SearchBar submitCallBack={this.onSubmit}></SearchBar>
      </main>
    );
  }
}
