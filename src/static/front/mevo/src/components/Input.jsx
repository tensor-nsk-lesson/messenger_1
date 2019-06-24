import React from 'react'

export default class Input extends React.Component {
    render() {
        return(
                <input
                    value = {this.props.value}
                    type = {this.props.input.type} 
                    required 
                    placeholder = {this.props.input.placeholder}
                    onChange = {this.props.input.on_change}
                />
        )
    }
}