import React, { useState } from "react";
import { ReactComponent as Logo } from "../../../shared/icons/logo.svg";

const LogInPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onEmailChange = (e: any) => {
    setEmail(e.target.value);
  };

  const onPasswordChange = (e: any) => {
    setPassword(e.target.value);
  };

  const onSubmit = (e: any) => {
    e.preventDefault();
    setEmail("");
    setPassword("");
  };

  return (
    <form>
      <Logo className="logo" />
      <label></label>
      <br />
      <label>
        <input
          name="email"
          placeholder="Email"
          value={email}
          onChange={(e) => onEmailChange(e)}
        />
      </label>
      <label>
        <input
          name="password"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => onPasswordChange(e)}
        />
      </label>
      <button color="#00000" onClick={(e) => onSubmit(e)}>
        Submit
      </button>{" "}
      <p
        onClick={() => {
          console.log("");
        }}
        style={{ fontSize: "10px" }}
      >
        <u>Forgot your password?</u>
      </p>
    </form>
  );
};

export default LogInPage;
