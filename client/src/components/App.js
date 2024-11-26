import React, { useEffect, useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import NavBar from "./NavBar";
import Homepage from "./Homepage";
import About from "./About";
import Login from "./Login";
import Signup from "./Signup";
import Contact from "./Contact";
import AdvertiserSignup from "./AdvertiserSignup";
import LocalExpertSignup from "./LocalExpertSignup";
import TravelerSignup from "./TravelerSignup";
import Welcome from "./Welcome";
import TravelerLogin from "./TravelerLogin"
import LocalExpertLogin from "./LocalExpertLogin";
import AdvertiserLogin from "./AdvertiserLogin";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch("/check_session").then((r) => {
      if (r.ok) {
        r.json().then((user) => setUser(user));
      }
    });
  }, []);

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
  }

  return (
    <>
      {user && <NavBar user={user} setUser={setUser} handleLogout={handleLogout} />}
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/homepage" replace />} />
          <Route path="/homepage" element={<Homepage />} />
          {!user ? (
            <>
              <Route path="/about" element={<About />}/>
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/signup/advertiser" element={<AdvertiserSignup />}/>
              <Route path="/signup/localexpert" element={<LocalExpertSignup />}/>
              <Route path="/signup/traveler" element={<TravelerSignup />}/>
              <Route path="/login/traveler" element={<TravelerLogin onLogin={setUser} />}/>
              <Route path="/login/advertiser" element={<AdvertiserLogin onLogin={setUser} />}/>
              <Route path="/login/localexpert" element={<LocalExpertLogin onLogin={setUser} />}/>
              <Route path="/verification/pending" element={<Pending />} />
            </>
          ) : (
            <>
              <Route path="/welcome/home" element={<Welcome />}/>
            </>
          )}
          
        </Routes>
      </main>
    </>
  );
}
export default App;
