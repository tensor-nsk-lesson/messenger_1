import React from 'react'

class Foter extends React.Component {
    constructor(props){
        super(props);
        this.class = props.class;
    }
    render(){
        return(
            <footer className={this.class}>
	            <div className="footer">
                    <h3>Copyright (c) 2019 MEVO TEAM</h3>
                </div>
            </footer>
        )
    }
}

export default Foter;