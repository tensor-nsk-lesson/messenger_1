import React from 'react'
import Navigations from '../routers/Navigations'

class Header extends React.Component {
    constructor(props){
        super(props);
        this.class = props.class;
        this.url = props.url;
        this.to = props.to;
    }
    render(){
        return(
            <div className='header'>
                <div className="name"><h1>MEVO</h1></div>
			    <Navigations class={this.class} url={this.url} to = {this.to} />
            </div>
        )
    }
}

export default Header;