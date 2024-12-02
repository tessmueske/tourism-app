import React from "react";
import { useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from 'yup';
import { useUserContext } from "./UserContext";
import '../index.css'; 

function AdvertiserLogin({ setUser }) {
    const navigate = useNavigate();
    const { setEmail, setUsername } = useUserContext();

    // LOG IN WITH EMAIL ONLY
    const validationSchema = Yup.object().shape({
      email: Yup.string().email("Invalid email format"),
      password: Yup.string().required("Password is required"),
    });

    const handleLogin = ({ username, email, password }, { setSubmitting, setErrors }) => {
      fetch("/login/advertiser", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      })
        .then((r) => {
          setSubmitting(false);
          if (r.ok) {
            r.json().then((userData) => {
              setUser({ username: userData.username, email: userData.email });
              setEmail(email);
              setUsername(username);
              navigate("/welcome/home");
            });
          } else {
            r.json().then((err) => {
              setErrors({ api: err.errors || ["Signup failed"] });
            });
          }
        })
        .catch(() => {
          setSubmitting(false);
          setErrors({ api: ["Something went wrong. Please try again."] });
        });
    };

    return (
      <div className="account-center-container">
        <h2>advertiser login for magwa</h2>
        <p>⋇⊶⊰❣⊱⊷⋇</p>
        <p>please sign in with your email, and password</p>
        <br />
  
        <Formik
          initialValues={{ email: "", password: "" }}
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
  