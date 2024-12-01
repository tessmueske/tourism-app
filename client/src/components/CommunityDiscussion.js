import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import '../index.css'; 
import "../communitycard.css"

function CommunityDiscussion() {
  const [posts, setPosts] = useState([]);
  const navigate = useNavigate();

  const handleNavigate = () => {
    navigate('/community/post/new');
  };

  useEffect(() => {
    fetch("/community/posts/all", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch posts");
        }
        return response.json();
      })
      .then((data) => setPosts(data)) 
      .catch((error) => console.error("Error fetching posts:", error));
  }, []);

  return (
    <div className="communitycard-display card">
      <h2>community discussion</h2>
      <button onClick={handleNavigate} className="button">make a post</button>
      <div className="post-list">
        {posts.length > 0 ? (
          posts.map((post) => (
            <div key={post.id} className="post-card">
              <h3>{post.subject}</h3>
              <p>{post.text}</p>
              <p>posted by {post.author} on {post.date}</p>
              <p className="hashtag">{post.hashtag}</p>
            </div>
          ))
        ) : (
          <p>no posts available. be the first one!</p>
        )}
      </div>
    </div>
  );
}

export default CommunityDiscussion;