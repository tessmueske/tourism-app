import React, { useEffect, useState } from "react";
import { useUserContext } from "./UserContext";
import "../index.css";

function MyProfile() {
    const { email, username } = useUserContext();
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
    <div className="account-center-container">
      <p>welcome to your profile, {username}!</p>

      <div className="profile-display">
        <p><strong>name:</strong> {profile.name || "N/A"}</p>
        <p><strong>bio:</strong> {profile.bio || "N/A"}</p>
        <p><strong>age:</strong> {profile.age || "N/A"}</p>
        <p><strong>gender:</strong> {profile.gender || "N/A"}</p>
      </div>
    </div>
  );
}

export default MyProfile;
