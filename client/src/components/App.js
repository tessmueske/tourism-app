import React, { useEffect, useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import NavBar from "./NavBar";
import Homepage from "./Homepage";
import About from "./About";
import Login from "./Login";
import Signup from "./Signup";
import Contact from "./Contact";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch("/check_session").then((r) => {
      if (r.ok) {
        r.json().then((user) => setUser(user));
      }
    });
  }, []);

  return (
    <>
      <NavBar />
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/homepage" replace />} />
          <Route path="/homepage" element={<Homepage />} />
          <Route path="/about" element={<About />}/>
          <Route path="/login" element={<Login onLogin={setUser} />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </main>
    </>
  );
}
export default App;

