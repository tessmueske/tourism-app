import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
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
    <div className="communitycard-displaycard-center">
      <div className="card">
      <h2>community discussion</h2>
      <button onClick={handleNavigate} className="button">make a post</button>
      <div>
        {posts.length > 0 ? (
          posts.map((post) => (
            <div key={post.id}>
              <h3>
                <Link to={`/community/post/${post.id}`}>
                  {post.subject}
                </Link>
              </h3>
              <p>{post.text}</p>
              <p style={{ fontSize: '10px' }}>posted by {post.author} on {post.date}</p>
              <p className="hashtag">{post.hashtag}</p>
              <p>----------------------------------------------------------</p>
            </div>
          ))
        ) : (
          <p>no posts available. be the first one!</p>
        )}
      </div>
      </div>
    </div>
  );
}

export default CommunityDiscussion;