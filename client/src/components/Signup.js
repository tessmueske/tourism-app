import React from "react";
import { useNavigate, Link } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from 'yup';
import '../index.css'; 

function Signup() {
    return (
        <div className="account-center-container">
            <p>i want to sign up as...</p>
            <p>a traveler</p>
            <p>a local expert</p>
            <p>an advertiser</p>
            <p>Don't know? <Link to="/about">Click here</Link>.</p> 
        </div>
    )
}

export default Signup;