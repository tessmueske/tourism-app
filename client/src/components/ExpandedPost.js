import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import '../index.css'; 
import "../communitycard.css";

function ExpandedPost() {
  const { postId } = useParams(); 
  const [post, setPost] = useState(null);

  useEffect(() => {
    fetch(`/community/post/${postId}`)
      .then((response) => response.json())
      .then((data) => setPost(data))
      .catch((error) => console.error("Error fetching post details:", error));
  }, [postId]);

  return (
    <div className="communitycard-displaycard-center">
        <div className='card'>
      {post ? (
        <>
          <h2>{post.subject}</h2>
          <p>{post.body}</p>
          <p style={{ fontSize: '10px' }}>posted by {post.author} on {post.date}</p>
          <p className="hashtag">{post.hashtag}</p>
        </>
      ) : (
        <p>Loading post details...</p>
      )}
    </div>
    </div>
  );
}

export default ExpandedPost;
