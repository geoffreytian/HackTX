import React from "react";
import './search.css';
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
      <form style={{fontSize: "25px", position: 'relative', top: '200px', left: '23%', width: '70%', color: 'white', fontFamily: 'PT Sans Narrow'}} onSubmit={this.handleSubmit}>
        <input type="text" style={{color: 'white'}} name="name" placeholder={this.state.value} onChange={this.handleChange} class="question" id="nme" required autocomplete="off" />
        <label for="nme"><span></span></label>
        <input type="submit" value="Submit!" />
      </form>
    );
  }
}

export default SearchBar;