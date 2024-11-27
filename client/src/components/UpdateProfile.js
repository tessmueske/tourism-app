import React from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import "../index.css";

function UpdateProfile({ onUpdate }) {
  return (
    <Formik
      initialValues={{ name: "", bio: "", age: "", gender: "" }}
      validationSchema={Yup.object({
        age: Yup.number()
          .positive("Age must be a positive number")
          .integer("Age must be an integer"),
      })}
      onSubmit={(values, { setSubmitting, setErrors }) => {
        fetch("/profile/user/${email}", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(values),
        })
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
            throw new Error("Failed to update profile");
          })
          .then((updatedProfile) => {
            onUpdate(updatedProfile);
            setSubmitting(false);
          })
          .catch((error) => {
            setErrors({ general: "An error occurred. Please try again." });
            setSubmitting(false);
          });
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
  );
}

export default UpdateProfile;
