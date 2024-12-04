import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "../index.css";
import "../profilecard.css"

function ThatUser({ post, user }) {
    const { author } = useParams();
    const navigate = useNavigate();
    const [profile, setProfile] = useState({
        name: "",
        bio: "",
        age: "",
        gender: "",
    });
    console.log('Author:', author);
  
    useEffect(() => {
        if (author) {
            fetch(`/profile/user/author/${author}`, { method: "GET" })
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    }
                    throw new Error("Failed to fetch profile data");
                })
                .then((data) => {
                    console.log(data);  
                    setProfile(data);   
                })
                .catch((error) => console.error("Error fetching profile:", error));
        }
    }, [author]);


      return (
        <div className="profile-card">
            <p>⋇⊶⊰❣⊱⊷⋇</p>
            <p>welcome to {author}'s profile!</p>
            <p><strong>name:</strong> {profile.name || "N/A"}</p>
            <p><strong>age:</strong> {profile.age || "N/A"}</p>
            <p><strong>gender:</strong> {profile.gender || "N/A"}</p>
            <p><strong>bio:</strong> {profile.bio || "N/A"}</p>
            <p><strong>contact email:</strong> {profile.email || "N/A"}</p>
            <button className="button" onClick={() => navigate(`/community/post/${post.id}`)}>back</button>
        </div>
    );
}

export default ThatUser;