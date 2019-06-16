import React from 'react';
import Header from '../components/Header'
import Foter from '../components/Foter'
import InputsForm from '../components/InputsForm'

class DropPass extends React.Component {

  render(){
    const inputs = [
      { id: 1, type: 'password', placeholder: 'Пароль' }
    ]
    return (
      <div>
        <Header class='droppass' url='/signup' to='Отмена'></Header>
        <InputsForm name_form='Сброс пароля' inputs={inputs}></InputsForm>
        <Foter class='droppass'></Foter>
      </div>
    )
  }
}

export default DropPass;