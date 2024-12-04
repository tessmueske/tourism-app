import React, { useEffect, useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import { useUserContext } from "./UserContext";
import { useParams, useNavigate } from 'react-router-dom';
import '../index.css'; 
import "../post.css";

function NewPost({ today, europeanDate }) {
  const { username } = useUserContext();
  const navigate = useNavigate();
  const [successMessage, setSuccessMessage] = useState("");

  return (
    <div className="communitycard-display">
      <h2>new post</h2>
      <Formik
        initialValues={{
          author: username,
          date: today,
          subject: "",
          body: "",
          hashtag: "",
        }}
        onSubmit={async (values, { setSubmitting, resetForm }) => {
          try {
            const response = await fetch('/community/post/new', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(values), 
            });

            if (response.ok) {
              setSuccessMessage("posted successfully! redirecting to community homepage...");
              resetForm();
              setTimeout(() => {
                navigate(`/community/posts/all`); 
              }, 2000);
            } else {
              console.error("Error creating post");
            }
          } catch (error) {
            console.error("Error:", error);
          }
          setSubmitting(false); 
        }}
      >
        {({ isSubmitting }) => (
          <Form>
            <div className="inputContainer">
              <p>author:</p>
              <Field
                type="text"
                name="author"
                value={username} 
                className="inputBox"
                readOnly
              />
            </div>
            <div className="inputContainer">
              <p>date:</p>
              <Field
                type="date"
                name="date"
                value={today}
                className="inputBox"
              />
              <p style={{ fontSize: '14px' }}>(in Spanish format): {europeanDate}</p>
            </div>
            <div className="inputContainer">
              <p>subject:</p>
              <Field
                type="text"
                name="subject"
                placeholder="subject..."
                className="inputBox"
              />
              <ErrorMessage name="subject" component="div" className="errorLabel" />
            </div>
            <div className="inputContainer">
              <p>body:</p>
              <Field
                as="textarea"
                name="body"
                placeholder="what do you want to say?"
                className="textBox"
              />
              <ErrorMessage name="body" component="div" className="errorLabel" />
            </div>

            <div className="inputContainer">
              <p>hashtags:</p>
              <Field
                type="text"
                name="hashtag"
                placeholder="add hashtags"
                className="inputBox"
              />
              <ErrorMessage name="hashtag" component="div" className="errorLabel" />
            </div>
            <br></br>

            <div className="inputContainer">
              <button
                type="submit"
                className="button"
                disabled={isSubmitting}
              >
                {isSubmitting ? "submitting..." : "post now"}
              </button>
            </div>
          </Form>
        )}
      </Formik>
      {successMessage && (
        <div className="successMessage">
          <p>{successMessage}</p>
        </div>
      )}
    </div>
  );
}

export default NewPost;