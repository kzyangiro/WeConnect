from flask import request, make_response, jsonify
from . import auth
from .. models import User 
import re
from flask_bcrypt import Bcrypt

@auth.route('/api/v1/auth/register', methods=['POST'])
def create_user_account():
    """Register a new user"""    

    username = str(request.data.get('username').strip(' '))
    email = str(request.data.get('email').strip(' '))
    password = str(request.data.get('password').strip(' '))
    confirm_password = str(request.data.get('confirm_password').strip(' '))

    

    if username and email and password and confirm_password:
        """Checks is all fields have been filled in"""
        users=User.get_all()

        if password != confirm_password:
            response = make_response(jsonify({
                'message': "Unmatched passwords"
                }
            ), 400)
            return response
        
        elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            """Email Validation"""
            response = make_response(jsonify({
                'message': "Invalid email address"
                }
            ), 400)
            return response

        else:
            for user in users:
                if user.username == username:
                    response =make_response(
                    jsonify({
                        'message':'The username is already registered, kindly chose a different one'
                        
                        }), 409)
                    return response

                if user.email == email:
                    response =make_response(
                    jsonify({
                        'message':'The email is already registered, kindly chose a different one'
                        
                        }), 409)
                    return response


                    
        user= User(username=username, email=email, password=password)
        user.save()
        response =make_response(
            jsonify({
                'message':'User Registered successfully'
                
                }), 201)
        return response
    
    response = make_response(jsonify({
            'message': "Input empty fields"
            }
    ), 400)
    return response

@auth.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    """Log in a user using username and password provided """ 
    username = str(request.data.get('username'))
    password = str(request.data.get('password'))
    if username and password:


        user = User.query.filter_by(username=request.data['username']).first()

        if user and user.password_is_valid(request.data['password']):
    
            """If token is generated, login is successful"""

            access_token = user.generate_token(user.id)
            if access_token:
                
                responce = make_response(
                    jsonify({
                        'message':'User Logged in successfully',
                        'access_token':access_token.decode()
                    }),200)
                return responce
            
        responce1 = make_response(
            jsonify({
                'message':'Wrong username or password entered'
            }),404)

        return responce1
            

    responce = make_response(
        jsonify({
            'message':'Input empty fields'
        }),400)

    return responce

@auth.route('/api/v1/auth/logout', methods=['POST'])
def user_logout():
    """Logout the user by revoking access token"""

    if session.get("username") is not None:
        session.pop("username", None)
        return jsonify({"message": "User Logged out successfully"})
    

    responce = make_response(
    jsonify({
        'message':'You are not logged in'
    }),400)

    return responce


@auth.route('/api/v1/auth/reset_password', methods=['PUT'])
def reset_password():
    """ Logged in user can reset password """

    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        """If accessed, decode token to get userid"""
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
                    
            """This endpoint enables a registered user to edit password"""
            username = str(request.data.get('username'))
            password = str(request.data.get('password')) 
            new_password = str(request.data.get('new_password').strip(' ')) 
            confirm_password = str(request.data.get('confirm_password').strip(' ')) 

            if username and password and new_password and confirm_password: 
       
                user = User.query.filter_by(username=request.data['username']).first()

                if user and user.password_is_valid(request.data['password']):

                    if new_password != confirm_password:
                        res = make_response(jsonify({
                                'error':'Passwords not matching'
                            }), 400)
                        return res

                    
                    new_hashed_password = Bcrypt().generate_password_hash(new_password).decode('utf-8')
                    user.password=new_hashed_password


                    user.save()

                    resp= make_response(jsonify({
                                'message':'Password reset successfully'
                            }), 200)
                    return resp

                respon = make_response(jsonify({
                                'error':'Username or password error'
                            }), 404)
                return respon


            response = make_response(jsonify({
                                    'error':'Input Empty Fields'
                                }), 400)
            return response

        else:
            """last login session is expired/user is not legit, so the payload is an error message"""
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401              
