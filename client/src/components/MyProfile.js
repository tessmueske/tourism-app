import React, { useEffect, useState } from "react";
import { useUserContext } from "./UserContext";
import { useNavigate } from "react-router-dom";
import "../index.css";
import "../profilecard.css"

function MyProfile() {
    const navigate = useNavigate();
    const { user, setUser } = useUserContext();
  
    useEffect(() => {
      fetch(`/profile/user/${user.email}`, { method: "GET" })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
          throw new Error("Failed to fetch profile data");
        })
        .then((data) => setUser(data))
        .catch((error) => console.error("Error fetching profile:", error));
  }, [user.email]);

  const handleDeleteProfile = async () => {
    try {
        const response = await fetch(`/profile/user/delete/${user.email}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            navigate('/'); 
        } else {
            const errorData = await response.json();
            console.error('Error deleting profile:', errorData.error);
            alert('Failed to delete the profile.');
        }
    } catch (error) {
        console.error('An error occurred while deleting the profile:', error);
        alert('An error occurred. Please try again later.');
    }
};

      return (
        <div className="profile-card">
            <p>⋇⊶⊰❣⊱⊷⋇</p>
            <p>welcome to your profile, {user.username}!</p>
          <p><strong>role: </strong>{user.role || "not set"}</p>
          <p><strong>name:</strong> {user.name || "N/A"}</p>
          <p><strong>age:</strong> {user.age || "N/A"}</p>
          <p><strong>gender:</strong> {user.gender || "N/A"}</p>
          <p><strong>bio:</strong> {user.bio || "N/A"}</p>
          <p><strong>contact email:</strong> {user.email || "N/A"}</p>
          <button
                        className="button"
                        onClick={() => navigate(`/profile/user/update/${user.email}`)}
                    >
                        edit my profile
                    </button>
                    <br />
                    <br />
                    <button
                        className="button"
                        onClick={(handleDeleteProfile)}
                    >
                        delete my profile
                    </button>
        </div>
    );
}


export default MyProfile;
