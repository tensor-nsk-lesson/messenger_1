import React from 'react'
import Header from '../components/Header'
import Foter from '../components/Foter'
import InputsForm from '../components/InputsForm'

class SignUp extends React.Component {
  render() {
    const inputs = [
        { id: 1, type: 'email', placeholder: 'Логин' },
        { id: 2, type: 'password', placeholder: 'Пароль' }
      ]
    return (
      <div>
        <Header class='signin' url='/signup' to='Регистрация'></Header>
        <InputsForm name_form='Авторизация' inputs={inputs}></InputsForm>
        <Foter class='signin'></Foter>
      </div>
    )
  }
}

export default SignUp;