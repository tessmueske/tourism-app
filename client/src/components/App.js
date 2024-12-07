import React, { useEffect, useState } from "react";
import { Routes, Route, useNavigate, useParams } from "react-router-dom";
import { useUserContext } from "./UserContext";
import NavBar from "./NavBar";
import Homepage from "./Homepage";
import About from "./About";
import Login from "./Login";
import Signup from "./Signup";
import Contact from "./Contact";
import AdvertiserSignup from "./AdvertiserSignup";
import LocalExpertSignup from "./LocalExpertSignup";
import TravelerSignup from "./TravelerSignup";
import Welcome from "./Welcome";
import TravelerLogin from "./TravelerLogin"
import LocalExpertLogin from "./LocalExpertLogin";
import AdvertiserLogin from "./AdvertiserLogin";
import MyProfile from "./MyProfile";
import Pending from "./Pending";
import CommunityDiscussion from "./CommunityDiscussion"
import UpdateProfile from "./UpdateProfile";
import NewPost from "./NewPost";
import ExpandedPost from "./ExpandedPost"
import EditPost from "./EditPost";
import ThatUser from "./ThatUser";
import pencil from '../pencil.png';
import trash from '../trash.png';

function App() {
  const [post, setPost] = useState(null);
  const [posts, setPosts] = useState([]);
  const navigate = useNavigate();
  const { postId } = useParams(); 
  const { user, setUser } = useUserContext();

  const onUpdate = (updatedProfile) => {};

  const handleEdit = (postId) => {
    console.log("Editing post with ID:", postId);
    if (postId) {
      navigate(`/community/post/edit/${postId}`); 
    } else {
      console.error('postId is undefined');
    }
  };

  const confirmDelete = (postId) => {
    if (window.confirm("Are you sure you want to delete this post?")) {
      handleDelete(postId);
    }
  };

  const handleDelete = (postId) => {
    console.log("Post ID inside handleDelete:", postId);
    fetch(`/community/post/delete/${postId}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (response.ok) {
          console.log("Post deleted successfully");
          alert("Post deleted successfully");
          setPosts((prevPosts) => prevPosts.filter((post) => post.id !== postId));
          if (post && post.id === postId) {
            setPost(null);
          }
        } else {
          console.error("Failed to delete post");
        }
      })
      .catch((error) => console.error("Error deleting post:", error));
  };

  return (
    <>
      <NavBar />
    
      <main>
        <Routes>
          <Route path="/" element={<Homepage />} />
          
          {!user ? (
            <>
              <Route path="/about" element={<About />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/signup/advertiser" element={<AdvertiserSignup />} />
              <Route path="/signup/localexpert" element={<LocalExpertSignup />} />
              <Route path="/signup/traveler" element={<TravelerSignup />} />
              <Route path="/login/traveler" element={<TravelerLogin />} />
              <Route path="/login/advertiser" element={<AdvertiserLogin />} />
              <Route path="/login/localexpert" element={<LocalExpertLogin />} />
              <Route path="/verification/pending" element={<Pending />} />
            </>
          ) : (
            <>
              <Route path="/welcome/home" element={<Welcome />} />
              <Route path="/profile/user/:email" element={<MyProfile />} />
              <Route path="/profile/user/update/:email" element={<UpdateProfile onUpdate={onUpdate} />} />
              <Route 
                path="/community/posts/all" 
                element={
                <CommunityDiscussion 
                  handleEdit={handleEdit} 
                  handleDelete={handleDelete} 
                  pencil={pencil} 
                  trash={trash} 
                  confirmDelete={confirmDelete} 
                  posts={posts} 
                  setPosts={setPosts} 
                  />
                }/>
              <Route path="/community/post/new" element={<NewPost />} />
              <Route path="/community/post/:postId" element={<ExpandedPost post={post} setPost={setPost} handleEdit={handleEdit} handleDelete={handleDelete} pencil={pencil} trash={trash} posts={posts} setPosts={setPosts}/>} />
              <Route path="/community/post/edit/:postId" element={<EditPost postId={postId} />} />
              <Route path="/profile/user/author/:author" element={<ThatUser post={post} user={user} />} />
              <Route path="/contact" element={<Contact />} />
            </>
          )}
        </Routes>
      </main>
    </>
  );
}

export default App;

// comment on post actions
// implement hashtags
// take out date from the editpost component
// code for back button from thatusers profile
// add role type on profile