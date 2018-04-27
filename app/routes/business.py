from flask import request, make_response, jsonify, session
from . import bs
from .. models import Business, User, Review

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

    """ Endpoint to register a new business. User has to be logged in"""

    # Obtain token from header
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:

        """decode token to get userid"""
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
            """Invalid Access token, payload error"""
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401

@bs.route('/api/v1/businesses', methods=['GET'])
def get_all_business():
    """Retrieve all businesses"""

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
                "Name":business.business_name,
                "Category":business.category,
                "Business location":business.location

            }
            results.append(obj)

        response=jsonify(results)
        response.status_code = 200
        return response



@bs.route('/api/v1/mybusinesses', methods=['GET'])
def get_my_business():
    """Display all businesses of the loggedin user"""

    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):

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
                        "Business Id":business.businessid,
                        "Business Name":business.business_name,
                        "Category":business.category,
                        "Business location":business.location,
                        "Date created":business.date_created,
                        "Date modified":business.date_modified

                    }
                    results.append(obj)

                response=jsonify(results)
                response.status_code = 200
                return response

        else:
            """Invalid Access token, payload error"""
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401



@bs.route('/api/v1/businesses/<int:businessid>', methods=['GET'])
def get_businesses_by_id(businessid):

    """Retrieve a business of a given id"""
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

    """Obtain token from header"""
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        """If accessed, decode token to get userid"""
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            
            businesses = Business.query.filter_by(created_by=user_id)

            reviews = Review.get_all(businessid)

            for business in businesses:
                if reviews:
                    reviews.delete()
                else:
                    pass

                
                if businessid == business.businessid:
                    
                    business.delete()
                    response=jsonify({"Success":"Business Deleted Successfully"})
                    response.status_code = 200
                    return response

            response=jsonify({"Error":"No Business with that ID"})
            response.status_code = 404
            return response

        else:
            """Invalid Access token, payload error"""
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401


@bs.route('/api/v1/businesses/<int:businessid>', methods=['PUT'])

def update_businesses(businessid):
    """Edit details of the business of the ID indicated in the URL"""

    """Ensure use is logged in, then obtain token from header"""
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        """If accessed, decode token to get userid"""
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
            
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
                            "Description":business.about,
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
            """Invalid Access token payload error"""
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401


@bs.route('/api/v1/businesses/<q>', methods=['GET'])

def search_business_by_name(q):

    """Retrieve a business by the given search name"""
    businesses = Business.query.filter(Business.business_name.contains(q))
    results = []
    not_found_message = "Sorry, No business with that name"

    for business in businesses:

        obj={
        "Business Id":business.businessid,
        "Business Name":business.business_name,
        "Category":business.category,
        "Business location":business.location

        }
        results.append(obj)

    if results == []:
        response=jsonify(not_found_message)
        response.status_code = 404

    else:
        response=jsonify(results)
        response.status_code = 200
    
    return response

@bs.route('/api/v1/business_location/<string:location>', methods=['GET'])

def filter_business_by_location(location):

    """Retrieve a list of busiesses in the given location"""

    businesses = Business.query.filter(Business.location.contains(location))
    results = []
    not_found_message = "Sorry, No business in that location"

    for business in businesses:

        obj={
        "Business Id":business.businessid,
        "Business Name":business.business_name,
        "Category":business.category

        }
        results.append(obj)

    if results == []:
        response=jsonify(not_found_message)
        response.status_code = 404

    else:
        response=jsonify(results)
        response.status_code = 200
    
    return response

@bs.route('/api/v1/business_category/<string:category>', methods=['GET'])

def filter_business_by_category(category):

    """Retrieve a list of busiesses in the given Category"""
    businesses = Business.query.filter(Business.category.contains(category))
    results = []
    not_found_message = "Sorry, No business in that category"

    for business in businesses:

        obj={
        "Business Id":business.businessid,
        "Business Name":business.business_name,
        "Business location":business.location

        }
        results.append(obj)

    if results == []:
        response=jsonify(not_found_message)
        response.status_code = 404

    else:
        response=jsonify(results)
        response.status_code = 200
    
    return response

@bs.route('/api/v1/businesses_by_limit/<int:b_limit>', methods=['GET'])

def filter_business_by_limit(b_limit):

    """Retrieve a list of businesses of just the indicated limit"""
    businesses = Business.get_business_by_limit(b_limit)
    results = []
    not_found_message = "Sorry, No busineses found"

    for business in businesses:

        obj={
        "Business Id":business.businessid,
        "Business Name":business.business_name,
        "Category":business.category,
        "Business location":business.location

        }
        results.append(obj)

    if results == []:
        response=jsonify(not_found_message)
        response.status_code = 404

    else:
        response=jsonify(results)
        response.status_code = 200
    
    return response