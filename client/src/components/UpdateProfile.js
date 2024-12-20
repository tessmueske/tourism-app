import React, { useEffect } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { useNavigate } from "react-router-dom";
import { useUserContext } from './UserContext';
import "../index.css";
import "../profilecard.css";

function UpdateProfile({ onUpdate }) {
    const navigate = useNavigate();
    const { user, setUser } = useUserContext();

  useEffect(() => {
    fetch(`/users/${user.email}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch profile");
        }
        return response.json();
      })
      .then((data) => {
        setUser(data);
      })
      .catch((error) => {
        console.error("Error fetching profile:", error);
      });
  }, [user.email]);

  return (
    <div className="profile-display card">
      <Formik
        initialValues={{
          name: user.name || "",
          bio: user.bio || "",
          age: user.age || "",
          gender: user.gender || "",
        }}
        validationSchema={Yup.object({
          age: Yup.number()
            .positive("Age must be a positive number")
            .integer("Age must be an integer"),
        })}
        onSubmit={(values, { setSubmitting, setErrors }) => {
            const updatedProfile = { ...user, ...values };
          
            fetch(`/users/${user.email}`, {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(updatedProfile),
            })
              .then((response) => {
                if (response.ok) {
                  return response.json();
                }
                return response.json().then((data) => {
                  throw new Error(data.message || "Failed to update profile");
                });
              })
              .then((updatedProfile) => {
                onUpdate(updatedProfile);
                navigate(`/user/${user.email}`); 
              })
              .catch((error) => {
                console.error("Error updating profile:", error);
                setErrors({ general: error.message });
              })
              .finally(() => {
                setSubmitting(false);
              });
        }}
      >
        {({ isSubmitting, errors }) => (
          <Form>
            <div className="inputContainer">
              <p>name:</p>
              <Field
                type="text"
                name="name"
                placeholder="name"
                className="inputBox"
              />
              <ErrorMessage name="name" component="div" className="errorLabel" />
            </div>
            <br />

            <div className="inputContainer">
              <p>age:</p>
              <Field
                type="number"
                name="age"
                placeholder="age"
                className="inputBox"
              />
              <ErrorMessage name="age" component="div" className="errorLabel" />
            </div>
            <br />

            <div className="inputContainer">
              <p>gender:</p>
              <Field
                type="text"
                name="gender"
                placeholder="gender"
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
              <p>bio:</p>
              <Field
                as="textarea"
                name="bio"
                placeholder="bio"
                className="textBox"
              />
              <ErrorMessage name="bio" component="div" className="errorLabel" />
            </div>
            <br />

            <div className="inputContainer">
              <button type="submit" className="button" disabled={isSubmitting}>
                {isSubmitting ? "submitting..." : "update"}
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

export default UpdateProfile;

