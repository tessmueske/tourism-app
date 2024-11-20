import React from "react";
import { useNavigate, Link } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from 'yup';
import '../index.css'; 

function Signup() {
    return (
        <div className="account-center-container">
            <p>i want to sign up as...</p>
            <Link to="/signup/traveler">a traveler</Link>
            <Link to="/signup/localexpert">a local expert</Link>
            <Link to="/signup/advertiser">an advertiser</Link>
            <p>don't know? <Link to="/about">click here</Link>.</p> 
        </div>
    )
}

export default Signup;