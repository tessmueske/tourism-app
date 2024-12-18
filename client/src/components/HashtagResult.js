import React, { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { useUserContext } from './UserContext';
import "../communitycard.css";

function HashtagResult({ handleEdit, handleDelete, pencil, trash }){
    const navigate = useNavigate();
    const { hashtagId } = useParams(); 
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { user } = useUserContext();

    const takeMeBack = () => {
        navigate('/posts');
      };

      useEffect(() => {
        setLoading(true);
        fetch(`/posts/filter/${hashtagId}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch posts");
                }
                return response.json();
            })
            .then((data) => {
                setPosts(data.posts);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, [hashtagId]);
    
    if (loading) {
        return <p>Loading...</p>;
    }
    
    if (error) {
        return <p>Error: {error}</p>;
    }

      return (
        <div className="communitycard-displaycard-center">
            <div className="card">
                <div className="centered-elements">
                    <h3>filtering by '#{hashtagId}'</h3>
                <button onClick={takeMeBack} className="button">back to main community page</button>
                </div>
                {posts && posts.length > 0 ? (
                    posts.map((post) => (
                    <div key={post.id}>
                        <h3 style={{ fontSize: "20px" }}>
                        <Link to={`/posts/${post.id}`}>{post.subject}</Link>
                        </h3>
                        <p style={{ fontSize: "14px" }}>{post.body}</p>
                        <p style={{ fontSize: "12px" }}>
                        posted by{" "}
                        <Link
                            to={`/user/author/${post.username}`}
                            style={{ fontSize: "10px" }}
                        >
                            {post.username}
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
                                    to={`/posts/${hashtagId}`}
                                    style={{ fontSize: "10px" }}
                                >
                                    #{hashtag}
                                </Link>
                                {index < post.hashtags.length - 1 && ", "}
                                </span>
                            ))}
                        {user.username === post.username && (
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
                    <p>no posts found for #{hashtagId}</p>
                )}
                </div>
            </div>
      );
    }
    
    export default HashtagResult;    