import React from "react";
import { Link } from "react-router-dom";
import '../index.css'; 

function Signup() {
    return (
        <div className="account-center-container">
            <p>i want to sign up as...</p>
            <Link to="/signup/traveler" className="nav-link">a traveler</Link>
            <Link to="/signup/localexpert" className="nav-link">a local expert</Link>
            <Link to="/signup/advertiser" className="nav-link">an advertiser</Link>
            <p>don't know? <Link to="/about">click here</Link>.</p> 
        </div>
    )
}

export default Signup;