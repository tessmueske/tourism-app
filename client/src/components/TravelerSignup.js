import React from "react";
import { useNavigate } from "react-router-dom";
import { useFormik } from "formik";
import { useUserContext } from "./UserContext";
import * as Yup from 'yup';
import '../index.css'; 

function TravelerSignup() {
    const navigate = useNavigate();
    const { user, setUser } = useUserContext();

    const validationSchema = Yup.object().shape({
      username: Yup.string().required("Username is required"),
      email: Yup.string()
        .email("Invalid email format")
        .required("Email is required"), 
      password: Yup.string().required("Password is required")
    });

    const formik = useFormik({
      initialValues: {
        username: "",
        email: "",
        password: "",
      },
      validationSchema,
      onSubmit: (values) => {
        handleSignup(values);
      },
    });

    const handleSignup = ({ username, email, password }) => {
      fetch("/signup/traveler", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      })
        .then((r) => {
          if (r.ok) {
            r.json().then((userData) => {
              setUser({ username: userData.username, email: userData.email });
              navigate("/welcome/home");
            });
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
        <h2>traveler sign up for magwa</h2>
        <p>⋇⊶⊰❣⊱⊷⋇</p>
        <p>we do not require verification for travelers to use magwa (we require local experts and advertisers to be verified by our team before use to ensure everything stays local).</p>
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
          <br></br>
          <button type="submit" className="button" disabled={formik.isSubmitting}>
            {formik.isSubmitting ? "signing up..." : "sign up now"}
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
