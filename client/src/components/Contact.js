import React from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import "../index.css"; 

function Contact() {

  const validationSchema = Yup.object({
    name: Yup.string().required("Name is required"),
    email: Yup.string().email("Invalid email format").required("Email is required"),
    message: Yup.string().required("Message is required"),
  });

  const formik = useFormik({
    initialValues: {
      name: "",
      email: "",
      message: "",
    },
    validationSchema,
    onSubmit: (values) => {
    },
  });

  return (
    <div className='center-container'>
      <h1>we want to hear from you.</h1>
      <p>
        do you have suggestions for improvement? a new idea? something you don't like? 
        want to report a bug? <span className="bold">we'd love to hear from you.</span>
      </p>
      <p>fill out the form below and we'll be in touch!</p>

      <form
        action="https://formspree.io/f/movqlnak"
        method="POST"
        className="contact-form"
        onSubmit={formik.handleSubmit} 
      >
        <div>
          <label htmlFor="name">name</label>
          <br></br>
          <input
            type="text"
            id="name"
            name="name"
            onChange={formik.handleChange}
            value={formik.values.name}
            placeholder="Your Name"
          />
          {formik.errors.name && formik.touched.name && (
            <div className="error">{formik.errors.name}</div>
          )}
        </div>
        <br></br>

        <div>
          <label htmlFor="email">email</label>
          <br></br>
          <input
            type="email"
            id="email"
            name="email"
            onChange={formik.handleChange}
            value={formik.values.email}
            placeholder="Your Email"
          />
          {formik.errors.email && formik.touched.email && (
            <div className="error">{formik.errors.email}</div>
          )}
        </div>
        <br></br>

        <div>
          <label htmlFor="message">message</label>
          <br></br>
          <textarea
            id="message"
            name="message"
            onChange={formik.handleChange}
            value={formik.values.message}
            placeholder="Your message..."
            rows="6"
          />
          {formik.errors.message && formik.touched.message && (
            <div className="error">{formik.errors.message}</div>
          )}
        </div>
        <br></br>

        <button type="submit" className="submit-button">
          Submit
        </button>
      </form>
    </div>
  );
}

export default Contact;
