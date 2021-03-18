import loadable from '@loadable/component'
import React from 'react'
import { Route, Switch } from 'react-router-dom'

export enum RouteName {
    HOME = '/',
    PROJECTS = '/projects'
}


const Home = loadable(() => import('../components/pages/home'), {
    fallback: <div>Loading...</div>
})

const Projects = loadable(() => import('../components/pages/projects'), {
    fallback: <div>Loading...</div>
})


export const Routes: React.FC = () => {
    return (
        <React.Fragment>
            <Switch>
                <Route exact path={RouteName.HOME}>
                    <Home />
                </Route>

                <Route path={RouteName.PROJECTS}>
                    <Projects />
                </Route>
            </Switch>
        </React.Fragment>
    )
}
                        
