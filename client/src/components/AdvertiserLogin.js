import React from "react";
import { useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from 'yup';
import { useUserContext } from "./UserContext";
import '../index.css'; 

function AdvertiserLogin() {
    const navigate = useNavigate();
    const { user, setUser, handleAdvertiserLogin } = useUserContext();

    const validationSchema = Yup.object().shape({
      email: Yup.string().email("Invalid email format"),
      username: Yup.string().required("Username is required"),
      password: Yup.string().required("Password is required"),
    });

    return (
      <div className="account-center-container">
        <h2>advertiser login for magwa</h2>
        <p>⋇⊶⊰❣⊱⊷⋇</p>
        <p>please sign in with your email, username, and password</p>
        <br />
  
        <Formik
        initialValues={{ email: "", username: "", password: "" }}
        validationSchema={validationSchema}
        onSubmit={(values, { setSubmitting, setErrors }) => {
          handleAdvertiserLogin(values, { setSubmitting, setErrors });
        }}
      >
          {({ isSubmitting, errors }) => (
            <Form>
              <div className="inputContainer">
                <p>email</p>
                <Field
                  type="email"
                  name="email"
                  placeholder="Email"
                  className="inputBox"
                />
                <ErrorMessage name="email" component="div" className="errorLabel" />
              </div>
              <br></br>
              <div className="inputContainer">
                <p>username</p>
                <Field
                  type="username"
                  name="username"
                  placeholder="username"
                  className="inputBox"
                />
                <ErrorMessage name="email" component="div" className="errorLabel" />
              </div>
              <br></br>
              <div className="inputContainer">
                <p>password</p>
                <Field
                  type="password"
                  name="password"
                  placeholder="Password"
                  className="inputBox"
                />
                <ErrorMessage name="password" component="div" className="errorLabel" />
              </div>
              <br></br>
  
              <button type="submit" className="button" disabled={isSubmitting}>
                {isSubmitting ? "logging in..." : "log in now"}
              </button>
  
              {errors.api && (
                <p style={{ color: "red" }}>{errors.api.join(", ")}</p>
              )}
            </Form>
          )}
        </Formik>
      </div>
    );
  }
  
  export default AdvertiserLogin;
  