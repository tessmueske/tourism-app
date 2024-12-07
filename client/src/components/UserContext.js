import React, { createContext, useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState({
    email: "",
    username: "",
    role: "",
    name: "",
    age: "",
    gender: "",
    bio: ""
  });

  useEffect(() => {
    fetch("/current-user", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => setUser(data))
      .catch((err) => console.error("Error fetching user:", err));
  }, []);

  const handleAdvertiserLogin = ({ username, email, role, password }, { setSubmitting, setErrors }) => {
    fetch("/login/advertiser", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, email, role, password }),
    })
      .then((r) => {
        setSubmitting(false);
        if (r.ok) {
          r.json().then((userData) => {
            setUser({ username: userData.username, email: userData.email, role: userData.role });
            navigate("/welcome/home");
          });
        } else {
          r.json().then((err) => {
            setErrors({ api: err.errors || ["Signup failed"] });
          });
        }
      })
      .catch(() => {
        setSubmitting(false);
        setErrors({ api: ["Something went wrong. Please try again."] });
      });
  };

  const handleLocalExpertLogin = ({ username, email, role, password }, { setSubmitting, setErrors }) => {
    fetch("/login/localexpert", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, email, role, password }),
    })
      .then((r) => {
        setSubmitting(false);
        if (r.ok) {
          r.json().then((userData) => {
            setUser({ username: userData.username, email: userData.email, role: userData.role  });
            navigate("/welcome/home");
          });
        } else {
          r.json().then((err) => {
            setErrors({ api: err.errors || ["login failed"] });
          });
        }
      })
      .catch(() => {
        setSubmitting(false);
        setErrors({ api: ["something went wrong. please try again."] });
      });
  };

  const handleTravelerLogin = ({ username, email, role, password }, { setSubmitting, setErrors }) => {
    fetch("/login/traveler", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, email, role, password }),
    })
      .then((r) => {
        setSubmitting(false);
        if (r.ok) {
          r.json().then((userData) => {
            setUser(userData); 
            navigate("/welcome/home");
          });
        } else {
          r.json().then((err) => {
            setErrors({ api: err.errors || ["Signup failed"] });
          });
        }
      })
      .catch(() => {
        setSubmitting(false);
        setErrors({ api: ["Something went wrong. Please try again."] });
      });
  };


  const handleLogout = () => {
    fetch("/logout", { 
      method: "DELETE",
      credentials: "include"
    })
    .then((response) => {
      if (response.status === 204) {
        setUser(null);
        navigate("/");
      } else {
        console.error("Logout failed:", response);
      }
    })
    .catch((error) => {
      console.error("Logout failed:", error);
    });
  };

  return (
    <UserContext.Provider value={{ user, setUser, handleAdvertiserLogin, handleLocalExpertLogin, handleTravelerLogin, handleLogout }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUserContext = () => useContext(UserContext);