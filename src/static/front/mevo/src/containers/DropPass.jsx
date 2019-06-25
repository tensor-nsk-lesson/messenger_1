import React from 'react';
import Header from '../components/Header'
import Foter from '../components/Footer'
import InputsForm from '../components/InputsForm'

class DropPass extends React.Component {

  render(){
    const inputs = [
      { id: 1, type: 'password', placeholder: 'Пароль' }
    ]
    return (
      <div>
        <Header class='droppass' url='/signup' to='Отмена' />
        <InputsForm name_form='Сброс пароля' inputs={inputs} />
        <Foter class='droppass' />
      </div>
    )
  }
}

export default DropPass;