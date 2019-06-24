import React from 'react'
import Header from '../components/Header'
import Foter from '../components/Footer'
import InputsForm from '../components/InputsForm'

class SignUp extends React.Component {
  render() {
    const inputs = [
        { id: 1, type: 'email', placeholder: 'Логин' },
        { id: 2, type: 'password', placeholder: 'Пароль' }
      ]
    return (
      <div>
        <Header class='signin' url='/signup' to='Регистрация' />
        <InputsForm name_form='Авторизация' inputs={inputs} />
        <Foter class='signin' />
      </div>
    )
  }
}

export default SignUp;