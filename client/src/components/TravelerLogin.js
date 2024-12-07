import React from "react";
import { useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import { useUserContext } from "./UserContext";
import * as Yup from 'yup';
import '../index.css';

function TravelerLogin() {
  const { user, setUser, handleTravelerLogin } = useUserContext();
  const navigate = useNavigate();

  const validationSchema = Yup.object().shape({
    email: Yup.string()
      .email("Invalid email format"),
    username: Yup.string().required("Username is required"),
    password: Yup.string().required("Password is required"),
  });

  return (
    <div className="account-center-container">
      <h2>traveler login for magwa</h2>
      <p>⋇⊶⊰❣⊱⊷⋇</p>
      <p>please sign in with your email and password.</p>
      <br />

      <Formik
        initialValues={{ email: "", username: "", password: "" }}
        validationSchema={validationSchema}
        onSubmit={(values, { setSubmitting, setErrors }) => {
          handleTravelerLogin(values, { setSubmitting, setErrors });
        }}
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
              <p style={{ color: "red" }}>{errors.api}</p>
            )}
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default TravelerLogin;
