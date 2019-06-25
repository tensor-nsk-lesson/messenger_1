import React from 'react';
import {Link} from 'react-router-dom'

class Navigations extends React.Component {
    constructor(props){
        super(props);
        this.class = props.class;
        this.url = props.url;
        this.to = props.to;
    }
    render() {
        return (
            <Link className={this.class} to={this.url}>{ this.to }</Link>
        );
    }
}

export default Navigations;