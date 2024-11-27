import React, { useEffect, useState } from "react";
import { useUserContext } from "./UserContext";
import { useNavigate } from "react-router-dom";
import "../index.css";
import "../card.css"

function MyProfile() {
    const navigate = useNavigate();
    const { username, email } = useContext(useUserContext);
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
      }, [email, username]); 

      console.log("Username from context:", username);

      const handleClick = () => {
        navigate(`/profile/user/${email}/update`);
      };

      return (
        <div className="profile-display card">
          <p>welcome to your profile, {username}!</p>
          <p>⋇⊶⊰❣⊱⊷⋇</p>
          <p><strong>name:</strong> {profile.name || "N/A"}</p>
          <p><strong>bio:</strong> {profile.bio || "N/A"}</p>
          <p><strong>age:</strong> {profile.age || "N/A"}</p>
          <p><strong>gender:</strong> {profile.gender || "N/A"}</p>
          <button onClick={handleClick}>edit my profile</button>
        </div>
      );
}

export default MyProfile;
