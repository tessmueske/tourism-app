#!/usr/bin/env python3

from flask import Flask, request, session, jsonify, render_template
from flask_session import Session
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from datetime import datetime, date
from sqlalchemy import cast, Date, extract, or_
from dotenv import load_dotenv
import os
import traceback
import logging
import json

from config import app, db, api
from models import Traveler, LocalExpert, Advertiser, Post, Hashtag

load_dotenv()  
app.secret_key = os.getenv('SECRET_KEY')

bcrypt = Bcrypt()
mail = Mail(app)
Session(app)
CORS(app, supports_credentials=True)

class CurrentUser(Resource):
    def get():
        user = session.get('user')
        if user:
            return {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "name": user.name,
                "age": user.age,
                "gender": user.gender,
                "bio": user.bio
            }
        else:
            return {"User not logged in"}, 401

class TravelerLogin(Resource):
    def post(self):
        data = request.get_json()
        user = None

        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not password:
            return {"errors": ["Password is required"]}, 400

        if not (username or email):
            return {"errors": ["Either username or email is required"]}, 400

        traveler = None
        if email:
            traveler = Traveler.query.filter_by(email=email).first()
        elif username:
            traveler = Traveler.query.filter_by(username=username).first()

        if traveler and traveler.authenticate(password):
            session['user_id'] = traveler.id
            return {
                'id': traveler.id,
                'email': traveler.email,
                'username': traveler.username,
                "name": traveler.name,
                "age": traveler.age,
                "gender": traveler.gender,
                "bio": traveler.bio
            }, 200

        return {'errors': ['Invalid username/email or password']}, 401

class AdvertiserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = None

        email = data.get('email')
        password = data.get('password')
        username = data.get('username')

        errors = []
        if not (email or username):
            errors.append("Email or username is required.")
        if not password:
            errors.append("Password is required.")
        
        if errors:
            return {"errors": errors}, 400

        advertiser = None
        if email:
            advertiser = Advertiser.query.filter_by(email=email).first()
        elif username:
            advertiser = Advertiser.query.filter_by(username=username).first()

        if not advertiser:
            return {"Error": "Invalid email or username."}, 401

        if advertiser.status != 'approved':
            return {"Error": "Your account has not been approved yet."}, 403

        if advertiser and advertiser.authenticate(password):
            session['user_id'] = advertiser.id
            return {
                'id': advertiser.id,
                'email': advertiser.email,
                'username': advertiser.username,
                "name": advertiser.name,
                "age": advertiser.age,
                "gender": advertiser.gender,
                "bio": advertiser.bio
            }, 200

        return {'Error': 'Invalid email, username, or password'}, 401


class LocalExpertLogin(Resource):
    def post(self):
        data = request.get_json()
        user = None

        email = data.get('email')
        password = data.get('password')
        username = data.get('username')

        errors = []
        if not email:
            errors.append("Email is required.")
        if not password:
            errors.append("Password is required.")
        
        if errors:
            return {"errors": errors}, 400

        localexpert = None
        localexpert = LocalExpert.query.filter((LocalExpert.email == email) | (LocalExpert.username == username)).first()

        if not localexpert:
            return {"Error": "Invalid email or username."}, 401

        if localexpert.status != 'approved':
            return {"Error": "Your account has not been approved yet."}, 403

        if localexpert and localexpert.authenticate(password):
            session['user_id'] = localexpert.id
            return {
                'id': localexpert.id,
                'email': localexpert.email,
                'username': localexpert.username,
                "name": localexpert.name,
                "age": localexpert.age,
                "gender": localexpert.gender,
                "bio": localexpert.bio
            }, 200

        return {'Error': 'Invalid email, username, or password'}, 401

class TravelerSignup(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        errors = []

        if not username:
            errors.append("Username is required.")
        if not email:
            errors.append("Email is required.")
        if not password: 
            errors.append("Password is required.")
        if errors:
            return {"errors": errors}, 400 

        user = Traveler.query.filter((Traveler.email == email) | (Traveler.username == username)).first()

        if user:
            return {"errors": ["Email already registered. Please log in."]}, 400
        
        new_user = Traveler(
            email=email,
            username=username,
        )
        new_user.password_hash = password 

        try:
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
            }
 
        except Exception as e:
            return {"error": f"Failed to create user: {str(e)}"}, 422

