import React from "react";
import { Link } from "react-router-dom";
import '../index.css'; 

function NavBar({ user, handleLogout }) { 

  const confirmLogout = () => {
    if (window.confirm("Are you sure you want to log out?")) {
      handleLogout();
    }
  };


  return (
    <nav>
      <ul>
        {!user ? (
          <>
            <li>
              <Link to="/homepage">home</Link>
            </li>
            <li>
              <Link to="/about">about us</Link>
            </li>
            <li>
              <Link to="/login">log in</Link>
            </li>
            <li>
              <Link to="/signup">sign up</Link>
            </li>
            <li>
              <Link to="/contact">contact us</Link>
            </li>
          </>
        ) : (
          <>
            <li>
              <Link to="/homepage">home</Link>
            </li>
            <li>
              <Link to="/profile">my profile</Link>
            </li>
              <Link to="/community">community discussion</Link>
            <li>
              <button onClick={confirmLogout}>log out</button>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
}

export default NavBar;
