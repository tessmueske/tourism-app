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
import uuid

from config import app, db, api
from models import Traveler, LocalExpert, Advertiser, Post, Hashtag

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

class MyProfile(Resource):
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

    def get_poster_username_and_role(post):
        if post.traveler:
            return post.traveler.username, post.traveler.role
        elif post.localexpert:
            return post.localexpert.username, post.localexpert.role
        elif post.advertiser:
            return post.advertiser.username, post.advertiser.role
        else:
            return "unknown", "unknown"

    def get(self):
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
                    'hashtags': [hashtag.name for hashtag in post.hashtags]
                })
            print(post_data)
            return {'posts': post_data}, 200

        except Exception as e:
            error_message = str(e)
            error_trace = traceback.format_exc()
            print(f"Error fetching posts: {error_message}")
            print(f"Traceback: {error_trace}")
            return {'error': error_message}, 500

    def post(self):
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
                'hashtags': [hashtag.name for hashtag in post.hashtags]
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

    def get(self, post_id):
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

        comments = post.comments
        if isinstance(comments, str):
            try:
                comments = json.loads(comments)
            except json.JSONDecodeError:
                comments = []

        formatted_comments = []
        for comment in comments:
            comment_author = comment.get('author', 'anonymous')
            comment_role = comment.get('role', 'unknown') 
            if comment_author == 'anonymous' or comment_role == 'unknown':
                comment_author = author
                comment_role = role

            formatted_comments.append({
                "id": comment['id'],
                "text": comment['text'],
                "author": comment_author,
                "role": comment_role,
                "date": comment['date']
            })

        return {
            "author": author,
            "role": role,
            "subject": post.subject,
            "body": post.body,
            'date': post.date.strftime('%Y-%m-%dT%H:%M:%S'),
            "hashtags": [hashtag.name for hashtag in post.hashtags], 
            "comments": formatted_comments
        }, 200

    def put(self, post_id):
        data = request.get_json()

        post = Post.query.filter_by(id=post_id).first()
        if not post:
            return {"error": "Post not found"}, 404

        comment_text = data.get("text")
        comment_role = data.get("role")
        comment_author = data.get("author")

        if not comment_text:
            return {"error": "Missing comment text"}, 400

        comments = json.loads(post.comments) if isinstance(post.comments, str) else post.comments
        if not isinstance(comments, list):
            comments = []

        new_comment = {
            "id": str(uuid.uuid4()),
            "text": comment_text,
            "author": comment_author,
            "role": comment_role,
            "date": datetime.utcnow().isoformat(),
        }

        comments.append(new_comment)
        post.comments = json.dumps(comments)

        try:
            db.session.commit()
            return {"message": "Comment added successfully", "comments": comments}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": f"Error adding comment: {str(e)}"}, 500


class MyComment(Resource):
    def delete(self, post_id, comment_id):
        user = session.get('username') 
        if not user:
            return {"error": "User not logged in"}, 401

        post = Post.query.filter_by(id=post_id).first()
        if not post:
            return {"error": "Post not found"}, 404

        comments = json.loads(post.comments) if isinstance(post.comments, str) else post.comments
        if not isinstance(comments, list):
            return {"error": "Comments data is not valid"}, 500

        comment_to_delete = next((comment for comment in comments if comment["id"] == comment_id), None)

        if not comment_to_delete:
            return {"error": "Comment not found"}, 404

        comments = [comment for comment in comments if comment["id"] != comment_id]
        post.comments = json.dumps(comments)

        try:
            db.session.commit()
            return {"message": "Comment deleted successfully", "comments": comments}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": f"Error deleting comment: {str(e)}"}, 500

class EditPost(Resource):
    def put(self, post_id):
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
                return {'error': 'You are not the author of this post'}, 403

        except Exception as e:
            error_message = str(e)
            print(f"Error deleting post: {error_message}")
            return {'error': error_message}, 500

class HashtagFilter(Resource):
    def get(self, keyword):

        hashtag = Hashtag.query.filter_by(name=keyword).first()
        print(hashtag)
        
        posts = hashtag.posts
        print(posts)

        serialized_posts = []

        for post in posts:
            if post.traveler_id:
                traveler = Traveler.query.get(post.traveler_id)
                username = traveler.username if traveler else "unknown"
                role = traveler.role if traveler else "unknown"
            elif post.localexpert_id:
                localexpert = LocalExpert.query.get(post.localexpert_id)
                username = localexpert.username if localexpert else "unknown"
                role = localexpert.role if localexpert else "unknown"
            elif post.advertiser_id:
                advertiser = Advertiser.query.get(post.advertiser_id)
                author = advertiser.username if advertiser else "unknown"
                role = advertiser.role if advertiser else "unknown"
            else:
                username = "unknown"
                role = "unknown"

            serialized_posts.append({
                'id': post.id,
                'username': username,
                'role': role,
                'subject': post.subject,
                'body': post.body,
                "date": post.date.strftime('%Y-%m-%dT%H:%M:%S')
            })  
            
            print(serialized_posts)
            return {'posts': serialized_posts}, 200
       
        return {'message': 'No posts found for this hashtag'}, 404


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
                print(f"Before clearing session: {session.items()}")
                session.clear()
                session.modified = True
                print(f"After clearing session: {session.items()}")
                return '', 204
            else:
                return {"error": "User not found"}, 404

        except Exception as e:
            db.session.rollback()
            print(f"Error deleting user: {str(e)}")
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

api.add_resource(Community, '/community/posts/all', endpoint='all_posts') #GET all posts
api.add_resource(Community, '/community/post/new', endpoint='new_post') #PUT new post

api.add_resource(MyPost, '/community/post/<int:post_id>', endpoint='post_id')  # GET for one post, PUT for comments
api.add_resource(EditPost, '/community/post/edit/<int:post_id>', endpoint='post_id_edit') #PUT for editing posts
api.add_resource(EditPost, '/community/post/delete/<int:post_id>', endpoint='post_delete') #DELETE for deleting posts

api.add_resource(MyComment, '/posts/<int:post_id>/comments/<comment_id>', endpoint='comment_delete') #Deleting comments

api.add_resource(HashtagFilter, '/community/post/filterby/<string:keyword>', endpoint='filterby_hashtag')

api.add_resource(Logout, '/logout', endpoint='logout')

api.add_resource(DeleteProfile, '/profile/user/delete/<string:email>', endpoint='user_profile_delete')

if __name__ == '__main__':
    app.run(port=5555, debug=True)