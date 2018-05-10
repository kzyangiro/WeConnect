from flask import request, make_response, jsonify, session
from . import bs
from .. models import User, BlacklistToken
import re


@bs.route('/api/v1/auth/register', methods=['POST'])
def create_user_account():
    """Register a new user"""

    username = str(request.data.get('username').strip(' '))
    email = str(request.data.get('email').strip(' '))
    password = str(request.data.get('password').strip(' '))
    confirm_password = str(request.data.get('confirm_password').strip(' '))

    if username and email and password and confirm_password:
        """Checks is all fields have been filled in"""
        
        if password != confirm_password:
            return jsonify({'message': "Unmatched passwords"}), 400
        
        elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            """Email Validation"""
            return jsonify({'message': "Invalid email address"}), 400

        else:
            for user in User.USERS:
                if user.username == username:
                    return jsonify({'message':'The username already exists'}), 409

                if user.email == email:
                    return jsonify({'message':'The email address already exists'}), 409

                    
        user= User(username=username, email=email, password=password)
        user.save(user)
        return jsonify({'message':'User Created successfully'}), 201
    
    return jsonify({'message': "Input empty fields"}), 400
    

@bs.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    """log in a user using username and password provided """ 
    username = str(request.data.get('username'))
    password = str(request.data.get('password'))
    
    if username and password:

        log_user = [myuser for myuser in User.USERS if username==myuser.username]
        if log_user:
            log_user = log_user[0] #If not, will only pick first variable
            if password==log_user.password:
                """Generate access token"""

                access_token = log_user.generate_token(log_user.userid)

                if access_token:

                    responce = make_response(
                        jsonify({
                            'message':'User Logged in successfully',
                            'access_token':access_token
                        }),200)
                    return responce 
                

            return jsonify({'message':'Wrong password entered'}),400

        return jsonify({'message':'User not found, kindly register first'}),404
    
    return jsonify({'message':'Fill in the empty fields'}),400


@bs.route('/api/v1/auth/logout', methods=['POST'])
def user_logout():

    """logout the user by blacklisting the acess_token"""
    auth_header = request.headers.get('Authorization')
    if auth_header:
        access_token = auth_header.split(' ')[1]
    else:
        access_token = 'Invalid Token'

    if access_token:

        for token in BlacklistToken.blacklist_tokens:
            "Check if input access token is blacklisted, if yes, prompt new login"
            if token == access_token:
                return jsonify({'status':'You are already Logged Out'}),401
          
        """Decode token"""
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            
            try:
                BlacklistToken.blacklist_tokens.append(access_token)
                return jsonify({'message':'Successfully Logged Out'}),200

            except Exception as e:
                return jsonify({'message': e}), 401
        else:
            return jsonify({'message': 'Invalid Access Token'}), 401


@bs.route('/api/v1/auth/reset_password', methods=['PUT'])
def reset_password():
    """A registered user to edit password"""
            
    email = str(request.data.get('email'))
    current_password = str(request.data.get('current_password')) 
    new_password = str(request.data.get('new_password').strip(' ')) 
    confirm_password = str(request.data.get('confirm_password').strip(' '))

    auth_header = request.headers.get('Authorization')
    if auth_header:
        access_token = auth_header.split(' ')[1]
    else:
        access_token = 'Invalid Token'    
    
    if access_token:

        for token in BlacklistToken.blacklist_tokens:
            if token == access_token:
                return jsonify({'status':'You are Logged Out, kindly login first'}),400

        """Decode Token"""
        
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):

            if email and current_password and new_password and confirm_password: 

                user = [myuser for myuser in User.USERS if myuser.email == email]
                if user:
                    user = user[0]
                    if user.password == current_password:
                    
                        if new_password != confirm_password:
                            return jsonify({'message':'Passords not matching'}), 400

                        user.password=new_password
                        return jsonify({'message':'Password reset successfully'}), 200

                    return jsonify({'message':'Wrong Password'}), 401

                return jsonify({'message':'User not found, invalid email'}), 404

            return jsonify({'message':'Input Empty Fields'}), 400

        """Invalid Token"""
        return jsonify({'message': user_id}), 401       
