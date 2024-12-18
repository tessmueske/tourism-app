import { useParams, useNavigate, Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useUserContext } from './UserContext';
import "../index.css"; 
import "../communitycard.css";

function ExpandedPost({ handleEdit, pencil, trash, confirmDelete }) {
    const navigate = useNavigate();
    const { user } = useUserContext();
    const { postId } = useParams(); 
    const [newComment, setNewComment] = useState('');
    const [post, setPostState] = useState(null); 
    const [loading, setLoading] = useState(true); 

    useEffect(() => {    
        setLoading(true); 
        fetch(`/community/posts/${postId}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                setPostState(data);  
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error fetching post details:", error);
                setLoading(false);
            });
    }, [postId]);

    const handleCommentSubmit = (e) => {
        e.preventDefault();
    
        if (!user) {
            console.error("User is not defined");
            return;
        }
    
        if (!newComment.trim()) return;  
    
        const commentData = {
            text: newComment,
            author: user.username,
            post_id: postId,
            date: new Date().toISOString()
        };
    
        fetch(`/community/posts/${postId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(commentData), 
        })
        .then(response => response.json())
        .then(data => {
            return fetch(`/community/posts/${postId}`);
        })
        .then(response => response.json())
        .then(updatedPost => {
            console.log("Updated Post:", updatedPost);
            setPostState(updatedPost); 
            setNewComment('');
        })
        .catch(error => console.error('Error submitting comment:', error)); 
    };
    
    

    const handleCommentDelete = (e, comment_id) => {
        e.preventDefault();
        
        fetch(`/posts/${postId}/comments/${comment_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ comment_id })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            setPostState(prevPost => ({
                ...prevPost,
                comments: prevPost.comments.filter(comment => comment.id !== comment_id)
            }));
        })
        .catch(error => console.error('Error deleting comment:', error)); 
    };

    const backNavigate = () => {
        navigate("/community/posts");
    };

    if (loading) {
        return <p>loading post details...</p>;
    }
    
    if (!post) {
        return <p>post not found</p>;
    }

    return (
        <div className="communitycard-displaycard-center">
            <div className='card'>
                {post ? (
                    <>
                        <h2>{post.subject}</h2>
                        <p>{post.body}</p>
                        <p style={{ fontSize: '12px' }}>
                            posted by <Link to={`/profile/user/author/${post.author}`} style={{ fontSize: '10px' }}>
                            {post.author}
                            </Link> 
                            , {post.role}, on{" "}{post.date
                            ? new Date(post.date).toLocaleString()
                            : "no date available"}
                        </p>
                        <div className="hashtag">
                            {post.hashtags && post.hashtags.length > 0 && post.hashtags.map((hashtag, index) => (
                                <span key={hashtag}>
                                    <Link to={`/community/posts/filter/${hashtag}`} style={{ fontSize: '10px' }}>
                                        #{hashtag}
                                    </Link>
                                    {index < post.hashtags.length - 1 && ", "}
                                </span>
                            ))}
                        </div>
                        <div className="button-group">
                            {user.username === post.author && (
                                <div className="edit-delete-buttons">
                                    <button onClick={() => handleEdit(postId)}>
                                        <img src={pencil} alt="Edit" style={{ width: '20px', height: 'auto' }} />
                                    </button>
                                    <button onClick={() => confirmDelete(postId)}>
                                        <img src={trash} alt="Delete" style={{ width: '20px', height: 'auto' }} />
                                    </button>
                                </div>
                            )}
                        </div>
                        <p style={{ textDecoration: 'underline' }}>comments:</p>
                        <hr className="post-divider" />
                        <div>
                        {post.comments && post.comments.length > 0 ? (
                            post.comments.map((comment) => {
                                if (!comment) return null; 
                                console.log('Rendering comment:', comment); 
                                return (
                                    <div key={comment.id}>
                                        <p>{comment.text}</p>
                                        {user.username === comment.author && (
                                            <div className="edit-delete-buttons">
                                                <button onClick={(e) => handleCommentDelete(e, comment.id)}>
                                                    <img src={trash} alt="Delete" style={{ width: '20px', height: 'auto' }} />
                                                </button>
                                            </div>
                                        )}
                                        <p style={{ fontSize: '10px' }}>
                                            <em>- <Link to={`/profile/user/author/${comment.author}`} style={{ fontSize: '10px' }}>
                                                {comment.author}
                                            </Link>, {comment.role}, on{" "}
                                            {comment.date ? new Date(comment.date).toLocaleString() : "no date available"}
                                            </em>
                                        </p>
                                        <hr className="post-divider" />
                                    </div>
                                );
                            })
                        ) : (
                            <p style={{ fontSize: '12px' }}><em>no comments</em></p>
                        )}
                        </div>
                        <form onSubmit={handleCommentSubmit}>
                            <textarea
                                value={newComment}
                                onChange={(e) => setNewComment(e.target.value)}
                                placeholder="add a comment..."
                                className="small-textarea"
                            />
                            <div className="inputContainer">
                                <p style={{ fontSize: '12px' }}>author: {user.username}</p>
                            </div>
                            <button type="submit" className="button">submit comment</button>
                        </form>
                        <br />
                        <button onClick={backNavigate} className="button">back to all posts</button>
                    </>
                ) : (
                    <p>Loading post...</p>
                )}
            </div>
        </div>
    );
}

export default ExpandedPost;
