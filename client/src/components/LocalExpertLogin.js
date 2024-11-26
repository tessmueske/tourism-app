import React from "react";
import { useNavigate, Link } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from 'yup';
import '../index.css'; 

function LocalExpertLogin({ onLogin }) {
    const navigate = useNavigate();

    const validationSchema = Yup.object().shape({
      email: Yup.string()
        .email("invalid email format")
        .required("email is required"),
      password: Yup.string()
        .required("password is required")
    });
  
    const handleSubmit = (values, { setSubmitting, setErrors }) => {
      fetch("/login/localexpert", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values),
      })
        .then((r) => {
          setSubmitting(false);
          if (r.ok) {
            r.json().then((user) => {
              onLogin(user);
              navigate("/welcome/home");
            });
          } else {
            r.json().then((err) => {
              if (r.status === 404) {
                setErrors({ email: "Email not registered. Please sign up." });
              } else {
                setErrors({ password: "Invalid login credentials. Try again?" });
              }
            });
          }
        })
        .catch(() => {
          setSubmitting(false);
          setErrors({ general: "Something went wrong. Please try again." });
        });
    };
  
    return (
      <div className="account-center-container">
        <div className="mainContainer">
          <div className="titleContainer">
            <p>⋇⊶⊰❣⊱⊷⋇</p>
            <div>local expert log in to magwa</div>
            <br></br>
          </div>
          <Formik
            initialValues={{ email: "", password: "" }}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
          >
            {({ isSubmitting, errors }) => (
              <Form>
                <div className="inputContainer">
                  <Field
                    type="email"
                    name="email"
                    placeholder="Email"
                    className="inputBox"
                  />
                  <ErrorMessage name="email" component="div" className="errorLabel" />
                </div>
  
                <br />
  
                <div className="inputContainer">
                  <Field
                    type="password"
                    name="password"
                    placeholder="password"
                    className="inputBox"
                  />
                  <ErrorMessage name="password" component="div" className="errorLabel" />
                </div>
  
                <br />
  
                <div className="inputContainer">
                  <button type="submit" className="button" disabled={isSubmitting}>
                    {isSubmitting ? "Logging in..." : "Log in"}
                  </button>
                </div>
                <br></br>
  
                {errors.general && (
                  <div className="errorContainer">
                    <p className="errorText">{errors.general}</p>
                  </div>
                )}
              </Form>
            )}
          </Formik>
        </div>
      </div>
    );
  }

export default LocalExpertLogin;