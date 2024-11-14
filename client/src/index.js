import React from "react";
import App from "./components/App";
import "./index.css";
import { BrowserRouter } from "react-router-dom"; 
import ReactDOM from "react-dom/client"

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);