import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import * as serviceWorker from './serviceWorker';
import { Provider } from 'react-redux'
import { createStore, applyMiddleware } from 'redux'
import ReduxThunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'
import RootReduser from './redusers/RootReduser'
import {BrowserRouter, Route} from 'react-router-dom'
import SignUp from './containers/SignUp';
import SignIn from './containers/SignIn';
import DropPass from './containers/DropPass';


const store = createStore(
    RootReduser,
    composeWithDevTools(applyMiddleware(ReduxThunk))
);

ReactDOM.render(
<Provider store = {store}>
    <BrowserRouter>
        <Route path="/signup" component={SignUp} />
        <Route path="/signin" component={SignIn} />
        <Route path="/droppass" component={DropPass} />
    </BrowserRouter>
</Provider>, document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
