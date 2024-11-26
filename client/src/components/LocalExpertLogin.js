import React from "react";
import { useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from 'yup';
import '../index.css';

function LocalExpertLogin({ setUser }) {
  const navigate = useNavigate();

  const validationSchema = Yup.object().shape({
    email: Yup.string()
      .email("invalid email format")
      .required("email is required"),
    password: Yup.string()
      .required("password is required")
  });

  const handleLogin = ({ username, email, password }, { setSubmitting, setErrors }) => {
    fetch("/login/traveler", {
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
            setUser(userData);
            navigate("/welcome/home");
          });
        } else {
          r.json().then((err) => {
            setErrors({ api: err.errors || ["login failed"] });
          });
        }
      })
      .catch(() => {
        setSubmitting(false);
        setErrors({ api: ["something went wrong. please try again."] });
      });
  };

  return (
    <div className="account-center-container">
      <div className="mainContainer">
        <div className="titleContainer">
          <p>⋇⊶⊰❣⊱⊷⋇</p>
          <div>local expert log in to magwa</div>
          <p>please sign in with your username or email and password</p>
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
                    placeholder="email"
                    className="inputBox"
                  />
                  <ErrorMessage name="email" component="div" className="errorLabel" />
                </div>
                <br />

                <div className="inputContainer">
                  <p>username</p>
                  <Field
                    type="text"
                    name="username"
                    placeholder="username"
                    className="inputBox"
                  />
                  <ErrorMessage name="username" component="div" className="errorLabel" />
                </div>
                <br />

                <div className="inputContainer">
                  <p>password</p>
                  <Field
                    type="password"
                    name="password"
                    placeholder="password"
                    className="inputBox"
                  />
                  <ErrorMessage name="password" component="div" className="errorLabel" />
                </div>
                <br />

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
      </div>
    </div>
  );
}

export default LocalExpertLogin;
