import React, { useEffect, useState } from "react";
import { useUserContext } from "./UserContext";
import { useNavigate } from "react-router-dom";
import "../index.css";
import "../profilecard.css"

function MyProfile() {
    const navigate = useNavigate();
    const { username, email } = useUserContext();
    const [currentUser, setCurrentUser] = useState(null);
    const [profile, setProfile] = useState({
        name: "",
        bio: "",
        age: "",
        gender: "",
    });

    useEffect(() => {
      if (email) {
        fetch(`/current-user/${email}`)
          .then((response) => {
            if (!response.ok) {
              throw new Error("Failed to fetch current user data");
            }
            return response.json();
          })
          .then((data) => {
            setCurrentUser(data);
            console.log(currentUser)
          })
          .catch((error) => console.error("Error fetching current user:", error));
      }
    }, [email]);
  
    useEffect(() => {
      if (email) {
        fetch(`/profile/user/${email}`, { method: "GET" })
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
            throw new Error("Failed to fetch profile data");
          })
          .then((data) => setProfile(data))
          .catch((error) => console.error("Error fetching profile:", error));
      }
    }, [email]);
  
    if (!currentUser) {
      return <div>loading...</div>;
    }
  

      return (
        <div className="profile-card">
            <p>⋇⊶⊰❣⊱⊷⋇</p>
            <p>
              {username === currentUser?.username ? 
                `welcome to your profile, ${username}!` : 
                `welcome to ${username}'s profile!`
              }
          </p>
          <p><strong>name:</strong> {profile.name || "N/A"}</p>
          <p><strong>age:</strong> {profile.age || "N/A"}</p>
          <p><strong>gender:</strong> {profile.gender || "N/A"}</p>
          <p><strong>bio:</strong> {profile.bio || "N/A"}</p>
          <p><strong>contact email:</strong> {profile.email || "N/A"}</p>
          <p>
          {currentUser?.username === username && (
  <>
    <button
      className="button"
      onClick={() => navigate(`/profile/user/update/${email}`)}
    >
      edit my profile
    </button>
    <br></br>
    <br></br>
    <button
      className="button"
      onClick={() => navigate(`/profile/user/delete/${email}`)}
    >
      delete my profile
    </button>
  </>
)}

          </p>
        </div>
      );
}

export default MyProfile;
