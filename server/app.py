#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(username=json['username'])
        user.password_hash=json['password']
        db.session.add(user)
        db.session.commit()
        session['user_id']= user.id
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        user= User.query.filter(User.id == session.get('user_id')).first()
        if not user:
            return make_response({}, 204)
        return make_response(user.to_dict(), 200)

class Login(Resource):
    def post(self):
        params= request.json
        user= User.query.filter(User.username == params['username']).first()
        if not user:
            return make_response({'Login unsuccesful'}, 404)
        password= params['password']
        if not user.authenticate(password):
            return make_response({'Incorrect password'}, 401)
        session['user_id']= user.id
        return make_response(user.to_dict(), 200)

class Logout(Resource):
    def delete(self):
        session['user_id']= None
        return make_response({}, 204)
 

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
