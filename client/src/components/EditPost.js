import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from 'react-router-dom';
import { useUserContext } from './UserContext';
import { Formik, Form, Field, ErrorMessage } from "formik";import * as Yup from 'yup';
import '../index.css'; 


function EditPost() {
    const [initialValues, setInitialValues] = useState(null);
    const { username } = useUserContext();
    const navigate = useNavigate();
    const { postId } = useParams(); 

    useEffect(() => {
        fetch(`/community/post/${postId}`)
          .then((response) => response.json())
          .then((data) => {
            setInitialValues({
                author: data.author,
                date: data.date,
                subject: data.subject,
                body: data.body,
                hashtag: data.hashtag,
            });
          })
          .catch((error) => console.error("Error fetching post data:", error));
      }, [postId]);

      const handleSubmit = (values) => {
        fetch(`/community/post/${postId}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(values),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Failed to update post");
            }
            return response.json();
          })
          .then(() => {
            navigate(`/community/post/${postId}`);
          })
          .catch((error) => console.error("Error updating post:", error));
      };

      if (!initialValues) {
        return <p>Loading form...</p>;
      }

      return (
        <div className="communitycard-displaycard-center">
          <div className="card">
            <h2>edit post</h2>
            <Formik
              initialValues={initialValues}
              onSubmit={handleSubmit}
            >
              {({ isSubmitting }) => (
                <Form>

                  <div>
                    <label htmlFor="subject">subject:</label>
                    <Field name="subject" type="text" />
                    <ErrorMessage name="subject" component="div" className="errorLabel" />
                  </div>
    
                  <div>
                    <label htmlFor="body">body:</label>
                    <Field name="body" as="textarea" />
                    <ErrorMessage name="body" component="div" className="errorLabel" />
                  </div>
    
                  <div>
                    <label htmlFor="hashtag">hashtags:</label>
                    <Field name="hashtag" type="text" />
                    <ErrorMessage name="hashtag" component="div" className="errorLabel" />
                  </div>
                  <br></br>
    
                  <button type="submit" className="button" disabled={isSubmitting}>
                    save changes
                  </button>
                  <br></br>
                  <br></br>
                  <button
                    type="button"
                    className="button"
                    onClick={() => navigate(`/community/post/${postId}`)}
                  >
                    go back
                  </button>
                </Form>
              )}
            </Formik>
          </div>
        </div>
      );
    }
    
    export default EditPost;