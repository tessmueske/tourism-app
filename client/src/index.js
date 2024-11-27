import React from "react";
import App from "./components/App";
import "./index.css";
import { BrowserRouter } from "react-router-dom"; 
import { UserProvider } from "./UserContext";
import ReactDOM from "react-dom/client"

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BrowserRouter>
    <UserProvider>
      <App />
    </UserProvider>
  </BrowserRouter>
);