import React from "react";
import { Link } from "react-router-dom";
import '../index.css'; 

function Homepage() {
  return (
    <div>
      <div className="home-header">
        <h1 className="home-h1">⋇ welcome to magwa ⋇</h1>
      </div>
      <div className="center-container">
        <h2>we are an independent organization that promotes culturally and ecologically sensitive tourism in the canary islands.</h2>
        <Link to="/about" className="nav-link">click here to learn more about magwa</Link>
      </div>
    </div>
  );
}

export default Homepage;