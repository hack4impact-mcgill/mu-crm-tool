import React, { useState } from "react";
import { NavLink, Route } from "react-router-dom";
import { ReactComponent as Logo } from "../../../shared/icons/logo.svg";
import { ReactComponent as Avatar } from "../../../shared/icons/avatar.svg";
import { ReactComponent as BoldAvatar } from "../../../shared/icons/bold_avatar.svg";
import { ReactComponent as Burger } from "../../../shared/icons/burger.svg";
import "./index.css";

const NavBar: React.FC = () => {
  const [showNav, setShowNav] = useState(false);
  return (
    <nav className="navbar">
      <div className="sm-navbar">
        <Burger className="burger" onClick={() => setShowNav(!showNav)} />
        <Logo className="logo" />
        <div className="sm-avatar-logout">
          <NavLink
            key={"User"}
            to={"/user"}
            className="nav-link"
            activeClassName="selected"
            exact
          >
            <Route
              path={"/user"}
              children={({ match }) => {
                return match ? <BoldAvatar /> : <Avatar />;
              }}
            />
          </NavLink>
          <NavLink
            key={"logout"}
            to={"/logout"}
            className="nav-link"
            activeClassName="selected"
            exact
          >
            Logout
          </NavLink>
        </div>
      </div>
      <ul className={"navbar-nav" + (showNav ? " show" : "")}>
        <li className="nav-item">
          <NavLink
            to={"/"}
            className="nav-link"
            activeClassName="selected"
            exact
          >
            Home
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink
            to={"/contacts"}
            className="nav-link"
            activeClassName="selected"
            exact
          >
            Contacts
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink
            to={"/donors"}
            className="nav-link"
            activeClassName="selected"
            exact
          >
            Donors
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink
            to={{ pathname: "https://mumap.xyz/" }}
            target="_blank"
            className="nav-link"
            activeClassName="selected"
            exact
          >
            Map
          </NavLink>
        </li>
      </ul>
      <div className="lg-avatar-logout">
        <NavLink
          key={"User"}
          to={"/user"}
          className="nav-link"
          activeClassName="selected"
          exact
        >
          <Route
            path={"/user"}
            children={({ match }) => {
              return match ? <BoldAvatar /> : <Avatar />;
            }}
          />
        </NavLink>
        <NavLink
          key={"logout"}
          to={"/logout"}
          className="nav-link"
          activeClassName="selected"
          exact
        >
          Logout
        </NavLink>
      </div>
    </nav>
  );
};

export default NavBar;
