import React from "react";
import Logo from "./logo.png";

// import styled from "styled-components";

export default class LogIn extends React.Component {
  state = {
    // as people type in the form, update the state, have the changes reflected in the form
    firstName: "", // default value
    lastName: "", // value is set, so won't let you change it
    username: "",
    email: "",
    password: "",
  };

  // change function, accepts e
  // code for coherency
  change = (e) => {
    this.props.onChange({ [e.target.name]: e.target.value });
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  onSubmit = (e) => {
    e.preventDefault(); // acts with the http address, ensures changes aren't logged to there
    //this.props.onSubmit(this.state);
    this.setState({
      // as people type in the form, update the state, have the changes reflected in the form
      username: "",
      email: "",
      password: "",
    });

    // code for coherency (can remove)
    this.props.onChange({
      // as people type in the form, update the state, have the changes reflected in the form
      username: "",
      email: "",
      password: "",
    });
  };

  render() {
    return (
      // use materialUI here
      // label defined elsewhere (in index.css)

      <form>
        <img src={Logo} height="70" width="100" alt="" />
        <label></label>
        <br />
        <label>
          <input
            name="email"
            placeholder="Email"
            value={this.state.email}
            onChange={(e) => this.change(e)}
          />
        </label>
        <label>
          <input
            name="password"
            type="password"
            placeholder="Password"
            value={this.state.password}
            onChange={(e) => this.change(e)}
          />
        </label>
        <button color="#00000" onClick={(e) => this.onSubmit(e)}>
          Submit
        </button>
      </form>
    );
  }
}
