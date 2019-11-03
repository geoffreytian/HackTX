import React from "react";
// import classnames from "classnames";
// import PropTypes from 'prop-types';

class SearchBar extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      value: "Search...",
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    this.props.submit(this.state.value);
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
          <input type="text" placeholder={this.state.value} onChange={this.handleChange} style={{fontSize: "25px", width: "90%"}} id="searchInput"/>
          <input type="submit" value="Go!" style={{fontSize: "25px", width: "10%"}} id="submitSearch"/>
      </form>
    );
  }
}

export default SearchBar;