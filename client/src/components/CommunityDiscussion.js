import React, { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useUserContext } from './UserContext';
import "../communitycard.css";

function CommunityDiscussion({ handleEdit, pencil, trash, confirmDelete, posts, setPosts }) {
  const navigate = useNavigate();
  const { user } = useUserContext();

  const handleNavigate = () => {
    navigate('/posts/new');
  };

  useEffect(() => {
    fetch("/posts", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("failed to fetch posts");
        }
        return response.json();
      })
      .then((data) => {
        setPosts(data.posts);
      })
      .catch((error) => console.error("error fetching posts:", error));
  }, [setPosts]);

  return (
    <div className="communitycard-displaycard-center">
      <div className="card">
        <div className="centered-elements">
          <h2>community discussion</h2>
          <p>keep it nice and respectful, please! click on a post to expand and comment. click on a hashtag to see posts related to that subject.</p>
          <button onClick={handleNavigate} className="button">make my own post</button>
        </div>
        {posts && posts.length > 0 ? (
          posts.map((post) => (
            <div key={post.id}>
              <h3 style={{ fontSize: '20px' }}>
                <Link to={`/posts/${post.id}`}>
                  {post.subject}
                </Link>
              </h3>
              <p style={{ fontSize: '14px' }}>{post.body}</p>
              <p style={{ fontSize: '12px' }}>
                posted by <Link to={`/user/author/${post.username}`} style={{ fontSize: '10px' }}>
                  {post.username}
                </Link> 
                , {post.role}, on{" "}
                {post.date
                  ? new Date(post.date).toLocaleString()
                  : "no date available"}
              </p>

              <div className="hashtag">
                  {post.hashtags && post.hashtags.length > 0 && post.hashtags.map((hashtag, index) => (
                      <span key={hashtag.id}>
                          <Link to={`/posts/filter/${hashtag.id}`} style={{ fontSize: '10px' }}>
                              #{hashtag.name}
                          </Link>
                          {index < post.hashtags.length - 1 && ", "}
                      </span>
                  ))}
              </div>
              
              <br></br>
              {user.username === post.username && (
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