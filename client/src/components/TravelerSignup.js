import React from "react";
import { useNavigate, Link } from "react-router-dom";
import { useFormik, Form, Field, ErrorMessage } from "formik";
import * as Yup from 'yup';
import '../index.css'; 

function TravelerSignup() {
    const navigate = useNavigate();

  const validationSchema = Yup.object().shape({
    email: Yup.string()
      .email("Invalid email format")
      .required("Email is required"), 
    password: Yup.string()
      .required("Password is required")
  });

  const formik = useFormik({
    initialValues: {
      email: "",
      password: "",
    },
    validationSchema,
    onSubmit: (values) => {
      handleSignup(values);
    },
  });

  const handleSignup = ({ email, password }) => {
    fetch("http://localhost:5555/signup/traveler", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    })
      .then((r) => {
        if (r.ok) {
        } else {
          r.json().then((err) => {
            formik.setErrors({ api: err.errors || ["signup failed"] }); 
          });
        }
      })
      .catch(() => {
        formik.setErrors({ api: ["Something went wrong. Please try again."] });
      });
  };

  return (
    <div className="account-center-container">
      <h2>traveler sign up for magwa</h2>
      <p>⋇⊶⊰❣⊱⊷⋇</p>
      <p>we do not require verification for travelers to use magwa (we require local experts and advertisers to be verified by our team before use to ensure everything stays local!).</p>
      <br />
      <form onSubmit={formik.handleSubmit}>
        <input
          type="email"
          name="email" 
          onChange={formik.handleChange}
          value={formik.values.email}
          placeholder="Email"
          required
        />
        <br />
        <br />
        <input
          type="password"
          name="password" 
          onChange={formik.handleChange}
          value={formik.values.password}
          placeholder="Password"
          required
        />
        <br />
        <br />
        <button type="submit" className="button" disabled={formik.isSubmitting}>
          {formik.isSubmitting ? "Signing up..." : "Sign up now"}
        </button>
        <br />
        {formik.errors.api && (
          <p style={{ color: "red" }}>{formik.errors.api.join(", ")}</p>
        )}
      </form>
    </div>
  );
}

export default TravelerSignup;