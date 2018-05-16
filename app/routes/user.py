from flask import request, make_response, jsonify
from . import auth
from .. models import User, BlacklistToken
import re
from flask_bcrypt import Bcrypt

@auth.route('/api/v1/auth/register', methods=['POST'])
def create_user_account():
    """Register a new user"""    

    username1 = request.data.get('username')
    email1 = request.data.get('email')
    password1 = request.data.get('password')
    confirm_password1 = request.data.get('confirm_password')

    
    if username1 and email1 and password1 and confirm_password1:

        username = str(username1.strip(' '))
        email = str(email1.strip(' '))
        password = str(password1.strip(' '))
        confirm_password = str(confirm_password1.strip(' '))
    else:
        return jsonify({'message': "Invalid input, kindly fill in all required input"}), 400

    if username and email and password and confirm_password:

        if len(username) < 3:
            return jsonify({'message': "Invalid input, kindly set a username of more than 3 letters"}), 200
        
        if len(password) < 3:
            return jsonify({'message': "Kindly set a password of more than 3 characters"}), 200
                

        """Checks is all fields have been filled in"""
        users = User.get_all()

        if password != confirm_password:
            return jsonify({'message': "Unmatched passwords"}), 400
        
        elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            """Email Validation"""
            return jsonify({'message': "Invalid email address"}), 400

        else:
            for user in users:
                if user.username == username:
                    return jsonify({'message': "The username is already registered, kindly chose a different one"}), 409

                if user.email == email:
                    return jsonify({'message': "The email is already registered, kindly chose a different one"}), 409
          
        user= User(username=username, email=email, password=password)
        user.save()
        return jsonify({'message': "User Registered successfully"}), 201

    return jsonify({'message': "Input empty fields"}), 400

@auth.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    """Log in a user using username and password provided """ 
    username1 = request.data.get('username')
    password1 = request.data.get('password')

    if username1 and password1:
        username = str(username1.strip(' '))
        password = str(password1.strip(' '))
    else:
        return jsonify({'message': "Invalid input, kindly fill in all required input"}), 400

    if username and password:

        user = User.query.filter_by(username=request.data['username']).first()

        if user and user.password_is_valid(request.data['password']):
    
            """If token is generated, login is successful"""

            access_token = user.generate_token(user.id)
            if access_token:
                
                responce = make_response(
                    jsonify({
                        'message':'Successfully Logged in',
                        'access_token':access_token.decode()
                    }),200)
                return responce
            
        return jsonify({'message': "Wrong username or password entered"}), 404
       
    return jsonify({'message': "Input empty fields"}), 400

@auth.route('/api/v1/auth/logout', methods=['POST'])
def user_logout():
    """Logout the user by blacklisting access token"""

    auth_header = request.headers.get('Authorization')
    if auth_header:
        access_token = auth_header.split(' ')[1]
    else:
        access_token = 'Invalid Token'

    if access_token:

        blacklisttokens = BlacklistToken.get_all()

        for token in blacklisttokens:
            "Check if input access token is blacklisted, if yes, prompt new login"
            if token.token == access_token:
                return jsonify({'status':'Invalid acess token, login to get a new one'}),401

        """Decode token"""
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            
            try:
                token= BlacklistToken(token=access_token)
                token.save()
                return jsonify({'message':'Successfully Logged Out'}),200

            except ValueError:
                return make_response(jsonify({"Message" :"Not Logged out"}), 400)

        else:
            return jsonify({'message': 'Invalid Access Token'}), 401

    return make_response(jsonify({'message': 'Invalid token, Login to obtain a new token'})), 401
     


@auth.route('/api/v1/auth/reset_password', methods=['PUT'])
def reset_password():
    """ Logged in user can reset password """

    email1 = request.data.get('email')
    current_password1 = request.data.get('current_password')
    new_password1 = request.data.get('new_password')
    confirm_password1 = request.data.get('confirm_password')

    auth_header = request.headers.get('Authorization')
    if auth_header:
        access_token = auth_header.split(' ')[1]
    else:
        access_token = 'Invalid Token'  

    if access_token:
        blacklisttokens = BlacklistToken.get_all()

        for token in blacklisttokens:
            "Check if input access token is blacklisted, if yes, prompt new login"
            if token.token == access_token:
                return jsonify({'status':'You are already Logged Out'}),401

        """If accessed, decode token to get userid"""
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
                    
            if email1 and current_password1 and new_password1 and confirm_password1:

                email = str(email1.strip(' '))
                current_password = str(current_password1.strip(' '))
                new_password = str(new_password1.strip(' '))
                confirm_password = str(confirm_password1.strip(' '))
            else:
                return jsonify({'message': "Invalid input, kindly fill in all required input"}), 400 

            if email and current_password and new_password and confirm_password: 
       
                user = User.query.filter_by(email=request.data['email']).first()

                if user and user.password_is_valid(request.data['current_password']):

                    if new_password != confirm_password:
                        return jsonify({'message': "Passwords not matching"}), 400

                    new_hashed_password = Bcrypt().generate_password_hash(new_password).decode('utf-8')
                    user.current_password=new_hashed_password

                    user.save()
                    return jsonify({'message': "Password reset successfully"}), 200


                return jsonify({'error': "Email or password error"}), 404

            return jsonify({'error':'Input Empty Fields'}), 400

        else:
            """last login session is expired/user is not legit, so the payload is an error message"""
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401              
