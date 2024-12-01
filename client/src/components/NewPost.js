import React from "react";
import { useFormik, Form, Field, ErrorMessage } from "formik";
import * as Yup from 'yup';
import '../index.css'; 
import "../communitycard.css"

function NewPost() {

    const formik = useFormik({
        initialValues: {
          subject: "",
          body: "",
          hashtag: "",
        },
        onSubmit: (values) => {
        },
      });

  return (
    <div className="communitycard-display card">
      <p>new post</p>
      <p>add a hashtag (island, activity, price, age, etc)</p>
    </div>
  );
}

export default NewPost;