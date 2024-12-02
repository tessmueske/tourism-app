import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useUserContext } from './UserContext';
import '../index.css'; 
import "../communitycard.css";

function ExpandedPost({ handleEdit, handleDelete, setPost, post, pencil, trash }) {
    const navigate = useNavigate();
    const { username } = useUserContext();
    const { postId } = useParams(); 

  useEffect(() => {
    fetch(`/community/post/${postId}`)
      .then((response) => response.json())
      .then((data) => setPost(data))
      .catch((error) => console.error("Error fetching post details:", error));
  }, [postId]);

  const backNavigate = () => {
    navigate("/community/posts/all");
  }

  return (
    <div className="communitycard-displaycard-center">
        <div className='card'>
      {post ? (
        <>
          <h2>{post.subject}</h2>
          <p>{post.body}</p>
          <p style={{ fontSize: '10px' }}>posted by {post.author} on {post.date}</p>
          <p className="hashtag">{post.hashtag}</p>
          <div className="button-group">
            <button onClick={backNavigate} className="button">go back</button>
            {username === post.author && ( 
             <div className="edit-delete-buttons">
                <button onClick={handleEdit}>
                    <img src={pencil} alt="pencil" style={{ width: '20px', height: 'auto' }} />
                    </button>
                <button onClick={handleDelete} ><img src={trash} alt="trash" style={{ width: '20px', height: 'auto' }} /></button>
              </div>
            )}
          </div>
        </>
      ) : (
        <p>loading post details...</p>
      )}
    </div>
  </div>
);
}

export default ExpandedPost;