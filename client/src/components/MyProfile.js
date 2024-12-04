import React, { useEffect, useState } from "react";
import { useUserContext } from "./UserContext";
import { useNavigate } from "react-router-dom";
import "../index.css";
import "../profilecard.css"

function MyProfile() {
    const navigate = useNavigate();
    const { username, email } = useUserContext();
    const [profile, setProfile] = useState({
        name: "",
        bio: "",
        age: "",
        gender: "",
    });
  
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
    }, []);

    console.log(username)

      return (
        <div className="profile-card">
            <p>⋇⊶⊰❣⊱⊷⋇</p>
            <p>welcome to your profile, {username}!</p>
          <p><strong>name:</strong> {profile.name || "N/A"}</p>
          <p><strong>age:</strong> {profile.age || "N/A"}</p>
          <p><strong>gender:</strong> {profile.gender || "N/A"}</p>
          <p><strong>bio:</strong> {profile.bio || "N/A"}</p>
          <p><strong>contact email:</strong> {profile.email || "N/A"}</p>
          <button
                        className="button"
                        onClick={() => navigate(`/profile/user/update/${email}`)}
                    >
                        edit my profile
                    </button>
                    <br />
                    <br />
                    <button
                        className="button"
                        onClick={() => navigate(`/profile/user/delete/${email}`)}
                    >
                        delete my profile
                    </button>
        </div>
    );
}


export default MyProfile;
