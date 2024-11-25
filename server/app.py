#!/usr/bin/env python3

from flask import Flask, request, session, jsonify, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from config import app, db, api
from models import Traveler, LocalExpert, Advertiser, Island, Activity

bcrypt = Bcrypt()
CORS(app, supports_credentials=True)

app.secret_key = '12346jkkkkkffff'

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
            session['traveler_id'] = traveler.id
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

        errors = []
        if not email:
            errors.append("Email is required.")
        if not password:
            errors.append("Password is required.")
        
        if errors:
            return {"errors": errors}, 400

        user = Advertiser.query.filter_by(email=email).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return {
                'id': user.id,
                'email': user.email
            }, 200

        return {'Error': 'Invalid email or password'}, 401


class LocalExpertLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        errors = []
        if not email:
            errors.append("Email is required.")
        if not password:
            errors.append("Password is required.")
        
        if errors:
            return {"errors": errors}, 400

        user = LocalExpert.query.filter_by(email=email).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return {
                'id': user.id,
                'email': user.email
            }, 200

        return {'Error': 'Invalid email or password'}, 401


class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
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
        return ''

class AdvertiserSignup(Resource):
    def post(self):
        return ''

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
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

