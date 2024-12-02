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
import pencil from '../pencil.png';
import trash from '../trash.png';

function App() {
  const [user, setUser] = useState(null);
  const [post, setPost] = useState(null);
  const navigate = useNavigate();
  const { postId } = useParams(); 
  const { email } = useUserContext();
 
  useEffect(() => {
    fetch("/check_session").then((r) => {
      if (r.ok) {
        r.json().then((user) => {
          console.log(user);
          setUser(user);
        });
      }
    });
  }, []);

  const onUpdate = (updatedProfile) => {};

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
  
  const handleLogout = () => {
    fetch("/logout", { 
      method: "DELETE",
      credentials: "include"
    })
    .then((response) => {
      if (response.status === 204) {
        setUser(null);
        localStorage.removeItem("authToken");
        navigate("/");
      } else {
        console.error("Logout failed:", response);
      }
    })
    .catch((error) => {
      console.error("Logout failed:", error);
    });
  };

  return (
    <>
      <NavBar user={user} setUser={setUser} handleLogout={handleLogout} />
    
      <main>
        <Routes>
          <Route path="/" element={<Homepage />} />
          
          {!user ? (
            <>
              <Route path="/about" element={<About />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/signup/advertiser" element={<AdvertiserSignup setUser={setUser} />} />
              <Route path="/signup/localexpert" element={<LocalExpertSignup setUser={setUser} />} />
              <Route path="/signup/traveler" element={<TravelerSignup setUser={setUser} />} />
              <Route path="/login/traveler" element={<TravelerLogin setUser={setUser} />} />
              <Route path="/login/advertiser" element={<AdvertiserLogin setUser={setUser} />} />
              <Route path="/login/localexpert" element={<LocalExpertLogin setUser={setUser} />} />
              <Route path="/verification/pending" element={<Pending />} />
            </>
          ) : (
            <>
              <Route path="/welcome/home" element={<Welcome />} />
              <Route path="/profile/user/:email" element={<MyProfile/>} />
              <Route path="/profile/user/update/:email" element={<UpdateProfile onUpdate={onUpdate} email={email} />} />
              <Route path="/community/posts/all" element={<CommunityDiscussion handleEdit={handleEdit} handleDelete={handleDelete} pencil={pencil} trash={trash}/>} />
              <Route path="/community/post/new" element={<NewPost />} />
              <Route path="/community/post/:postId" element={<ExpandedPost post={post} setPost={setPost} handleEdit={handleEdit} handleDelete={handleDelete} pencil={pencil} trash={trash}/>} />
              <Route path="/community/post/:postId/edit" element={<EditPost />} />
              <Route path="/contact" element={<Contact />} />
            </>
          )}
        </Routes>
      </main>
    </>
  );
}

export default App;

// fix edit and delete post actions
// comment on post actions
// view others' profiles
// useContext functionality
// LOG IN WITH EMAIL ONLY