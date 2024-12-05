import { useParams, useNavigate, Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useUserContext } from './UserContext';
import '../index.css'; 
import "../communitycard.css";

function ExpandedPost({ handleEdit, setPost, post, pencil, trash, confirmDelete }) {
    const navigate = useNavigate();
    const { username } = useUserContext();
    const { postId } = useParams(); 

    useEffect(() => {
        console.log("Post ID from useParams:", postId);
      }, [postId]);

    useEffect(() => {    
        fetch(`/community/post/${postId}`)
          .then((response) => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
          })
          .then((data) => {
            setPost(data); 
          })
          .catch((error) => console.error("Error fetching post details:", error));
      }, [postId, setPost]);
    

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
          <p style={{ fontSize: '10px' }}>posted by <Link to={`/profile/user/author/${post.author}`} style={{ fontSize: '10px' }}>{post.author}</Link> on {post.date}</p>
          <p style={{ fontSize: '12px' }}>
                <div className='hashtag'>
                {post.hashtags.map((hashtag, index) => (<span key={hashtag.name}>#{hashtag.name}{index < post.hashtags.length - 1 && ", "}</span>))}
                </div>
                </p>
            <p>comments:</p>
          <div className="button-group">
            <button onClick={backNavigate} className="button">go back</button>
            {username === post.author && (
                <div className="edit-delete-buttons">
                  <button onClick={() => handleEdit(postId)}><img src={pencil} alt="pencil" style={{ width: '20px', height: 'auto' }} /></button>
                  <button onClick={() => confirmDelete(postId)}><img src={trash} alt="trash" style={{ width: '20px', height: 'auto' }} /></button>
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