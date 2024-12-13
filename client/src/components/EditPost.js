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
        fetch(`/community/post/${postId}`)
          .then((response) => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
          })
          .then((data) => {
            // Ensure hashtags is an array, check the type of `data.hashtags`
            let hashtags = [];
            if (Array.isArray(data.hashtags)) {
                hashtags = data.hashtags;  // If it's already an array, use it directly
            } else if (typeof data.hashtags === 'string') {
                hashtags = data.hashtags.split(' ').map((hashtag) => hashtag.trim()).filter(Boolean);  // Split string to array
            }
            
            setInitialValues({
                author: user?.username || '',
                subject: data.subject,
                body: data.body,
                hashtag: hashtags,  // Ensure hashtag is always an array
            });
        })
          .catch((error) => console.error("Error fetching post data:", error));
      }, [postId]);

      const handleSubmit = (values) => {
        let updatedHashtags;

        if (Array.isArray(values.hashtag)) {
            updatedHashtags = values.hashtag;
        } else if (typeof values.hashtag === 'string') {
            updatedHashtags = values.hashtag.split(' ').map((hashtag) => hashtag.trim()).filter(Boolean);
        } else {
            updatedHashtags = [];
        }
    
        console.log("Form values before submit:", values);
        console.log("Updated hashtags array:", updatedHashtags);
    
        fetch(`/community/post/edit/${postId}`, {
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
        .then((responseData) => {
            console.log("Response data from backend:", responseData);
            navigate(`/community/post/${postId}`);
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
                <label htmlFor="hashtag">hashtags #typed #like #this!:</label>
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
