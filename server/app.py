#!/usr/bin/env python3

from flask import Flask, request, session, jsonify, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from datetime import datetime
from dotenv import load_dotenv
import os
import traceback

from config import app, db, api
from models import Traveler, LocalExpert, Advertiser, Island, Activity, Post

load_dotenv()  
app.secret_key = os.getenv('SECRET_KEY')

bcrypt = Bcrypt()
mail = Mail(app)
CORS(app, supports_credentials=True)

class CurrentUser(Resource):
    def get(self, email):

        user = (
            Traveler.query.filter_by(email=email).first() or
            LocalExpert.query.filter_by(email=email).first() or
            Advertiser.query.filter_by(email=email).first()
        )

        if not user:
            return {"message": "User not logged in"}, 401

        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "bio": user.bio
        }

class TravelerLogin(Resource):
    def post(self):

        session.clear()

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

        session.clear()

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

        session.clear()

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

class CheckSession(Resource):
    def get(self, email):
        user = (
            Traveler.query.filter_by(email=email).first() or
            LocalExpert.query.filter_by(email=email).first() or
            Advertiser.query.filter_by(email=email).first()
        )
        if not user:
            return {'error': 'No user logged in'}, 401

        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "bio": user.bio
        }

class TravelerSignup(Resource):
    def post(self):
        session.clear()

        data = request.get_json()

        print(request.data)

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
            return new_user.to_dict(), 201
 
        except Exception as e:
            return {"error": f"Failed to create user: {str(e)}"}, 422

class LocalExpertSignup(Resource):
    def post(self):
        session.clear()

        data = request.get_json()

        print(request.data)

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
        session.clear()

        data = request.get_json()

        print(request.data)

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
            "bio": user.bio,
            "age": user.age,
            "gender": user.gender,
            "email": user.email,
        }

class Community(Resource):
    def get(self):
        posts = Post.query.all()
        if posts:
            return [post.to_dict() for post in posts], 200
        else:
            return {"error": "No posts found"}, 400

    def post(self):
        data = request.get_json()
    
        try:
            date_str = data.get('date')
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return {"error": "Invalid date format. Expected YYYY-MM-DD."}, 400

            subject = data.get('subject')
            body = data.get('body')
            hashtag = data.get('hashtag')
        
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
                    date=date_obj,
                    subject=subject,
                    body=body,
                    hashtag=hashtag
                )
            elif isinstance(user, LocalExpert):
                post = Post(
                    localexpert_id=user.id,
                    author=username,
                    date=date_obj,
                    subject=subject,
                    body=body,
                    hashtag=hashtag
                )
            elif isinstance(user, Advertiser):
                post = Post(
                    advertiser_id=user.id,
                    author=username,
                    date=date_obj,
                    subject=subject,
                    body=body,
                    hashtag=hashtag
                )

            db.session.add(post)
            db.session.commit()

            return {
                'id': post.id,
                'author': post.author,
                'date': post.date.strftime('%Y-%m-%d'),
                'subject': post.subject,
                'body': post.body,
                'hashtag': post.hashtag
            }, 201
        except Exception as e:
            error_message = str(e)
            error_trace = traceback.format_exc()
            print(f"Error creating post: {error_message}")
            print(f"Traceback: {error_trace}")
            return {'error': error_message}, 500

class MyPost(Resource):
    def get(self, post_id):
        user_id = session.get('user_id')
        if 'user_id' not in session:
            return {'error': 'Unauthorized request'}, 401

        user = (
                Traveler.query.filter_by(id=user_id).first() or
                LocalExpert.query.filter_by(id=user_id).first() or
                Advertiser.query.filter_by(id=user_id).first()
            )

        post = Post.query.filter_by(id=post_id).first()
        print(post)
        if post:
            return {
                "author": post.author,
                'date': post.date.strftime('%Y-%m-%d'),
                "subject": post.subject,
                "body": post.body, 
                "hashtag": post.hashtag
            }, 200
        else:
            return {"error": "Post not found"}, 404

    def put(self, post_id):
        user_id = session.get('user_id')
        if 'user_id' not in session:
            return {'error': 'Unauthorized request'}, 401

        post = Post.query.filter_by(id=post_id).first()

        data = request.get_json()
        author = data.get('author')
        date_str = data.get('date') 
        subject = data.get('subject')
        body = data.get('body')
        hashtag = data.get('hashtag')

        try:
            post.author = author
            if date_str:
                post.date = datetime.strptime(date_str, '%Y-%m-%d').date()
            post.subject = subject
            post.body = body
            post.hashtag = hashtag
            db.session.commit()

            return {
                "author": post.author,
                'date': post.date.strftime('%Y-%m-%d'),
                "subject": post.subject,
                "body": post.body,
                "hashtag": post.hashtag
            }, 200

        except Exception as e:
            db.session.rollback()  
            print(f"Error updating post: {str(e)}")  
            return {"error": f"An error occurred: {str(e)}"}, 500

    def delete(self, post_id):
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
            print(f"User found: {user}")
        else:
            print("User not found")

        if user:
            print(f"User type: {type(user)}")
            post = Post.query.filter_by(id=post_id).first()
            if post:
                print(f"Post found: {post}")
                print(f"Post traveler_id: {post.traveler_id}, localexpert_id: {post.localexpert_id}, advertiser_id: {post.advertiser_id}")
                if isinstance(user, Traveler):
                    print(f"User is a Traveler with id: {user.id}")
                    if post.traveler_id == user.id:
                        db.session.delete(post)
                        db.session.commit()
                        return '', 204
                    else:
                        print("Error: Traveler does not have permission to delete this post")
                        return {'error': 'You are not the author of this post'}, 403
                elif isinstance(user, LocalExpert):
                    print(f"User is a LocalExpert with id: {user.id}")
                    if post.localexpert_id == user.id:
                        db.session.delete(post)
                        db.session.commit()
                        return '', 204
                    else:
                        print("Error: Local Expert does not have permission to delete this post")
                        return {'error': 'You are not the author of this post'}, 403
                elif isinstance(user, Advertiser):
                    print(f"User is an Advertiser with id: {user.id}")
                    if post.advertiser_id == user.id:
                        db.session.delete(post)
                        db.session.commit()
                        return '', 204
                    else:
                        print("Error: Advertiser does not have permission to delete this post")
                        return {'error': 'You are not the author of this post'}, 403
                else:
                    print("Error: User type is not recognized")
                    return {'error': 'You are not the author of this post'}, 403 
            else:
                print(f"Error: Post with ID {post_id} not found in the database")
                return {'error': 'Post not found'}, 404 
        else:
            print("Error: User not found in the database")
            return {'error': 'User not found'}, 404

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

api.add_resource(CheckSession, '/check_session/<string:email>')
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

api.add_resource(MyPost, '/community/post/<int:post_id>', endpoint='post_id')
api.add_resource(MyPost, '/community/post/edit/<int:post_id>', endpoint='post_id_edit')
api.add_resource(MyPost, '/community/post/delete/<int:post_id>', endpoint='post_id_delete')

api.add_resource(Logout, '/logout', endpoint='logout')

api.add_resource(DeleteProfile, '/profile/user/delete/<string:email>)', endpoint='user_profile_delete')

if __name__ == '__main__':
    app.run(port=5555, debug=True)