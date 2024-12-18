import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from 'react-router-dom';
import { useUserContext } from './UserContext';
import { Formik, Form, Field, ErrorMessage } from "formik";
import '../index.css'; 

function EditPost() {
    const [initialValues, setInitialValues] = useState(null);
    const { user } = useUserContext();
    const navigate = useNavigate();
    const { postId } = useParams(); 

    useEffect(() => {
      fetch(`/posts/${postId}`)
          .then((response) => {
              if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
          })
          .then((data) => {
              const hashtags = Array.isArray(data.hashtags)
                  ? data.hashtags
                  : data.hashtags?.split(' ').map((tag) => tag.trim()).filter(Boolean) || [];
              
              setInitialValues({
                  author: user?.username || '',
                  subject: data.subject || '',
                  body: data.body || '',
                  hashtag: hashtags.join(' '), 
              });
          })
          .catch((error) => console.error("Error fetching post data:", error));
    }, [postId, user]);
    
    const handleSubmit = (values) => {
        const updatedHashtags = values.hashtag
            ? values.hashtag.split(' ').map((tag) => tag.trim()).filter(Boolean)
            : [];
    
        fetch(`/posts/edit/${postId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                ...values,
                hashtags: updatedHashtags,
            }),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to update post");
                }
                return response.json();
            })
            .then(() => {
                navigate(`/posts/${postId}`);
            })
            .catch((error) => {
                console.error("Error updating post:", error);
            });
    };
    

    if (!initialValues) {
        return <p className="communitycard-displaycard-center">loading...</p>;
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
                    <div className="inputContainer">
                      <p>author:</p>
                      <Field
                        type="text"
                        name="author"
                        value={user.username}
                        className="inputBox"
                        readOnly
                      />
                    </div>
                  <div>
                    <label htmlFor="subject">subject (required):</label>
                    <Field name="subject" type="text" />
                    <ErrorMessage name="subject" component="div" className="errorLabel" />
                  </div>
                  <br></br>
    
                  <div>
                    <label htmlFor="body">body:</label>
                    <Field name="body" as="textarea" />
                    <ErrorMessage name="body" component="div" className="errorLabel" />
                  </div>
    
                  <div>
                <label htmlFor="hashtag">hashtags:</label>
                <Field 
                    name="hashtag" 
                    type="text" 
                    placeholder="hashtags"
                />
                <ErrorMessage name="hashtag" component="div" className="errorLabel" />
                </div>
                  <br />
    
                  <button type="submit" className="button" disabled={isSubmitting}>
                    save changes
                  </button>
                  <br />
                  <br />
                  <button
                    type="button"
                    className="button"
                    onClick={() => navigate(`/posts/${postId}`)}
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
