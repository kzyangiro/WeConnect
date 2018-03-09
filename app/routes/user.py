from flask import request, make_response, jsonify
from . import bs
from .. models import User
import re
@bs.route('/api/v1/auth/register', methods=['POST'])
def create_user_account():
    # import pdb; pdb.set_trace()

    username = str(request.data.get('username').strip(' '))
    email = str(request.data.get('email').strip(' '))
    password = str(request.data.get('password').strip(' '))
    confirm_password = str(request.data.get('confirm_password').strip(' '))

    

    if username and email and password and confirm_password:
        
        if password != confirm_password:
            response = make_response(jsonify({
                'message': "Unmatched passwords"
                }
            ), 403)
            return response
        
        elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            response = make_response(jsonify({
                'message': "Invalid email address"
                }
            ), 403)
            return response

        else:
            for user in User.user:
                if user.username == username:
                    response =make_response(
                    jsonify({
                        'message':'The username already exists'
                        
                        }), 409)
                    return response

                if user.email == email:
                    response =make_response(
                    jsonify({
                        'message':'The email address already exists'
                        
                        }), 409)
                    return response

                    
        user= User(username=username, email=email, password=password)
        user.save(user)
        response =make_response(
            jsonify({
                'message':'User Created successfully'
                
                }), 201)
        return response
    
    response = make_response(jsonify({
            'message': "Input empty fields"
            }
    ), 403)
    return response

@bs.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    username = str(request.data.get('username'))
    password = str(request.data.get('password'))
    responce = ''
    if username and password:
        if [username==users.username and password==users.password for users in User.user]:
            responce = make_response(
                jsonify({
                    'message':'User Logged in successfully'
                }),200)
            return responce
            

        else:
            responce = make_response(
                jsonify({
                    'message':'Wrong username or password entered'
                }),404)

            return responce
    else:
        responce = make_response(
            jsonify({
                'message':'Empty username or password field'
            }),403)

        return responce

@bs.route('/api/v1/auth/logout', methods=['POST'])
def user_logout():
    pass
    

  
