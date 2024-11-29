import React, { useEffect, useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
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
import MyProfile from "./MyProfile";
import Pending from "./Pending";
import CommunityDiscussion from "./CommunityDiscussion"
import UpdateProfile from "./UpdateProfile";

function App() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("/check_session").then((r) => {
      if (r.ok) {
        r.json().then((user) => setUser(user));
      }
    });
  }, []);

  const onUpdate = (updatedProfile) => {};
  

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
    <>
      <NavBar user={user} setUser={setUser} handleLogout={handleLogout} />
    
      <main>
        <Routes>
          <Route path="/" element={<Homepage />} />
          
          {!user ? (
            <>
              <Route path="/about" element={<About />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/signup/advertiser" element={<AdvertiserSignup />} />
              <Route path="/signup/localexpert" element={<LocalExpertSignup />} />
              <Route path="/signup/traveler" element={<TravelerSignup setUser={setUser}/>} />
              <Route path="/login/traveler" element={<TravelerLogin setUser={setUser} />} />
              <Route path="/login/advertiser" element={<AdvertiserLogin setUser={setUser} />} />
              <Route path="/login/localexpert" element={<LocalExpertLogin setUser={setUser} />} />
              <Route path="/verification/pending" element={<Pending />} />
            </>
          ) : (
            <>
              <Route path="/welcome/home" element={<Welcome />} />
              <Route path="/profile/user/:email" element={<MyProfile />} />
              <Route path="/profile/user/:email/update" element={<UpdateProfile onUpdate={onUpdate}/>} />
              <Route path="/community" element={<CommunityDiscussion />} />
              <Route path="/contact" element={<Contact />} />
            </>
          )}
        </Routes>
      </main>
    </>
  );
}

export default App;