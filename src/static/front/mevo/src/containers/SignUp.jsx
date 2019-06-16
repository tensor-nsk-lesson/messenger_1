import React from 'react';
import Header from '../components/Header'
import Foter from '../components/Foter'
import InputsForm from '../components/InputsForm'

class SignUp extends React.Component {
  render() {
    const inputs = [
      { id: 1, type: 'text', placeholder: 'Имя' },
      { id: 2, type: 'text', placeholder: 'Фамилия' },
      { id: 3, type: 'email', placeholder: 'Логин' },
      { id: 4, type: 'password', placeholder: 'Пароль' },
      { id: 5, type: 'password', placeholder: 'Пароль еще раз' }
    ]
    return (
      <div>
        <Header url='/signin' to='Войти'></Header>
        <InputsForm name_form='Регистрация' inputs={inputs}></InputsForm>
        <Foter></Foter>
      </div>
    )
  }
}

export default SignUp;