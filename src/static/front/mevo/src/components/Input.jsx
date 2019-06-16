import React from 'react'

export default function Input({ input }) {
    return(
        <input type={input.type} required placeholder={input.placeholder}></input>
    )
}