import loadable from "@loadable/component";
import React from "react";
import { Route, Switch } from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import "./index.css";

export enum RouteName {
  LOGOUT = "/logout",
  USER = "/user",
  MAP = "/map",
  DONORS = "/donors",
  CONTACTS = "/contacts",
  HOME = "/",
}

const Home = loadable(() => import("../components/pages/home"), {
  fallback: <div>Loading...</div>,
});

const ContactPage = loadable(() => import("../components/pages/contacts"), {
  fallback: <CircularProgress />,
});

const DonorPage = loadable(() => import("../components/pages/donors"), {
  fallback: <CircularProgress />,
});

const MapPage = loadable(() => import("../components/pages/map"), {
  fallback: <CircularProgress />,
});

const UserPage = loadable(() => import("../components/pages/user"), {
  fallback: <CircularProgress />,
});

export const Routes: React.FC = () => {
  return (
    <div className="main">
      <Switch>
        <Route path={RouteName.LOGOUT}>
          <div>logout placeholder</div>
        </Route>
        <Route path={RouteName.USER}>
          <UserPage />
        </Route>
        <Route path={RouteName.MAP}>
          <MapPage />
        </Route>
        <Route path={RouteName.DONORS}>
          <DonorPage />
        </Route>
        <Route path={RouteName.CONTACTS}>
          <ContactPage />
        </Route>
        <Route path={RouteName.HOME}>
          <Home />
        </Route>
      </Switch>
    </div>
  );
};
