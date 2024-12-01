import React from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import { useUserContext } from "./UserContext";
import '../index.css'; 
import "../post.css";

function NewPost() {
  const { username } = useUserContext();

  return (
    <div className="communitycard-display">
      <h2>new post</h2>
      <Formik
        initialValues={{
          author: username,
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
              resetForm();
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
                readOnly
                className="inputBox"
              />
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
              <p>hashtag:</p>
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
                {isSubmitting ? "submitting..." : "post"}
              </button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default NewPost;