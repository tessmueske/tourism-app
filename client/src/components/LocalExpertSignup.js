import React from "react";
import { useNavigate, Link } from "react-router-dom";
import { useFormik, Form, Field, ErrorMessage } from "formik";
import * as Yup from 'yup';
import '../index.css'; 

function LocalExpertSignup() {
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
            notes: "",
        },
        validationSchema,
        onSubmit: (values) => {
            handleSignup(values);
        },
    });

    const handleSignup = ({ email, password, notes }) => {
        fetch("/signup/localexpert", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email, password, notes }),
        })
          .then((r) => {
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
            <p>here is where you'll tell us why you want to be a part of the magwa community. there's no specific prompt, but here's some questions to get you thinking:</p>
            <p>where are you from? what language(s) do you speak? what types of activities are you passionate about? how do you think your skills and expertise can contribute to our community? feel free to share a bit about your background and what excites you about joining magwa! </p>
            <textarea
              type="text"
              name="notes" 
              onChange={formik.handleChange}
              value={formik.values.notes}
              placeholder="Write here..."
              required
            />
            <br></br>
            <br></br>
            <button type="submit" className="button" disabled={formik.isSubmitting}>
              {formik.isSubmitting ? "Submitting..." : "Submit for verification"}
            </button>
            <br />
            {formik.errors.api && (
              <p style={{ color: "red" }}>{formik.errors.api.join(", ")}</p>
            )}
          </form>
        </div>
      );
}

export default LocalExpertSignup;