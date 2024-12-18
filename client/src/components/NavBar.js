import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useUserContext } from "./UserContext";
import '../index.css'; 

function NavBar() { 
  const navigate = useNavigate();
  const { user, handleLogout } = useUserContext();

  const confirmLogout = () => {
    if (window.confirm("are you sure you want to log out?")) {
      handleLogout();
      navigate("/");
    }
  };

  return (
    <nav>
      <ul>
        {!user ? (
          <>
            <li>
              <Link to="/">home</Link>
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
              <Link to="/welcome/home">home</Link>
            </li>
            <li>
              <Link to={`/user/${user.email}`}>my profile</Link>
            </li>
            <li>
              <Link to="/posts">community discussion</Link>
            </li>
            <li>
              <Link to="/about">about us</Link>
            </li>
            <li>
              <Link to="/contact">contact us</Link>
            </li>
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

