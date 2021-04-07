import { combineReducers } from 'redux'
import homeReducer from '../components/pages/home/homeSlice'

export default combineReducers({
    home: homeReducer,
})
