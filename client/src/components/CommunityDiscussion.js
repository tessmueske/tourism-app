import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useUserContext } from './UserContext';
import "../communitycard.css"

function CommunityDiscussion({ handleEdit, pencil, trash, confirmDelete, posts, setPosts }) {
  const navigate = useNavigate();
  const { username } = useUserContext();

  console.log(posts)

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
        <div className="centered-elements">
          <h2>community discussion</h2>
          <p>keep it nice and respectful, please!</p>
          <button onClick={handleNavigate} className="button">make a post</button>
        </div>
        
        {posts.length > 0 ? (
          posts.map((post) => (
            <div key={post.id}>
              <h3>
                <Link to={`/community/post/${post.id}`}>
                  {post.subject}
                </Link>
              </h3>
              <p>{post.body}</p>
              <p style={{ fontSize: '10px' }}>posted by {post.author} on {post.date}</p>
              <p style={{ fontSize: '12px' }}>{post.hashtag}</p>

              {username === post.author && (
                <div className="edit-delete-buttons">
                  <button onClick={() => handleEdit(post.id)}><img src={pencil} alt="pencil" style={{ width: '20px', height: 'auto' }} /></button>
                  <button onClick={() => confirmDelete(post.id)}><img src={trash} alt="trash" style={{ width: '20px', height: 'auto' }} /></button>
                </div>
              )}
              
              <hr className="post-divider" />
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