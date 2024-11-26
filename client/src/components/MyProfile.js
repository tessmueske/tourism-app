import React, { useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import "../index.css";

function MyProfile({ username }) {
    const [profile, setProfile] = useState({
        name: "",
        bio: "",
        age: "",
        gender: "",
      });

  return (
    <div className="account-center-container">
      <p>welcome to your profile, {username}!</p>
      
      <div className="profile-display">
        <p><strong>name:</strong> {profile.name || ""}</p>
        <p><strong>bio:</strong> {profile.bio || ""}</p>
        <p><strong>age:</strong> {profile.age || ""}</p>
        <p><strong>gender:</strong> {profile.gender || ""}</p>
      </div>
      
      <Formik
        initialValues={{ name: "", bio: "", age: "", gender: "" }}
        validationSchema={Yup.object({
          age: Yup.number()
            .positive("Age must be a positive number")
            .integer("Age must be an integer")
        })}
        onSubmit={(values, { setSubmitting }) => {
            setProfile(values);
            setSubmitting(false);
        }}
      >
        {({ isSubmitting, errors }) => (
          <Form>
            <div className="inputContainer">
              <Field
                type="text"
                name="name"
                placeholder="Name"
                className="inputBox"
              />
              <ErrorMessage name="name" component="div" className="errorLabel" />
            </div>
            <br />

            <div className="inputContainer">
              <Field
                type="text"
                name="bio"
                placeholder="Bio"
                className="inputBox"
              />
              <ErrorMessage name="bio" component="div" className="errorLabel" />
            </div>
            <br />

            <div className="inputContainer">
              <Field
                type="number"
                name="age"
                placeholder="Age"
                className="inputBox"
              />
              <ErrorMessage name="age" component="div" className="errorLabel" />
            </div>
            <br />

            <div className="inputContainer">
              <Field
                type="text"
                name="gender"
                placeholder="Gender"
                className="inputBox"
              />
              <ErrorMessage
                name="gender"
                component="div"
                className="errorLabel"
              />
            </div>
            <br />

            <div className="inputContainer">
              <button type="submit" className="button" disabled={isSubmitting}>
                {isSubmitting ? "Submitting..." : "Submit"}
              </button>
            </div>
            <br />

            {errors.general && (
              <div className="errorContainer">
                <p className="errorText">{errors.general}</p>
              </div>
            )}
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default MyProfile;
