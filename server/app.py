#!/usr/bin/env python3

from flask import Flask, request, session, jsonify, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

from config import app, db, api
from models import Traveler, LocalExpert, Advertiser, Island, Activity

load_dotenv()  
app.secret_key = os.getenv('SECRET_KEY')

bcrypt = Bcrypt()
mail = Mail(app)
CORS(app, supports_credentials=True)

class TravelerLogin(Resource):
    def post(self):
        data = request.get_json()
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
            }, 200

        return {'errors': ['Invalid username/email or password']}, 401

class AdvertiserLogin(Resource):
    def post(self):
        data = request.get_json()
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
                'username': advertiser.username
            }, 200

        return {'Error': 'Invalid email, username, or password'}, 401


class LocalExpertLogin(Resource):
    def post(self):
        data = request.get_json()
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
        if email:
            localexpert = LocalExpert.query.filter_by(email=email).first()
        elif username:
            localexpert = LocalExpert.query.filter_by(username=username).first()

        if not localexpert:
            return {"Error": "Invalid email or username."}, 401

        if localexpert.status != 'approved':
            return {"Error": "Your account has not been approved yet."}, 403

        if localexpert and localexpert.authenticate(password):
            session['user_id'] = localexpert.id
            return {
                'id': localexpert.id,
                'email': localexpert.email,
                'username': localexpert.username
            }, 200

        return {'Error': 'Invalid email, username, or password'}, 401

class CheckSession(Resource):
    def get(self):
        user_id = session.get('traveler_id') or session.get('advertiser_id') or session.get('localexpert_id')
        if user_id:
            for model in [Traveler, Advertiser, LocalExpert]:
                user = db.session.get(model, user_id)
                if user:
                    return user.to_dict(), 200
        return {"error": "Unauthorized"}, 401

class TravelerSignup(Resource):
    def post(self):
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
            Traveler.query.get(email=email).first()
            or LocalExpert.query.get(email=email).first()
            or Advertiser.query.get(email=email).first()
        )
        
        if user:
            return {
                "username": user.username,
                "email": user.email
            }, 200
        return {"error": "User not found"} 404

    def patch(self, email):
        data = request.get_json()
        user = (
            Traveler.query.get(email=email).first()
            or LocalExpert.query.get(email=email).first()
            or Advertiser.query.get(email=email).first()
        )
        if not user:
            return {"error": "User not found"}, 404
            

class Logout(Resource):
    def delete(self):
        session.pop('traveler_id', None)
        session.pop('advertiser_id', None)
        session.pop('localexpert_id', None)
        return '', 204

api.add_resource(CheckSession, '/check_session', endpoint='check_session')
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

api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)



