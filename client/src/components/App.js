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
import Thanks from "./Thanks";
import TravelerLogin from "./TravelerLogin"
import LocalExpertLogin from "./LocalExpertLogin";
import AdvertiserLogin from "./AdvertiserLogin";
import Landing from "./Landing"

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
          <Route path="/landing" element={<Landing />} />
          <Route path="/about" element={<About />}/>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/signup/advertiser" element={<AdvertiserSignup />}/>
          <Route path="/signup/localexpert" element={<LocalExpertSignup />}/>
          <Route path="/signup/traveler" element={<TravelerSignup />}/>
          <Route path="/welcome/home" element={<Welcome />}/>
          <Route path="/thanks" element={<Thanks />}/>
          <Route path="/login/traveler" element={<TravelerLogin onLogin={setUser} />}/>
          <Route path="/login/advertiser" element={<AdvertiserLogin onLogin={setUser} />}/>
          <Route path="/login/localexpert" element={<LocalExpertLogin onLogin={setUser} />}/>
        </Routes>
      </main>
    </>
  );
}
export default App;

