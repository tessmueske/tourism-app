import React, { createContext, useContext, useState, useEffect } from "react";

const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");

  useEffect(() => {
    const fetchCurrentUser = async () => {
      try {
        const response = await fetch(`/current-user/${email}`);
        if (!response.ok) {
          throw new Error(`HTTP error - status: ${response.status}`);
        }

        const data = await response.json();
        setEmail(data.email);
        console.log(email);
        setUsername(data.username);
        console.log(username);
      } catch (error) {
        console.error("Error fetching current user:", error);
      }
    };

    fetchCurrentUser();
  }, [email, username]);


  return (
    <UserContext.Provider value={{ email, setEmail, username, setUsername }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUserContext = () => useContext(UserContext);
