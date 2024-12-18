import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "../index.css";
import "../profilecard.css"

function ThatUser() {
    const { author } = useParams();
    const navigate = useNavigate();
    const [profile, setProfile] = useState({
        name: "",
        role: "",
        bio: "",
        age: "",
        gender: "",
    });
  
    useEffect(() => {
        if (author) {
            fetch(`/users/author/${author}`, { method: "GET" })
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    }
                    throw new Error("Failed to fetch profile data");
                })
                .then((data) => {
                    setProfile(data);   
                })
                .catch((error) => console.error("Error fetching profile:", error));
        }
    }, [author]);


      return (
        <div className="profile-card">
            <p>⋇⊶⊰❣⊱⊷⋇</p>
            <p>welcome to {author}'s profile!</p>
            <p><strong>role: </strong>{profile.role || "not set"}</p>
            <p><strong>name:</strong> {profile.name || "not set"}</p>
            <p><strong>age:</strong> {profile.age || "not set"}</p>
            <p><strong>gender:</strong> {profile.gender || "not set"}</p>
            <p><strong>bio:</strong> {profile.bio || "not set"}</p>
            <p><strong>contact email:</strong> {profile.email || "not set"}</p>
            <button className="button" onClick={() => navigate(`/posts`)}>back</button>
        </div>
    );
}

export default ThatUser;