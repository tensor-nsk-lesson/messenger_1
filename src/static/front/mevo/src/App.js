import React from 'react';
import {BrowserRouter, Route} from 'react-router-dom'
import { connect } from 'react-redux'
import { personsFetchData } from './actions/persons'
import SignUp from './containers/SignUp';
import SignIn from './containers/SignIn';
import DropPass from './containers/DropPass';

class  App extends React.Component {


  render(){
    return(
      <BrowserRouter>
          <Route path="/signup" component={SignUp} />
          <Route path="/signin" component={SignIn} />
          <Route path="/droppass" component={DropPass} />
      </BrowserRouter>
    );
  }
}

const mapStateToProps = state => {
  return {
    persons: state.persons
  };
};

const mapDispatchToProps = dispatch => {
  return {
    fetchData: url => dispatch(personsFetchData(url))
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(App);
