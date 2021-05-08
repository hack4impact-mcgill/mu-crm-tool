import { combineReducers } from "redux";
import homeReducer from "../components/pages/home/homeSlice";
import donorReducer from "../components/pages/donors/donorSlice";

export default combineReducers({
  home: homeReducer,
  donor: donorReducer,
});
