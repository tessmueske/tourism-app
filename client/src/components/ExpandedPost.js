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
        console.log("Post ID from useParams:", postId);
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
        
        if (!newComment.trim()) return;  

        const commentData = {
            text: newComment,
            author: user.username, 
        };

        fetch(`/community/post/${postId}/comments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(commentData),
        })
        .then(response => response.json())
        .then(data => {
            setPostState((prevPost) => ({
                ...prevPost,
                comments: [...prevPost.comments, data], 
            }));
            setNewComment(''); 
        })
        .catch(error => console.error('Error submitting comment:', error));
    };

    const backNavigate = () => {
        navigate("/community/posts/all");
    };

    if (loading) {
        return <p>loading post details...</p>;
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
                            , {post.role}, on{" "}
                            {post.date
                            ? new Date(post.date).toLocaleString()
                            : "no date available"}
                        </p>
                        <div style={{ fontSize: '12px' }}>
                            <div className='hashtag'>
                                {post.hashtags.map((hashtag, index) => (
                                    <span key={hashtag}>
                                        #{hashtag}
                                        {index < post.hashtags.length - 1 && ", "}
                                    </span>
                                ))}
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
                        <div>
                            {post.comments && post.comments.length > 0 ? (
                            post.comments.map((comment) => (
                            <div key={comment.id}>
                            <p>{comment.text}</p>
                            <p style={{ fontSize: '10px' }}><em>- <Link to={`/profile/user/author/${post.author}`} style={{ fontSize: '10px' }}>
                            {post.author}
                            </Link> , {post.role}, on{" "}
                            {post.date
                            ? new Date(post.date).toLocaleString()
                            : "no date available"}</em></p>
                        </div>
                        ))
                    ) : (
                    <p style={{ fontSize: '12px' }}><em>no comments </em></p>
                    )}
                    </div>
                        <form onSubmit={handleCommentSubmit}>
                            <textarea
                                value={newComment}
                                onChange={(e) => setNewComment(e.target.value)}
                                placeholder="add a comment..."
                            />
                            <button type="submit" className='button'>submit comment</button>
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
