import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            print("here")
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password and dob
            password = body.get('password')
            #dob = body.get('dob')
            pnum = body.get('pnum')
            role = body.get('role', 'User')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(name=name, uid=uid, password=password, pnum=pnum)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.set_password(password)
            # convert to date type
            #if dob is not None:
                #try:
                 #   uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                #except:
                #    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
            
            if pnum is None:
                try:
                    pnum = "123-456-7890"
                except:
                    return {'message': f'Phone number format error {pnum}, must be 10 digits'}, 400
            
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            user.update(pnum = pnum)
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        @token_required
        def get(self): # Read Method , current_user
            token = request.cookies.get("jwt")
            if not token:
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
            try:
                data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                if data["role"] == "Admin":
                    users = User.query.all()    # read/extract all users from database
                    json_ready = [user.read() for user in users]  # prepare output in json
                    return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
                else: 
                    return {
                    "message": "Not an admin!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
            except Exception as e:
                return {
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e)
                }, 500
        
        

        #def put(self):
            #return ""

        @token_required
        def put(self):
            body = request.get_json() # get the body of the request
            uid = body.get('uid') # get the UID (Know what to reference)
            pnum = body.get('pnum')
            users = User.query.all()
            for user in users:
                if user.uid == uid:
                    user.update(pnum = pnum)
                    return f"Updated {user.uid} phone number to {user.pnum}"
            return f"user not found"
    
        @token_required
        def delete(self):
            ''' Read data from json body '''
            body = request.get_json()
            ''' Avoid garbage in, error checking '''
            # validate uid, name, and password
            uid = body.get('uid')
            password = body.get('password')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            if password is None or len(password) < 2:
                return {'message': f'Password is missing, or is less than 2 characters'}, 400
            ''' Find user '''
            user = User.query.filter_by(_uid=uid).first()
            if user is None:
                return {'message': f'User {uid} not found'}, 400
            ''' Delete user '''
            user.delete()
            return {'message': f'User {uid} deleted'}, 200
    
    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                ''' Get Data '''
                uid = body.get('uid')
                if uid is None:
                    return {'message': f'User ID is missing'}, 400
                password = body.get('password')
                if password is None:
                    return {'message': f'Password is missing'}, 400
                
                ''' Find user '''
                user = User.query.filter_by(_uid=uid).first()
                print(user._uid)
                print(uid)
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 400
                if user:
                    try:
                        print(user._uid)
                        token = jwt.encode(
                            {"_uid": user._uid,"role": user.role},
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        print(token)
                        resp = Response("Authentication for %s successful" % (user._uid))
                        resp.set_cookie('jwt', '', expires=0)
                        resp.set_cookie("jwt", token,
                                max_age=3600,
                                secure=True,
                                #httponly=True,
                                path='/',
                                samesite='None'  # This is the key part for cross-site requests

                                # domain="frontend.com"
                                )
                        print("text")
                        return resp
                    except Exception as e:
                        print(Exception)
                        current_app.logger.error('Error during authentication: %s', e)
                        return {'message': 'Internal server error'}, 500
                return {
                    "message": "Error fetching auth token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 404
            except Exception as e:
                return {
                        "message": "Something went wrong!",
                        "error": str(e),
                        "data": None
                }, 500

            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    