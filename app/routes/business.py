from flask import request, make_response, jsonify, session
from . import bs
from .. models import Business, User

@bs.route('/', methods=['POST', 'GET'])
def homepage():
    """This is the home endpoint"""
    res = make_response(
        jsonify({
        'message':'Welcome to Weconnect'
        
        }))
                
    return res
@bs.route('/api/v1/businesses', methods=['POST'])
def register_business():

        # Obtain token from header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(' ')[1]

        if access_token:
            """If accessed, decode token to get userid"""
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # If it returns a string then its an error, otherwise, token decoded, we can proceed

                business_name = str(request.data.get('business_name').strip(' '))
                about = str(request.data.get('about').strip(' '))
                location = str(request.data.get('location').strip(' '))
                category = str(request.data.get('category').strip(' '))
                
                if business_name and about and location and category:
                    businesses = Business.get_all()
                    for business in businesses:
                        if business.business_name == business_name:
                            res = jsonify({
                                "Error":"Business already exists, use a different business name"
                            })
                            res.status_code = 409
                            return res

                    business = Business(business_name=business_name, about=about, location=location, category=category, created_by=user_id)
                    business.save()
                    response = jsonify({
                        "Success":"Business Created successfully",
                        "business Id":business.businessid,
                        "business Name":business.business_name,
                        "business category":business.category,
                        "business location":business.location,
                        "date created":business.date_created,
                        "owner":user_id

                    })
                    response.status_code = 201
                    return response

                response = make_response(jsonify({
                        'Message': "Kindly input the missing fields"
                        }
                    ), 400)
                return response

            else:
                # payload error
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401
@bs.route('/api/v1/businesses', methods=['GET'])
def get_all_business():
    """retrieve all businesses """

    businesses = Business.get_all()
    results = []

    if len(businesses) == 0:
        """ Checking if there is no business"""
        response = make_response(jsonify({
            'Message': "No Businesses Available"
            }
        ), 404)
        return response
        
    else:
        for business in businesses:
            obj={
                "Business id":business.businessid,
                "Name":business.business_name

            }
            results.append(obj)

        response=jsonify(results)
        response.status_code = 200
        return response





@bs.route('/api/v1/mybusinesses', methods=['GET'])
def get_my_business():
    """Display all businesses of the loggedin user """

    # Obtain token from header
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        """If accessed, decode token to get userid"""
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
            # If it returns a string then its an error, otherwise, token decoded, we can proceed


            """retrieve all for the specific logged in id """
            businesses = Business.query.filter_by(created_by=user_id)
            results = []

            if businesses.count() == 0:
                """ Checking if there is no business"""
                response = make_response(jsonify({
                    'Message': "You have registered no businesses"
                    }
                ), 404)
                return response
                
            else:
                for business in businesses:
                    obj={
                        "Business id":business.businessid,
                        "Name":business.business_name

                    }
                    results.append(obj)

                response=jsonify(results)
                response.status_code = 200
                return response

        else:
            # payload error
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401



@bs.route('/api/v1/businesses/<int:businessid>', methods=['GET'])
def get_businesses_by_id(businessid):

    """This endpoint retrieves a business by the given id"""
    businesses = Business.get_all()

    for business in businesses:
        if businessid == business.businessid:
            obj={
                "Business Id":business.businessid,
                "Business Name":business.business_name,
                "Category":business.category,
                "Business location":business.location,
                "Description":business.about,
                "date created":business.date_created,
                "date modified":business.date_modified,
                "created_by":business.created_by

            }
            response=jsonify(obj)
            response.status_code = 200
            return response

    response=jsonify({"Error":"No Business with that ID"})
    response.status_code = 404
    return response


@bs.route('/api/v1/businesses/<int:businessid>', methods=['DELETE'])
def delete_businesses(businessid):
    """This endpoint deletes a business, but only by the owner while logged in"""

    #Obtain token from header
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        """If accessed, decode token to get userid"""
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
            # If it returns a string then its an error, otherwise, token decoded, we can proceed
            businesses = Business.query.filter_by(created_by=user_id)

            for business in businesses:
                if businessid == business.businessid:
                    business.delete()
                    response=jsonify({"Success":"Business Deleted Successfully"})
                    response.status_code = 200
                    return response

            response=jsonify({"Error":"No Business with that ID"})
            response.status_code = 404
            return response

        else:
            # last login session is expired/user is not legit, payload error
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401


@bs.route('/api/v1/businesses/<int:businessid>', methods=['PUT'])

def update_businesses(businessid):
    """This endpoint uses input data to update the content of a business of the ID indicated in the URL"""

    # Ensure use is logged in, then obtain token from header
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        """If accessed, decode token to get userid"""
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
            # If it returns a string then its an error, otherwise, token decoded, we can proceed

            business_name = str(request.data.get('business_name').strip(' '))
            about = str(request.data.get('about').strip(' '))
            location = str(request.data.get('location').strip(' '))
            category = str(request.data.get('category').strip(' '))
            
            if business_name and about and location and category:
                businesses = Business.query.filter_by(created_by=user_id)
                for business in businesses:
                    if business.business_name == business_name and business.businessid != businessid:
                        res = jsonify({
                            "Error":"Business Already Exists, use a different business name"
                        })
                        res.status_code = 409
                        return res

                    else:
                        business.business_name=business_name
                        business.about=about
                        business.location=location
                        business.category=category

                        business.save()
                        response = jsonify({
                            "Success":"Business updated successfully",
                            "business Name":business.business_name,
                            "category":business.category,
                            "location":business.location,
                            "created_by":user_id

                        })
                        response.status_code = 200
                        return response

                response = make_response(jsonify({
                        'Message': "No Business with that ID"
                        }
                    ), 404)
                return response
            
            response = make_response(jsonify({
                    'Message': "Fill in the Empty fields"
                    }
                ), 400)
            return response

        else:
            # payload error
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401
