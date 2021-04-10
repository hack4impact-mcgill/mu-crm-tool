import React from 'react'
import { BrowserRouter as Router } from 'react-router-dom'
import { Routes } from './routes'
import NavBar from './components/common/navbar'

const App = () => {
    return (
        <React.Fragment>
            <Router>
                <NavBar />
                <Routes />
            </Router>
        </React.Fragment>
    )
}


export default App
