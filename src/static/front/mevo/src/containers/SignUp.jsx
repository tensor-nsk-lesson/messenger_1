import React from 'react';
import { connect } from 'react-redux'
import Header from '../components/Header'
import Foter from '../components/Footer'
import InputsForm from '../components/InputsForm'
import reg from '../actions/reg'


class SignUp extends React.Component { 
  constructor() {
    super()
    this.fname = {
      value: ''
    };
    this.sname = {
      value: ''
    };
    this.email = {
      value: ''
    };
    this.fpass = {
      value: ''
    };
    this.cpass = {
      value: ''
    };
  }

  handleChangeValueFname = e => this.setState({fname: e.target.value});
  handleChangeValueSname = e => this.setState({sname: e.target.value});
  handleChangeValueEmail = e => this.setState({email: e.target.value});
  handleChangeValueFpass = e => this.setState({fpass: e.target.value});
  handleChangeValueCpass = e => this.setState({cpass: e.target.value});

  RegData(e) {
    e.preventDefault();
    if (this.fpass.value === this.cpass.value){
      const userData ={
        first_name: this.state.fname,
        second_name: this.state.sname,
        login: this.state.email,
        password: this.state.fpass
      }
      this.props.onReg('/register', userData);
      console.log(userData);
    }
    else {
      console.log("Пароли не совпадают", "1:", this.fpass.value, "2", this.cpass.value)
    }
  }
  render() {
    const inputs = [
      { 
        id: 1, type: 'text',
        placeholder: 'Имя', 
        value: this.fname.value, 
        on_change: this.handleChangeValueFname 
      },
      { 
        id: 2, 
        type: 'text', 
        placeholder: 'Фамилия', 
        value: this.sname.value, 
        on_change: this.handleChangeValueSname
      },
      { 
        id: 3, 
        type: 'email', 
        placeholder: 'Логин', 
        value: this.email.value, 
        on_change: this.handleChangeValueEmail
      },
      { 
        id: 4, 
        type: 'password', 
        placeholder: 'Пароль', 
        value: this.fpass.value, 
        on_change: this.handleChangeValueFpass
      },
      { 
        id: 5, 
        type: 'password', 
        placeholder: 'Пароль еще раз', 
        value: this.cpass.value, 
        on_change: this.handleChangeValueCpass
      }
    ]
    return (
      <div onSubmit={this.RegData.bind(this)}>
        <Header url='/signin' to='Войти' />
        <InputsForm name_form='Регистрация' inputs={inputs} url='/signin' />
        <Foter />
      </div>
    )
  }
}

export default connect(
  state => ({
    success: state.reg.success
  }),
  dispatch => ({
    onReg: (url, data) =>{
      dispatch(reg(url, data))
    }
  })
)(SignUp);