class LocalExpertSignup(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        notes = data.get('notes')

        errors = []

        if not username:
            errors.append("Username is required.")
        if not email:
            errors.append("Email is required.")
        if not password: 
            errors.append("Password is required.")
        if not notes:
            errors.append("Notes is required.")
        if errors:
            return {"errors": errors}, 400 

        user = LocalExpert.query.filter((LocalExpert.email == email) | (LocalExpert.username == username)).first()

        if user:
            if user.email == email:
                errors.append("Email already registered. Please log in.")
            if user.username == username:
                errors.append("Username already taken.")
            return {"errors": errors}, 400
        
        new_user = LocalExpert(
            email=email,
            username=username,
            notes=notes
        )
        new_user.password_hash = password 

        try:
            db.session.add(new_user)
            db.session.commit()

            admin_email = "tessmueske@gmail.com"  
            msg = Message(
                "New Local Expert Signup Pending Verification",
                sender="verification@magwa.com",
                recipients=[admin_email],
            )
            msg.body = f"A new local expert has signed up:\n\nUsername: {username}\nEmail: {email}\n\n Notes: {notes} \n\n Please review and verify or reject their account by sending a PUT request to /verify/localexpert/<int:localexpert_id> on Postman (or /reject/localexpert/<int:localexpert_id>). You can locate their id in the database in VSC. Then you can send them an email letting them know they've been verified."

            try:
                mail.send(msg)
            except Exception as email_error:
                print(f"Failed to send email: {str(email_error)}")

            return {
                "message": "Signup successful. Your account is pending verification.",
                "user": new_user.to_dict()
            }, 201

        except Exception as e:
            print(f"Database error: {str(e)}")
            return {"error": f"Failed to create user: {str(e)}"}, 422

class AdvertiserSignup(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        notes = data.get('notes')

        errors = []

        if not username:
            errors.append("Username is required.")
        if not email:
            errors.append("Email is required.")
        if not password: 
            errors.append("Password is required.")
        if errors:
            return {"errors": errors}, 400 

        user = Advertiser.query.filter((Advertiser.email == email) | (Advertiser.username == username)).first()

        if user:
            if user.email == email:
                errors.append("Email already registered. Please log in.")
            if user.username == username:
                errors.append("Username already taken.")
            return {"errors": errors}, 400
        
        new_user = Advertiser(
            email=email,
            username=username,
            notes=notes
        )
        new_user.password_hash = password 

        try:
            db.session.add(new_user)
            db.session.commit()

            admin_email = "tessmueske@gmail.com"  
            msg = Message(
                "New Advertiser Signup Pending Verification",
                sender="verification@magwa.com",
                recipients=[admin_email],
            )
            msg.body = f"A new advertiser has signed up:\n\nUsername: {username}\nEmail: {email}\n\nNotes: {notes} \n\n Please review and verify or reject their account by sending a PUT request to /verify/advertiser/<int:advertiser_id> on Postman (or /reject/advertiser/<int:advertiser_id>). Then you can send them an email letting them know they've been verified."

            try:
                mail.send(msg)
            except Exception as email_error:
                print(f"Failed to send email: {str(email_error)}")

            return {
                "user": new_user.to_dict()
            }, 201

        except Exception as e:
            print(f"Database error: {str(e)}")
            return {"error": f"Failed to create user: {str(e)}"}, 422

class VerifyAdvertiser(Resource):
    def put(self, advertiser_id):
        advertiser = Advertiser.query.get(advertiser_id)
        if not advertiser:
            return {"error": "Advertiser not found"}, 404

        advertiser.status = 'approved'

        try:
            db.session.commit()
            return {"message": "Advertiser verified successfully"}, 200
        except Exception as e:
            return {"error": f"Failed to verify advertiser: {str(e)}"}, 422

class RejectAdvertiser(Resource):
    def put(self, advertiser_id):
        advertiser = Advertiser.query.get(advertiser_id)
        if not advertiser:
            return {"error": "Advertiser not found"}, 404

        advertiser.status = 'rejected'

        try:
            db.session.commit()
            return {"message": "Advertiser rejected successfully"}, 200
        except Exception as e:
            return {"error": f"Failed to verify advertiser: {str(e)}"}, 422

class VerifyLocalExpert(Resource):
    def put(self, localexpert_id):
        localexpert = LocalExpert.query.get(localexpert_id)
        if not localexpert:
            return {"error": "Local expert not found"}, 404

        localexpert.status = 'approved'

        try:
            db.session.commit()
            return {"message": "Local expert verified successfully"}, 200
        except Exception as e:
            return {"error": f"Failed to verify local expert: {str(e)}"}, 422

class RejectLocalExpert(Resource):
    def put(self, localexpert_id):
        localexpert = LocalExpert.query.get(localexpert_id)
        if not localexpert:
            return {"error": "Local expert not found"}, 404

        localexpert.status = 'rejected'

        try:
            db.session.commit()
            return {"message": "Local expert rejected successfully"}, 200
        except Exception as e:
            return {"error": f"Failed to verify local expert: {str(e)}"}, 422

class MyProfile(Resource):
    def get(self, email):

        user = (
            Traveler.query.filter_by(email=email).first() or
            LocalExpert.query.filter_by(email=email).first() or
            Advertiser.query.filter_by(email=email).first()
        )

        print(email)

        if not email:
            return {"error": "Email is required"}, 400
        
        if user:
            return {
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "name": user.name,
                "bio": user.bio, 
                "age": user.age, 
                "gender": user.gender 
            }, 200

        return {"error": "User not found"}, 404

    def put(self, email):
        user = (
            Traveler.query.filter_by(email=email).first()
            or LocalExpert.query.filter_by(email=email).first()
            or Advertiser.query.filter_by(email=email).first()
        )

        if not user:
            return {"error": "User not found"}, 404

        data = request.get_json()

        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        bio = data.get('bio')

        try:
            user.name = name
            user.age = age
            user.gender = gender
            user.bio = bio
            db.session.commit()

            return {
                "name": user.name,
                "age": user.age,
                "gender": user.gender,
                "bio": user.bio,
            }, 200
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500

class TheirProfile(Resource):
    def get(self, username):
        user = (
            Traveler.query.filter_by(username=username).first() or
            LocalExpert.query.filter_by(username=username).first() or
            Advertiser.query.filter_by(username=username).first()
        )
        if not user:
            return {"error": "User not found"}, 404

        return {
            "name": user.name,
            "role": user.role,
            "bio": user.bio,
            "age": user.age,
            "gender": user.gender,
            "email": user.email,
        }

class Community(Resource):
    def get(self):
        try:
            posts = Post.query.filter(or_(Post.date != None, Post.date == None)).order_by(Post.date.desc()).all()

            formatted_posts = []
            for post in posts:
                if post.traveler_id:
                    traveler = Traveler.query.get(post.traveler_id)
                    author = traveler.username
                    role = traveler.role
                elif post.localexpert_id:
                    localexpert = LocalExpert.query.get(post.localexpert_id)
                    author = localexpert.username
                    role = localexpert.role
                elif post.advertiser_id:
                    advertiser = Advertiser.query.get(post.advertiser_id)
                    author = advertiser.username
                    role = advertiser.role
                else:
                    author = "Unknown"
                    role = "Unknown"

                formatted_posts.append({
                    'id': post.id,
                    'author': author, 
                    'role': role,
                    'date': post.date.strftime('%Y-%m-%dT%H:%M:%S') if post.date else None,
                    'subject': post.subject,
                    'body': post.body,
                    'hashtags': [hashtag.name for hashtag in post.hashtags]
                })

            return formatted_posts, 200

        except Exception as e:
            print(f"Error: {str(e)}")
            return {"error": "An error occurred while fetching posts"}, 500

    def post(self):
        data = request.get_json()

        try:
            subject = data.get('subject')
            body = data.get('body')
            hashtags = data.get('hashtags', [])
            comments = data.get('comments', [])

            hashtag_objects = []
            for hashtag in hashtags:
                hashtag_obj = Hashtag.query.filter_by(name=hashtag).first()
                if not hashtag_obj:
                    hashtag_obj = Hashtag(name=hashtag)
                    db.session.add(hashtag_obj)
                hashtag_objects.append(hashtag_obj)

            username = data.get('author')
            user = (
                Traveler.query.filter_by(username=username).first() or
                LocalExpert.query.filter_by(username=username).first() or
                Advertiser.query.filter_by(username=username).first()
            )

            if not user:
                return {'error': 'User not found'}, 404

            if isinstance(user, Traveler):
                post = Post(
                    traveler_id=user.id,
                    author=username,
                    subject=subject,
                    body=body,
                    hashtags=hashtag_objects
                )
            elif isinstance(user, LocalExpert):
                post = Post(
                    localexpert_id=user.id,
                    author=username,
                    subject=subject,
                    body=body,
                    hashtags=hashtag_objects
                )
            elif isinstance(user, Advertiser):
                post = Post(
                    advertiser_id=user.id,
                    author=username,
                    subject=subject,
                    body=body,
                    hashtags=hashtag_objects
                )

            if comments:
                for comment_data in comments:
                    comment = {
                        'author': comment_data.get('author'),
                        'text': comment_data.get('text'),
                        'date': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
                    }
                    post.comments.append(comment)

            db.session.add(post)
            db.session.commit()

            return {
                'id': post.id,
                'author': post.author,
                "date": post.date.strftime('%Y-%m-%dT%H:%M:%S'),
                'subject': post.subject,
                'body': post.body,
                'hashtags': [hashtag.name for hashtag in post.hashtags],
                'comments': [comment.text for comment in post.comments]
            }, 201

        except Exception as e:
            error_message = str(e)
            error_trace = traceback.format_exc()
            print(f"Error creating post: {error_message}")
            print(f"Traceback: {error_trace}")
            return {'error': error_message}, 500

class MyPost(Resource):
    #GET post info including comments
    def get(self, post_id):
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            return {"error": "Post not found"}, 404

        comments = json.loads(post.comments) if isinstance(post.comments, str) else post.comments

        return {
            "author": post.author,
            "subject": post.subject,
            "body": post.body,
            "comments": comments
        }, 200

    def put(self, post_id):
        #PUT comment onto a post
        data = request.get_json()
        print(f"Request data: {data}")

        post = Post.query.filter_by(id=post_id).first()
        if not post:
            print(f"Post with ID {post_id} not found.")
            return {"error": "Post not found"}, 404
        
        comment_text = data.get("text")
        comment_author = data.get("author")
        print(f"Extracted comment text: {comment_text}, author: {comment_author}")
        
        if not comment_text or not comment_author:
            print("Missing comment text or author.")
            return {"error": "Missing comment text or author"}, 400
        
        new_comment = {
            "text": comment_text,
            "author": comment_author,
            "timestamp": datetime.utcnow().isoformat()
        }
        print(f"Adding new comment: {new_comment}")

        post.comments.append(new_comment)
        print(f"Post after adding comment: {post.comments}")

        post.comments = json.dumps(post.comments)

        print(f"Type of comments before commit: {type(post.comments)}")
        
        try:
            db.session.commit()
            print("Comment added and database commit successful.")
            return {"message": "Comment added successfully", "comments": post.comments}, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error adding comment: {str(e)}")
            return {"error": f"Error adding comment: {str(e)}"}, 500

class EditPost(Resource):
    def put(self, post_id):
        # This route handles editing a post (e.g., subject, body, hashtags)
        data = request.get_json()
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            return {"error": "Post not found"}, 404
        
        subject = data.get('subject')
        body = data.get('body')
        hashtags = data.get('hashtag')

        if not subject or not body:
            return {"error": "Subject and body are required to update the post"}, 400
        
        post.subject = subject
        post.body = body
        post.hashtag = hashtags 

        try:
            db.session.commit()
            return {
                "message": "Post updated successfully",
                "subject": post.subject,
                "body": post.body,
                "hashtag": post.hashtag
            }, 200
        except Exception as e:
            db.session.rollback()
            return {"error": f"Error updating post: {str(e)}"}, 500

    # def get(self, post_id):
    #     try:
    #         post = Post.query.filter_by(id=post_id).first()
    #         if not post:
    #             return {"error": "Post not found"}, 404

    #         author = None
    #         role = None
    #         if post.traveler_id:
    #             author = Traveler.query.get(post.traveler_id)
    #             role = "traveler"
    #         elif post.localexpert_id:
    #             author = LocalExpert.query.get(post.localexpert_id)
    #             role = "local expert"
    #         elif post.advertiser_id:
    #             author = Advertiser.query.get(post.advertiser_id)
    #             role = "advertiser"

    #         if not author:
    #             return {"error": "Author not found"}, 404
    #         return {
    #             "author": author.username if author else None, 
    #             "role": role,
    #             "date": post.date.strftime('%Y-%m-%dT%H:%M:%S') if post.date else None,
    #             "subject": post.subject,
    #             "body": post.body,
    #             "hashtags": [hashtag.to_dict() for hashtag in post.hashtags],
    #             'comments': [comment.to_dict() for comment in post.comments] if post.comments else []
    #         }, 200

        # except Exception as e:
        #     db.session.rollback()  
        #     print(f"Error updating post: {str(e)}")  
        #     return {"error": f"An error occurred: {str(e)}"}, 500

    def delete(self, post_id):
        try:
            post = Post.query.filter_by(id=post_id).first()
            if not post:
                return {'error': 'Post not found'}, 404

            print(f"Post found: {post}")
            print(f"Post author: {post.author}")

            user = (
                Traveler.query.filter_by(username=post.author).first() or
                LocalExpert.query.filter_by(username=post.author).first() or
                Advertiser.query.filter_by(username=post.author).first()
            )
            if not user:
                return {'error': 'Author of the post not found'}, 404

            print(f"User found: {user}, Type: {type(user)}")

            user_type_to_id = {
                Traveler: post.traveler_id,
                LocalExpert: post.localexpert_id,
                Advertiser: post.advertiser_id,
            }

            for user_type, post_owner_id in user_type_to_id.items():
                if isinstance(user, user_type) and post_owner_id == user.id:
                    db.session.delete(post)
                    db.session.commit()
                    return '', 204

            return {'error': 'You are not the author of this post'}, 403

        except Exception as e:
            error_message = str(e)
            print(f"Error deleting post: {error_message}")
            return {'error': error_message}, 500    

class Logout(Resource):
    def delete(self):
        session.pop('traveler_id', None)
        session.pop('advertiser_id', None)
        session.pop('localexpert_id', None)
        session.pop('user_id', None)
        return '', 204

class DeleteProfile(Resource):
    def delete(self, user_id):
        user_id = session.get('user_id')
        print(f"User ID from session: {user_id}")

        if not user_id:
            print("Error: User ID not found in session")
            return {'error': 'Unauthorized request'}, 401

        user = (
            Traveler.query.filter_by(id=user_id).first() or
            LocalExpert.query.filter_by(id=user_id).first() or
            Advertiser.query.filter_by(id=user_id).first()
        )
        if user:
            db.session.delete(user)
            db.session.commit()
            return '', 204
        else: 
            db.session.rollback()  
            print(f"Error updating post: {str(e)}")  
            return {"error": f"An error occurred: {str(e)}"}, 500

api.add_resource(CurrentUser, '/current-user/<string:email>', endpoint='current_user')

api.add_resource(TravelerLogin, '/login/traveler', endpoint='login_traveler')
api.add_resource(AdvertiserLogin, '/login/advertiser', endpoint='login_advertiser')
api.add_resource(LocalExpertLogin, '/login/localexpert', endpoint='login_localexpert')
api.add_resource(TravelerSignup, '/signup/traveler', endpoint='signup_traveler')
api.add_resource(LocalExpertSignup, '/signup/localexpert', endpoint='signup_localexpert')
api.add_resource(AdvertiserSignup, '/signup/advertiser', endpoint='signup_advertiser')
api.add_resource(VerifyAdvertiser, '/verify/advertiser/<int:advertiser_id>', endpoint='verify_advertiser')
api.add_resource(RejectAdvertiser, '/reject/advertiser/<int:advertiser_id>', endpoint='reject_advertiser')
api.add_resource(VerifyLocalExpert, '/verify/localexpert/<int:localexpert_id>', endpoint='verify_localexpert')
api.add_resource(RejectLocalExpert, '/reject/localexpert/<int:localexpert_id>', endpoint='reject_localexpert')

api.add_resource(MyProfile, '/profile/user/<string:email>', endpoint='user_profile')
api.add_resource(MyProfile, '/profile/user/update/<string:email>')

api.add_resource(TheirProfile, '/profile/user/author/<string:username>')

api.add_resource(Community, '/community/posts/all', endpoint='all_posts')
api.add_resource(Community, '/community/post/new', endpoint='new_post')

api.add_resource(MyPost, '/community/post/<int:post_id>', endpoint='post_id')  # GET for posts, PUT for comments
api.add_resource(EditPost, '/community/post/edit/<int:post_id>', endpoint='post_id_edit') #PUT for editing posts
api.add_resource(MyPost, '/community/post/delete/<int:post_id>', endpoint='post_id_delete')

api.add_resource(Logout, '/logout', endpoint='logout')

api.add_resource(DeleteProfile, '/profile/user/delete/<string:email>', endpoint='user_profile_delete')

if __name__ == '__main__':
    app.run(port=5555, debug=True)