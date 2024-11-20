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

class Login(Resource):
    def post(self):
        return ''

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
        return ''

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
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(TravelerSignup, '/signup/traveler', endpoint='signup_traveler')
api.add_resource(LocalExpertSignup, '/signup/localexpert', endpoint='signup_localexpert')
api.add_resource(AdvertiserSignup, '/signup/advertiser', endpoint='signup_advertiser')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

