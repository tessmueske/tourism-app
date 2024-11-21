import React from "react";
import { useNavigate, Link } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from 'yup';
import '../index.css'; 

function Login() {
    return (
        <div className="account-center-container">
            <p>i want to log in as...</p>
            <Link to="/login/traveler">a traveler</Link>
            <Link to="/login/localexpert">a local expert</Link>
            <Link to="/login/advertiser">an advertiser</Link>
            <br></br>
            <p>thank you for using magwa!</p>
        </div>
    )
}

export default Login;