import React, { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { useUserContext } from './UserContext';
import "../communitycard.css";

function HashtagResult({ handleEdit, handleDelete, pencil, trash }){
    const navigate = useNavigate();
    const { keyword } = useParams(); 
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { user } = useUserContext();

    const takeMeBack = () => {
        navigate('/community/posts/all');
      };

    useEffect(() => {
        setLoading(true);
        fetch(`/community/post/filterby/${keyword}`)
          .then((response) => {
            if (!response.ok) {
              throw new Error("Failed to fetch posts");
            }
            return response.json();
          })
          .then((data) => {
            setPosts(data);
            setLoading(false);
          })
          .catch((err) => {
            setError(err.message);
            setLoading(false);
          });
      }, [keyword]);
    
      if (loading) {
        return <p>loading...</p>;
      }
    
      if (error) {
        return <p>error: {error}</p>;
      }

      return (
        <div className="communitycard-displaycard-center">
            <div className="card">
                <div className="centered-elements">
                    <h3>filtering by '#{keyword}'</h3>
                <button onClick={takeMeBack} className="button">back to main community page</button>
                </div>
                {posts && posts.length > 0 ? (
                    posts.map((post) => (
                    <div key={post.id}>
                        <h3 style={{ fontSize: "20px" }}>
                        <Link to={`/community/post/${post.id}`}>{post.subject}</Link>
                        </h3>
                        <p style={{ fontSize: "14px" }}>{post.body}</p>
                        <p style={{ fontSize: "12px" }}>
                        posted by{" "}
                        <Link
                            to={`/profile/user/author/${post.author}`}
                            style={{ fontSize: "10px" }}
                        >
                            {post.author}
                        </Link>
                        , {post.role || "unknown role"}, on{" "}
                        {post.date
                            ? new Date(post.date).toLocaleString()
                            : "no date available"}
                        </p>
                        <div style={{ fontSize: "12px" }}>
                        <div className="hashtag">
                            {post.hashtags &&
                            post.hashtags.length > 0 &&
                            post.hashtags.map((hashtag, index) => (
                                <span key={hashtag.id || index}>
                                <Link
                                    to={`/community/post/filterby/${hashtag}`}
                                    style={{ fontSize: "10px" }}
                                >
                                    #{hashtag}
                                </Link>
                                {index < post.hashtags.length - 1 && ", "}
                                </span>
                            ))}
                        {user.username === post.author && (
                            <div className="edit-delete-buttons">
                            <button onClick={() => handleEdit(post.id)}><img src={pencil} alt="pencil" style={{ width: '20px', height: 'auto' }} /></button>
                            <button onClick={() => handleDelete(post.id)}><img src={trash} alt="trash" style={{ width: '20px', height: 'auto' }} /></button>
                            </div>
                        )}
                        </div>
                        </div>
                        <hr className="post-divider" />
                    </div>
                    ))
                ) : (
                    <p>no posts found for #{keyword}</p>
                )}
                </div>
            </div>
      );
    }
    
    export default HashtagResult;    