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
from models import Traveler, LocalExpert, Advertiser, Post, Hashtag, Comment

load_dotenv()  
app.secret_key = os.getenv('SECRET_KEY')

bcrypt = Bcrypt()
mail = Mail(app)
Session(app)
CORS(app, supports_credentials=True)

class CurrentUser(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = Traveler.query.get(user_id) or Advertiser.query.get(user_id) or LocalExpert.query.get(user_id)
            if user:
                return {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "role": user.role,
                    "name": user.name,
                    "age": user.age,
                    "gender": user.gender,
                    "bio": user.bio
                }, 201
            return {"Error": "User not logged in"}, 401

class TravelerLogin(Resource):
    def post(self):
        data = request.get_json()

        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not password:
            return {"errors": ["Password is required"]}, 400

        if not username or not email:
            return {"errors": ["Both username and email are required"]}, 400

        traveler = Traveler.query.filter_by(email=email, username=username).first()

        if traveler and traveler.authenticate(password):
            session['user_id'] = traveler.id
            session['username'] = traveler.username
            return {
                'id': traveler.id,
                'email': traveler.email,
                'username': traveler.username,
                "role": traveler.role,
                "name": traveler.name,
                "age": traveler.age,
                "gender": traveler.gender,
                "bio": traveler.bio
            }, 200

        return {'errors': ['Invalid username/email or password']}, 401

class AdvertiserLogin(Resource):
    def post(self):
        data = request.get_json()

        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        errors = []
        if not email:
            errors.append("Email is required.")
        if not username:
            errors.append("Username is required.")
        if not password:
            errors.append("Password is required.")

        if errors:
            return {"errors": errors}, 400

        advertiser = Advertiser.query.filter_by(email=email, username=username).first()

        if not advertiser:
            return {"error": "Invalid email or username."}, 401

        if advertiser.status != 'approved':
            return {"error": "Your account has not been approved yet."}, 403

        if advertiser.authenticate(password):
            session['user_id'] = advertiser.id
            session['username'] = advertiser.username
            return {
                'id': advertiser.id,
                'email': advertiser.email,
                'username': advertiser.username,
                'role': advertiser.role,
                "name": advertiser.name,
                "age": advertiser.age,
                "gender": advertiser.gender,
                "bio": advertiser.bio
            }, 200

        return {'error': 'Invalid password.'}, 401

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
        if not username:
            errors.append("Username is required.")
        if not password:
            errors.append("Password is required.")
        
        if errors:
            return {"errors": errors}, 400

        localexpert = LocalExpert.query.filter_by(email=email, username=username).first()

        if not localexpert:
            return {"Error": "Invalid email or username."}, 401

        if localexpert.status != 'approved':
            return {"Error": "Your account has not been approved yet."}, 403

        if localexpert and localexpert.authenticate(password):
            session['user_id'] = localexpert.id
            session['username'] = localexpert.username
            return {
                'id': localexpert.id,
                'email': localexpert.email,
                'username': localexpert.username,
                "role": localexpert.role,
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

class MyProfile(Resource): #GET my profile, PUT edits for my profile
    def get(self, email):

        user = (
            Traveler.query.filter_by(email=email).first() or
            LocalExpert.query.filter_by(email=email).first() or
            Advertiser.query.filter_by(email=email).first()
        )

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

class TheirProfile(Resource): #GET another user's profile info
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
    def get(self): #GET all of the posts
        try:
            posts = Post.query.order_by(Post.date.desc()).all()

            post_data = []
            for post in posts:
                username = None
                if post.traveler_id:
                    traveler = db.session.get(Traveler, post.traveler_id)
                    username = traveler.username if traveler else None
                    role = traveler.role if traveler else "unknown"
                elif post.localexpert_id:
                    localexpert = db.session.get(LocalExpert, post.localexpert_id)
                    username = localexpert.username if localexpert else None
                    role = localexpert.role if localexpert else "unknown"
                elif post.advertiser_id:
                    advertiser = db.session.get(Advertiser, post.advertiser_id)
                    username = advertiser.username if advertiser else None
                    role = advertiser.role if advertiser else "unknown"

                post_data.append({
                    'id': post.id,
                    'username': username,
                    'role': role,
                    'date': post.date.strftime('%Y-%m-%dT%H:%M:%S'),
                    'subject': post.subject,
                    'body': post.body,
                    'hashtags': [{'id': hashtag.id, 'name': hashtag.name} for hashtag in post.hashtags],
                })
            return {'posts': post_data}, 200

        except Exception as e:
            error_message = str(e)
            error_trace = traceback.format_exc()
            print(f"Error fetching posts: {error_message}")
            print(f"Traceback: {error_trace}")
            return {'error': error_message}, 500

    def post(self): #POSTing a new post
        data = request.get_json()

        try:
            subject = data.get('subject')
            body = data.get('body')
            hashtags = data.get('hashtags', [])
            
            hashtag_objects = []
            for hashtag in hashtags:
                hashtag_obj = Hashtag.query.filter_by(name=hashtag).first()
                if not hashtag_obj:
                    hashtag_obj = Hashtag(name=hashtag)
                    db.session.add(hashtag_obj)
                hashtag_objects.append(hashtag_obj)

            username = data.get('username') 
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
                    subject=subject,
                    body=body,
                    hashtags=hashtag_objects
                )
            elif isinstance(user, LocalExpert):
                post = Post(
                    localexpert_id=user.id,
                    subject=subject,
                    body=body,
                    hashtags=hashtag_objects
                )
            elif isinstance(user, Advertiser):
                post = Post(
                    advertiser_id=user.id,
                    subject=subject,
                    body=body,
                    hashtags=hashtag_objects
                )

            db.session.add(post)
            db.session.commit()

            return {
                'id': post.id,
                'username': username, 
                "date": post.date.strftime('%Y-%m-%dT%H:%M:%S'),
                'subject': post.subject,
                'body': post.body,
                'hashtags': [{'id': hashtag.id, 'name': hashtag.name} for hashtag in post.hashtags]
            }, 201

        except Exception as e:
            error_message = str(e)
            error_trace = traceback.format_exc()
            print(f"Error creating post: {error_message}")
            print(f"Traceback: {error_trace}")
            return {'error': error_message}, 500

class MyPost(Resource):

    @staticmethod
    def process_comments(comments):
        formatted_comments = []
        for comment in comments:
            traveler_id = comment.get('traveler_id')
            localexpert_id = comment.get('localexpert_id')
            advertiser_id = comment.get('advertiser_id')

            if traveler_id:
                traveler = Traveler.query.get(traveler_id)
                author = traveler.username if traveler else "anonymous"
                role = traveler.role if traveler else "unknown"
            elif localexpert_id:
                localexpert = LocalExpert.query.get(localexpert_id)
                author = localexpert.username if localexpert else "anonymous"
                role = localexpert.role if localexpert else "unknown"
            elif advertiser_id:
                advertiser = Advertiser.query.get(advertiser_id)
                author = advertiser.username if advertiser else "anonymous"
                role = advertiser.role if advertiser else "unknown"
            else:
                author = "anonymous"
                role = "unknown"

            formatted_comments.append({
                "id": comment.get("id"),
                "text": comment.get("text", "No text"),
                "author": author,
                "role": role,
                "date": comment.get("date", None)
            })

        return formatted_comments

    def get(self, post_id):  # GET one post INCLUDING the comments
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            return {"error": "Post not found"}, 404

        if post.traveler_id:
            traveler = Traveler.query.get(post.traveler_id)
            author = traveler.username if traveler else "unknown"
            role = traveler.role if traveler else "unknown"
        elif post.localexpert_id:
            localexpert = LocalExpert.query.get(post.localexpert_id)
            author = localexpert.username if localexpert else "unknown"
            role = localexpert.role if localexpert else "unknown"
        elif post.advertiser_id:
            advertiser = Advertiser.query.get(post.advertiser_id)
            author = advertiser.username if advertiser else "unknown"
            role = advertiser.role if advertiser else "unknown"
        else:
            author = "unknown"
            role = "unknown"

        formatted_comments = []
        for comment in post.comments: 
            if comment.traveler_id:
                comment_author = Traveler.query.get(comment.traveler_id).username or "anonymous"
                comment_role = "traveler"
            elif comment.localexpert_id:
                comment_author = LocalExpert.query.get(comment.localexpert_id).username or "anonymous"
                comment_role = "local expert"
            elif comment.advertiser_id:
                comment_author = Advertiser.query.get(comment.advertiser_id).username or "anonymous"
                comment_role = "advertiser"
            else:
                comment_author = "anonymous"
                comment_role = "unknown"

            formatted_comments.append({
                "id": comment.id,
                "text": comment.text,
                "author": comment_author,
                "role": comment_role,
                "date": comment.date.strftime('%Y-%m-%dT%H:%M:%S')
            })
        return {
            "author": author,
            "role": role,
            "subject": post.subject,
            "body": post.body,
            "date": post.date.strftime('%Y-%m-%dT%H:%M:%S'),
            'hashtags': [{'id': hashtag.id, 'name': hashtag.name} for hashtag in post.hashtags],
            "comments": formatted_comments
        }, 200

    def post(self, post_id):  # POSTing a comment to a post
        data = request.get_json()

        text = data.get("text")
        username = data.get("author")

        user = (
            Traveler.query.filter_by(username=username).first() or
            LocalExpert.query.filter_by(username=username).first() or
            Advertiser.query.filter_by(username=username).first()
        )

        if not user:
            return {'error': 'User not found'}, 404

        if isinstance(user, Traveler):
            user_id = user.id
            traveler_id = user.id
            localexpert_id = None
            advertiser_id = None
        elif isinstance(user, LocalExpert):
            user_id = user.id
            traveler_id = None
            localexpert_id = user.id
            advertiser_id = None
        elif isinstance(user, Advertiser):
            user_id = user.id
            traveler_id = None
            localexpert_id = None
            advertiser_id = user.id

        if not text:
            return {"error": "Comment text is required."}, 400
        if not post_id:
            return {"error": "Post ID is required to associate the comment."}, 400

        new_comment = Comment(
            text=text,
            post_id=post_id,
            traveler_id=traveler_id,
            localexpert_id=localexpert_id,
            advertiser_id=advertiser_id,
            date=datetime.utcnow()  
        )

        try:
            db.session.add(new_comment)
            db.session.commit()
            return {"message": "Comment created successfully!"}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": f"Error creating comment: {str(e)}"}, 500

# class EditPost(Resource):
    def put(self, post_id): #PUTting an edit onto a post
        data = request.get_json()
        post = Post.query.filter_by(id=post_id).first()
        
        if not post:
            return {"error": "Post not found"}, 404
        
        subject = data.get('subject')
        body = data.get('body')
        hashtags = data.get('hashtags', [])

        hashtag_objects = []
        for hashtag in hashtags:
            hashtag_obj = Hashtag.query.filter_by(name=hashtag).first()
            if not hashtag_obj:
                hashtag_obj = Hashtag(name=hashtag)
                db.session.add(hashtag_obj)
            hashtag_objects.append(hashtag_obj)

        if not subject or not body:
            return {"error": "Subject and body are required to update the post"}, 400
        
        post.subject = subject
        post.body = body
        post.hashtags = hashtag_objects 

        try:
            db.session.commit()
            return {
                "message": "Post updated successfully",
                "subject": post.subject,
                "body": post.body,
                'hashtags': [hashtag.name for hashtag in post.hashtags], 
            }, 200
        except Exception as e:
            db.session.rollback()
            return {"error": f"Error updating post: {str(e)}"}, 500

    def delete(self, post_id):
        try:
            user_username = session.get('username')

            post = Post.query.filter_by(id=post_id).first()
            if not post:
                return {'error': 'Post not found'}, 404

            user = None
            if post.traveler_id:
                user = Traveler.query.filter_by(id=post.traveler_id).first()
            elif post.localexpert_id:
                user = LocalExpert.query.filter_by(id=post.localexpert_id).first()
            elif post.advertiser_id:
                user = Advertiser.query.filter_by(id=post.advertiser_id).first()

            if not user:
                return {'error': 'User not found'}, 404

            if user_username == user.username:
                db.session.delete(post)
                db.session.commit()
                return '', 204
            else:
                return {'error': 'you are not the author of this post'}, 403

        except Exception as e:
            error_message = str(e)
            print(f"Error deleting post: {error_message}")
            return {'error': error_message}, 500

class MyComment(Resource):
    def delete(self, post_id, comment_id):
        user = session.get('username') 
        if not user:
            return {"error": "User not logged in"}, 401

        post = Post.query.filter_by(id=post_id).first()
        if not post:
            return {"error": "Post not found"}, 404

        comment_to_delete = next((comment for comment in post.comments if comment.id == comment_id), None)

        if not comment_to_delete:
            return {"error": "Comment not found"}, 404

        try:
            db.session.delete(comment_to_delete)
            db.session.commit()

            updated_comments = [{
                "id": comment.id,
                "text": comment.text,
                "date": comment.date.strftime('%Y-%m-%dT%H:%M:%S')
            } for comment in post.comments]

            return {"comments": updated_comments}, 200

        except Exception as e:
            db.session.rollback()
            return {"error": f"Error deleting comment: {str(e)}"}, 500

class HashtagName(Resource):
    def get(self, hashtag_id):
        hashtag = Hashtag.query.get(hashtag_id)

        if not hashtag:
            return {"message": "Hashtag not found"}, 404
        
        return {"name": hashtag.name}

class HashtagFilter(Resource):
    def get(self, hashtag_id):
        hashtag = Hashtag.query.get(hashtag_id)
        
        if not hashtag:
            return {'message': 'Hashtag not found'}, 404
        
        posts_with_hashtag = hashtag.posts
        
        if not posts_with_hashtag:
            return {'message': 'No posts found for this hashtag'}, 404
        
        serialized_posts = []
        
        for post in posts_with_hashtag:
            if post.traveler_id:
                user = Traveler.query.get(post.traveler_id)
            elif post.localexpert_id:
                user = LocalExpert.query.get(post.localexpert_id)
            elif post.advertiser_id:
                user = Advertiser.query.get(post.advertiser_id)
            else:
                user = None

            username = user.username if user else "unknown"
            role = user.role if user else "unknown"
            
            serialized_posts.append({
                'id': post.id,
                'username': username,
                'role': role,
                'subject': post.subject,
                'body': post.body,
                'date': post.date.strftime('%Y-%m-%dT%H:%M:%S'),
                'hashtags': [{'id': hashtag.id, 'name': hashtag.name} for hashtag in post.hashtags],
            })

        return {'posts': serialized_posts}

class Logout(Resource):
    def delete(self):
        session.pop('traveler_id', None)
        session.pop('advertiser_id', None)
        session.pop('localexpert_id', None)
        session.pop('user_id', None)
        return '', 204

class DeleteProfile(Resource):
    def delete(self, email):
        if not email:
            email = session.get('email')

        if not email:
            return {'error': 'Unauthorized request'}, 401

        try:
            user = (
                Traveler.query.filter_by(email=email).first() or
                LocalExpert.query.filter_by(email=email).first() or
                Advertiser.query.filter_by(email=email).first()
            )

            if user:
                db.session.delete(user)
                db.session.commit()
                session.clear()
                session.modified = True
                return '', 204
            else:
                return {"error": "User not found"}, 404

        except Exception as e:
            db.session.rollback()
            print(f"Error deleting user: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}, 500


api.add_resource(CurrentUser, '/current-user')

api.add_resource(TravelerLogin, '/login/traveler')
api.add_resource(AdvertiserLogin, '/login/advertiser')
api.add_resource(LocalExpertLogin, '/login/localexpert')
api.add_resource(TravelerSignup, '/signup/traveler')
api.add_resource(LocalExpertSignup, '/signup/localexpert')
api.add_resource(AdvertiserSignup, '/signup/advertiser')
api.add_resource(VerifyAdvertiser, '/verify/advertiser/<int:advertiser_id>')
api.add_resource(RejectAdvertiser, '/reject/advertiser/<int:advertiser_id>')
api.add_resource(VerifyLocalExpert, '/verify/localexpert/<int:localexpert_id>')
api.add_resource(RejectLocalExpert, '/reject/localexpert/<int:localexpert_id>')

api.add_resource(MyProfile, '/users/<string:email>') #GET my profile, #PUT an update onto the profile
api.add_resource(TheirProfile, '/users/<string:username>') #GET another user's profile
api.add_resource(Community, '/posts') #GET all posts, #POST for making a new post
api.add_resource(MyPost, '/posts/<int:post_id>')  #GET for one post, POST for comments, PUT for editing posts, DELETE for deleting posts

api.add_resource(MyComment, '/posts/<int:post_id>/comments/<int:comment_id>') #DELETE a comment

api.add_resource(HashtagFilter, '/posts/filter/<int:hashtag_id>') #GET the list of posts associated with one hashtag

api.add_resource(HashtagName, '/hashtags/<int:hashtag_id>') #GET a hashtag's name by its ID

api.add_resource(Logout, '/logout')

api.add_resource(DeleteProfile, '/user/delete/<string:email>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)