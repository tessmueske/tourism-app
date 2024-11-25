import React from "react";
import { useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from 'yup';
import '../index.css'; 

function AdvertiserLogin({ onLogin }) {
    const navigate = useNavigate();

    const validationSchema = Yup.object().shape({
      username: Yup.string(),
      email: Yup.string().email("Invalid email format"),
      password: Yup.string().required("Password is required"),
    }).test({
      name: "username-or-email-required",
      message: "Either username or email is required",
      test: function (value) {
        return value.username || value.email;
      },
    });  

    const handleLogin = ({ username, email, password }, { setSubmitting, setErrors }) => {
        fetch("/login/advertiser", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, email, password }),
        })
        .then((r) => r.json().then((data) => ({ status: r.ok, data })))
        .then(({ status, data }) => {
            setSubmitting(false);
            if (status) {
                navigate("/landing");
            } else {
                setErrors({ api: data.errors || ["Signup failed"] });
            }
        })
        .catch(() => {
            setSubmitting(false);
            setErrors({ api: ["Something went wrong. Please try again."] });
        });
    };

    return (
      <div className="account-center-container">
        <h2>advertiser login for Magwa</h2>
        <p>⋇⊶⊰❣⊱⊷⋇</p>
        <p>please sign in with your username, email, and password</p>
        <br />
  
        <Formik
          initialValues={{ email: "", username: "", password: "" }}
          validationSchema={validationSchema}
          onSubmit={handleLogin}
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
                  type="text"
                  name="username"
                  placeholder="Username"
                  className="inputBox"
                />
                <ErrorMessage name="username" component="div" className="errorLabel" />
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
                {isSubmitting ? "Logging in..." : "Log in now"}
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
  