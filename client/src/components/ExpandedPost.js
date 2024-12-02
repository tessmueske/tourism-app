import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useUserContext } from './UserContext';
import '../index.css'; 
import "../communitycard.css";

function ExpandedPost() {
    const navigate = useNavigate();
    const { postId } = useParams(); 
    const [post, setPost] = useState(null);
    const { username } = useUserContext();

    const loggedInUser = "currentLoggedInUser"; 

  useEffect(() => {
    fetch(`/community/post/${postId}`)
      .then((response) => response.json())
      .then((data) => setPost(data))
      .catch((error) => console.error("Error fetching post details:", error));
  }, [postId]);

  const handleEdit = () => {
    console.log(`Editing post with ID: ${postId}`);
    navigate(`/community/post/${postId}/edit`);
  };

  const handleDelete = () => {
    fetch(`/community/post/${postId}/delete`, {
      method: "DELETE",
    })
      .then((response) => {
        if (response.ok) {
          console.log("Post deleted successfully");
          setPost(null);
          alert("post deleted successfully");
          navigate("/community/posts/all");
        } else {
          console.error("Failed to delete post");
        }
      })
      .catch((error) => console.error("Error deleting post:", error));
  };

  return (
    <div className="communitycard-displaycard-center">
        <div className='card'>
      {post ? (
        <>
          <h2>{post.subject}</h2>
          <p>{post.body}</p>
          <p style={{ fontSize: '10px' }}>posted by {post.author} on {post.date}</p>
          <p className="hashtag">{post.hashtag}</p>
          {username === post.author && ( 
              <div>
                <button onClick={handleEdit} className="button">edit</button>
                <br></br>
                <br></br>
                <button onClick={handleDelete} className="button">delete</button>
              </div>
            )}
          </>
        ) : (
          <p>loading post details...</p>
        )}
      </div>
    </div>
  );
}

export default ExpandedPost;