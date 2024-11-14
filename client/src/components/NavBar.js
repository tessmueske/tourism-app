import React from "react";
import { Link } from "react-router-dom";
import '../index.css'; 

function NavBar(){
  return (
    <>
      <nav>
        <ul>
          <li>
            <Link to="/homepage">home</Link>
          </li>
          <li>
            <Link to="/about">about magwa</Link>
          </li>
          <li>
            <Link to="/contact">contact us</Link>
          </li>
        </ul>
      </nav>
    </>
  );
};

export default NavBar;