import React from "react";
import { useNavigate } from "react-router-dom";
import { useFormik } from "formik";
import * as Yup from 'yup';
import '../index.css'; 

function LocalExpertSignup() {
    const navigate = useNavigate();

    const validationSchema = Yup.object().shape({
      username: Yup.string().required("Username is required"),
      email: Yup.string()
          .email("Invalid email format")
          .required("Email is required"), 
      password: Yup.string()
          .required("Password is required")
  });

    const formik = useFormik({
      initialValues: {
          username: "",
          email: "",
          password: "",
          notes: "",
      },
      validationSchema,
      onSubmit: (values) => {
          handleSignup(values);
      },
    });

    const handleSignup = ({ username, email, password, notes }) => {
      fetch("/signup/localexpert", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password, notes }),
      })
        .then((r) => {
          console.log("Form data being sent:", { username, email, password, notes });
          if (r.ok) {
              navigate("/verification/pending");
          } else {
            r.json().then((err) => {
              formik.setErrors({ api: err.errors || ["Signup failed"] }); 
            });
          }
        })
        .catch(() => {
          formik.setErrors({ api: ["Something went wrong. Please try again."] });
        });
    };

      return (
        <div className="account-center-container">
          <h2>local expert sign up for magwa</h2>
          <p>⋇⊶⊰❣⊱⊷⋇</p>
          <p>before you can use our site, your profile will need to be verified by
            our team. we want to make sure that we keep our community local! please fill out the form below with your email, password, and a bit about yourself.</p>
          <br />
          <form onSubmit={formik.handleSubmit}>
            <p>email</p>
            <input
              type="email"
              name="email" 
              onChange={formik.handleChange}
              value={formik.values.email}
              placeholder="email"
              required
            />
            <br />
            <p>create a username (others will see this)</p>
          <input
            type="text"
            name="username" 
            onChange={formik.handleChange}
            value={formik.values.username}
            placeholder="username"
            required
            />
            <br />
            <p>password</p>
            <input
              type="password"
              name="password" 
              onChange={formik.handleChange}
              value={formik.values.password}
              placeholder="password"
              required
            />
            <br />
            <br />
            <p>here is where you'll tell us why you want to be a part of the magwa community. there's no specific prompt, but here's some questions to get you thinking:</p>
            <p>where are you from? what language(s) do you speak? what types of activities are you passionate about? how do you think your skills and expertise can contribute to our community? feel free to share a bit about your background and what excites you about joining magwa! </p>
            <textarea
              type="text"
              name="notes" 
              onChange={formik.handleChange}
              value={formik.values.notes}
              placeholder="write here..."
              required
            />
            <br></br>
            <br></br>
            <button type="submit" className="button" disabled={formik.isSubmitting}>
              {formik.isSubmitting ? "submitting... (this may take a few moments!)" : "submit for verification"}
            </button>
            <br />
            <br></br>
            <br></br>
            {formik.errors.api && (
              <p style={{ color: "red" }}>{formik.errors.api.join(", ")}</p>
            )}
          </form>
        </div>
      );
}

export default LocalExpertSignup;