import { combineReducers } from 'redux'
import reg from './reg'
import auth from './auth'

const RootReduser = combineReducers({
    reg,
    auth
});

export default RootReduser;