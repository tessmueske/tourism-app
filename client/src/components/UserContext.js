import React, { createContext, useContext, useState } from "react";

const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [email, setEmail] = useState("user@example.com");
  const [username, setUsername] = useState("exampleuser");

  return (
    <UserContext.Provider value={{ email, setEmail, username, setUsername }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUserContext = () => useContext(UserContext);
