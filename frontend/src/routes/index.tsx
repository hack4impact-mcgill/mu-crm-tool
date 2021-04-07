import loadable from '@loadable/component'
import React from 'react'
import { Route, Switch } from 'react-router-dom'

export enum RouteName {
    HOME = '/'
}


const Home = loadable(() => import('../components/pages/home'), {
    fallback: <div>Loading...</div>
})

export const Routes: React.FC = () => {
    return (
        <React.Fragment>
            <Switch>
                <Route path={RouteName.HOME}>
                    <Home />
                </Route>
            </Switch>
        </React.Fragment>
    )
}
                        
