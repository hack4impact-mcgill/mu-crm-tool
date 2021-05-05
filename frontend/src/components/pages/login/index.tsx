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
    <form
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <Logo className="logo" />
      <br />
      <input
        name="email"
        placeholder="Email"
        value={email}
        onChange={(e) => onEmailChange(e)}
      />
      <input
        name="password"
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => onPasswordChange(e)}
      />
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
