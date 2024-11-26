import React from "react";
import { useFormik } from "formik";
import * as Yup from 'yup';
import '../index.css'; 

function MyProfile({ username }){

  return (
    <div className='about-center-container'>
        <p>this is your profile, {username}!</p>
        <Formik
            initialValues={{ name: "", bio: "", age: "", gender: "" }}
            onSubmit={handleSubmit}
          ></Formik>
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
                    type="integer"
                    name="age"
                    placeholder="Age"
                    className="inputBox"
                  />
                  <ErrorMessage name="age" component="div" className="errorLabel" />
                </div>

                <div className="inputContainer">
                  <Field
                    type="text"
                    name="gender"
                    placeholder="Gender"
                    className="inputBox"
                  />
                  <ErrorMessage name="gender" component="div" className="errorLabel" />
                </div>
  
                <div className="inputContainer">
                  <button type="submit" className="button" disabled={isSubmitting}>
                    {isSubmitting ? "Logging in..." : "Log in"}
                  </button>
                </div>
                <br></br>
  
                {errors.general && (
                  <div className="errorContainer">
                    <p className="errorText">{errors.general}</p>
                  </div>
                )}
              </Form>
    </div>
  );
};

export default MyProfile;