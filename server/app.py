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

class TravelerLogin(Resource):
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

        user = Traveler.query.filter_by(email=email).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return {
                'id': user.id,
                'email': user.email
            }, 200

        return {'Error': 'Invalid email or password'}, 401

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

        Advertiser.query.filter_by(email=email).first()

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

        LocalExpert.query.filter_by(email=email).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return {
                'id': user.id,
                'email': user.email
            }, 200

        return {'Error': 'Invalid email or password'}, 401


class CheckSession(Resource):
    def get(self):
        for key, model in {'traveler_id': Traveler, 'advertiser_id': Advertiser, 'localexpert_id': LocalExpert}.items():
            user_id = session.get(key)
            if user_id:
                user = db.session.get(model, user_id)
                if user:
                    return user.to_dict(), 200
        return {"error": "Unauthorized"}, 401

class TravelerSignup(Resource):
    def post(self):
        data = request.get_json()

        print(request.data)

        email = data.get('email')
        password = data.get('password')

        errors = []

        if not email:
            errors.append("email is required.")
        if not password: 
            errors.append("password is required.")
        if errors:
            return {"errors": errors}, 400 

        user = User.query.filter_by(email=email).first()
        if user:
            return {"errors": ["email already registered. please log in."]}, 400
        
        new_user = User(email=email)
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
api.add_resource(LocalExpert, '/login/localexpert', endpoint='login_localexpert')
api.add_resource(TravelerSignup, '/signup/traveler', endpoint='signup_traveler')
api.add_resource(LocalExpertSignup, '/signup/localexpert', endpoint='signup_localexpert')
api.add_resource(AdvertiserSignup, '/signup/advertiser', endpoint='signup_advertiser')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

