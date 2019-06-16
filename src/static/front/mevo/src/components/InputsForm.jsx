import React from 'react'
import Input from './Input'
import Button from './Button'
import NameForm from './NameForm'

export default function InputsForm(props) {
    return(
        <div className="input_form">
            <NameForm name_form={props.name_form}></NameForm>
			<form method="post">
            	{ props.inputs.map( input=> {
                    return <Input input={input} key={input.id}></Input>
                }) }
                <Button></Button>
          </form>
		</div>
    )
}