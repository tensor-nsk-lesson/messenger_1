import { combineReducers } from 'redux'
import { persons } from './persons'

const RootReduser = combineReducers({
    persons
});

export default RootReduser;