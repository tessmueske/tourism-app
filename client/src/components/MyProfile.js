import React, { useEffect, useState } from "react";
import { useUserContext } from "./UserContext";
import { useNavigate } from "react-router-dom";
import "../index.css";
import "../profilecard.css"

function MyProfile() {
    const navigate = useNavigate();
    const { username, email, currentUser } = useUserContext();
    const [profile, setProfile] = useState({
        name: "",
        bio: "",
        age: "",
        gender: "",
    });

    useEffect(() => {
        fetch(`/profile/user/${email}`, { method: "GET" })
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
            throw new Error("Failed to fetch profile data");
          })
          .then((data) => setProfile(data))
          .catch((error) => console.error("Error fetching profile:", error));
      }, [email]);

      return (
        <div className="profile-card">
            <p>⋇⊶⊰❣⊱⊷⋇</p>
            <p>
              {username === currentUser ? 
                `welcome to your profile, ${username}!` : 
                `welcome to ${username}'s profile!`
              }
          </p>
          <p><strong>name:</strong> {profile.name || "N/A"}</p>
          <p><strong>age:</strong> {profile.age || "N/A"}</p>
          <p><strong>gender:</strong> {profile.gender || "N/A"}</p>
          <p><strong>bio:</strong> {profile.bio || "N/A"}</p>
          <p><strong>contact email:</strong> {profile.email || "N/A"}</p>
          <button className="button" onClick={() => navigate(`/profile/user/update/${email}`)}>edit my profile</button>
        </div>
      );
}

export default MyProfile;
