import React from "react";
import { useNavigate, Link } from "react-router-dom";
import { useFormik, Form, Field, ErrorMessage } from "formik";
import * as Yup from 'yup';
import '../index.css'; 

function AdvertiserSignup() {
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
        fetch("http://localhost:5555/signup/advertiser", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email, password, notes }),
        })
          .then((r) => {
            if (r.ok) {
                navigate("/thanks");
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
          <h2>advertiser sign up for magwa</h2>
          <p>⋇⊶⊰❣⊱⊷⋇</p>
          <p>before you can use our site, your profile will need to be verified by
            our team. please fill out the form below with your email, password, a bit about yourself, and why you'd like to advertise with magwa.</p>
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
            <p>here is where you'll tell us why you want to advertise with us. where are you from? what business(es) or service(s) do you provide? how do those businesses or services help the community?</p>
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

export default AdvertiserSignup;