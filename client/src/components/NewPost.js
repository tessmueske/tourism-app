import React, { useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import { useUserContext } from "./UserContext";
import { useNavigate } from 'react-router-dom';
import '../index.css'; 
import "../post.css";

function NewPost() {
  const { user } = useUserContext();
  const navigate = useNavigate();
  const [successMessage, setSuccessMessage] = useState("");

  return (
    <div className="communitycard-display">
      <h2>new post</h2>
      <Formik
        initialValues={{
          username: user.username,
          subject: "",
          body: "",
          hashtags: "",
        }}
        onSubmit={async (values, { setSubmitting, resetForm }) => {
          const hashtagsPattern = /#(\w+)/g;
          const hashtags = [...(values.hashtags.match(hashtagsPattern) || [])].map(tag => tag.slice(1));
          const postData = {
            ...values,
            hashtags: hashtags, 
          };
          try {
            const response = await fetch('/posts/new', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(postData), 
            });

            if (response.ok) {
              setSuccessMessage("posted successfully! redirecting to community homepage...");
              resetForm();
              setTimeout(() => {
                navigate(`/posts`); 
              }, 2000);
            } else {
              console.error("Error creating post");
            }
          } catch (error) {
            console.error("Error:", error.message);
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
                name="username"
                value={user.username} 
                className="inputBox"
                readOnly
              />
            </div>
            <div className="inputContainer">
              <p>subject:</p>
              <Field
                type="text"
                name="subject"
                placeholder="subject...(required)"
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
              <p>hashtags #typed #like #this (try #tenerife or #paella!):</p>
              <Field
                type="text"
                name="hashtags"
                placeholder="add hashtags"
                className="inputBox"
              />
              <ErrorMessage name="hashtags" component="div" className="errorLabel" />
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