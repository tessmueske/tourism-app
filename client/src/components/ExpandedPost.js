import { useParams, useNavigate, Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useUserContext } from './UserContext';
import '../index.css'; 
import "../communitycard.css";

function ExpandedPost({ handleEdit, pencil, trash, confirmDelete }) {
    const navigate = useNavigate();
    const { user } = useUserContext();
    const { postId } = useParams(); 
    const [newComment, setNewComment] = useState('');
    const [post, setPostState] = useState(null); 
    const [loading, setLoading] = useState(true); 

    useEffect(() => {
    }, [postId]);

    useEffect(() => {    
        setLoading(true); 
        fetch(`/community/post/${postId}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                setPostState({
                    ...data,
                    comments: data.comments || []
                });
                setLoading(false);
                console.log('Fetched post data:', data);
                console.log('Fetched comments:', data.comments);
            })
            .catch((error) => {
                console.error("Error fetching post details:", error);
                setLoading(false);
            });
    }, [postId]);

    const handleCommentSubmit = (e) => {
        e.preventDefault();
        
        if (!newComment.trim()) return;  // Prevent submitting if the comment is empty
    
        const commentData = {
            text: newComment,
            author: user.username,
            role: user.role,
            date: new Date().toISOString(),  // Using ISO string for date consistency
        };
    
        fetch(`/community/post/${postId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(commentData), // Send the comment data to the server
        })
        .then(response => response.json())  // Parse the JSON response
        .then(data => {
            // Ensure comments are always parsed correctly
            const parsedComments = typeof data.comments === 'string' ? JSON.parse(data.comments) : data.comments;
            setPostState(prevPost => ({
                ...prevPost,
                comments: parsedComments || [] // Append the new comment to the post
            }));
            setNewComment(''); // Clear the comment input after submission
        })
        .catch(error => console.error('Error submitting comment:', error)); // Log any errors
    };

    const backNavigate = () => {
        navigate("/community/posts/all");
    };

    if (loading) {
        return <p>loading post details...</p>;
    }

    const handleCommentDelete = (e, comment_id) => {
        e.preventDefault();
        console.log("Post ID:", postId);
        console.log("Comment ID:", comment_id); 
        fetch(`/posts/${postId}/comments/${comment_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include'
        })
        .then(response => response.json())  // Parse the JSON response
        .then(data => {
            // Assuming the updated post is returned with the comments after deletion
            setPostState(prevPost => ({
                ...prevPost,
                comments: data.comments || []  // Assuming the response includes the updated comments
            }));
        })
        .catch(error => console.error('Error deleting comment:', error)); // Log any errors
    };

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
                        <div style={{ fontSize: '12px' }}>
                            <div className='hashtag'>
                            {Array.isArray(post.hashtags) && post.hashtags.length > 0 && (
                                post.hashtags.map((hashtag, index) => (
                                    <span key={hashtag}>
                                        {hashtag}
                                        {index < post.hashtags.length - 1 && ", "}
                                    </span>
                                ))
                            )}
                            </div>
                        </div>
                        <div className="button-group">
                            {user.username === post.author && (
                                <div className="edit-delete-buttons">
                                    <button onClick={() => handleEdit(postId)}>
                                        <img src={pencil} alt="pencil" style={{ width: '20px', height: 'auto' }} />
                                    </button>
                                    <button onClick={() => confirmDelete(postId)}>
                                        <img src={trash} alt="trash" style={{ width: '20px', height: 'auto' }} />
                                    </button>
                                </div>
                            )}
                        </div>
                        <p style={{ textDecoration: 'underline' }}>comments:</p>
                        <hr className="post-divider" />
                        <div>
                            {Array.isArray(post.comments) && post.comments.length > 0 ? (
                                post.comments.filter(comment => comment && comment.text).map((comment) => (
                                    <div key={comment.timestamp}>
                                        <p>{comment.text}</p>
                                        {user.username === comment.author && (
                                            <div className="edit-delete-buttons">
                                                <button onClick={(e) => {
                                                    console.log("Comment object before delete:", comment); // Debugging line
                                                    handleCommentDelete(e, comment.id);
                                                }}>
                                                    <img src={trash} alt="trash" style={{ width: '20px', height: 'auto' }} />
                                                </button>
                                            </div>
                                        )}
                                        <p style={{ fontSize: '10px' }}>
                                            <em>- <Link to={`/profile/user/author/${comment.author}`} style={{ fontSize: '10px' }}>
                                                {comment.author}
                                            </Link>,{comment.author.role}, on{" "}
                                            {comment.date ? new Date(comment.date).toLocaleString() : "no date available"}
                                            </em>
                                        </p>
                                        <p style={{ fontSize: '10px', fontStyle: 'italic' }}>
                                        </p>
                                        <hr className="post-divider" />
                                    </div>
                                ))
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
                        <button onClick={backNavigate} className="button">go back</button>
                    </>
                ) : (
                    <p>post data is not available right now. sorry!</p>
                )}
            </div>
        </div>
    );
}

export default ExpandedPost;
