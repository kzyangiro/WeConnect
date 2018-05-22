from flask import request, make_response, jsonify
from . import bs
from .. models import Business, User, Review, BlacklistToken
import re
from sqlalchemy import func # Change variable case

@bs.route('/')
def homepage():
    """This is the home endpoint"""
    responce = make_response(jsonify({'message':'Welcome to Weconnect'}))
                
    return responce

@bs.route('/api/v1/businesses', methods=['POST'])
def register_business():
    """Creates a new business"""

    business_name1 = request.data.get('business_name')
    about1 = request.data.get('about')
    location1 = request.data.get('location')
    category1 = request.data.get('category')

    token = User.validate_token()

    all_input = business_name1 and about1 and location1 and category1

    valid = r"[a-zA-Z0-9]*[a-zA-Z][a-zA-Z0-9]*"


    if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
        return jsonify({'message': 'Invalid token, Login to obtain a new token'}), 401


    if isinstance(business_name1, int) or isinstance(about1, int) or isinstance(location1, int) or isinstance(category1, int):
        return jsonify({'message': "Invalid input, kindly use valid strings"}), 400

    if all_input:

        business_name = str(business_name1.strip(' '))
        location = str(location1.strip(' '))
        category = str(category1.strip(' '))
        about = str(about1.strip(' '))

        all_stripped_input = business_name and about and location and category

        existing = [b for b in Business.get_all() if b.business_name.lower() == business_name.lower()]
    if not all_input:
        response = jsonify({'message': "Invalid input, kindly fill in all required input"}), 400

    elif not all_stripped_input:
        response = jsonify({'Message': "Kindly input the missing fields"}), 400
    
    elif not re.match(valid, business_name) or  not re.match(valid, about) or not re.match(valid, location) or not re.match(valid, category):
        response = jsonify({'message': "Input should not be only digits, kindly use letters as well"}), 400         

    elif len(business_name) < 2 or len(about) < 2 or len(location) < 2 or len(category) < 2:
        response = jsonify({'message': "Kindly use input of at least 2 characters"}), 400

    elif existing:
        response = jsonify({"Error":"Business already exists, use a different business name"}), 409

    else:
        business = Business(business_name=business_name, about=about, location=location, category=category, created_by=token['user_id'])
        business.save()
        response = jsonify({
            "Success":"Business Created successfully",
            "business Id":business.businessid,
            "business Name":business.business_name,
            "business category":business.category,
            "business location":business.location,
            "date created":business.date_created,
            "owner":token['user_id']

        })
        response.status_code = 201
    return response



       
@bs.route('/api/v1/businesses', methods=['GET'])
def get_all_business():

    q = request.args.get('q')
    location = request.args.get('location')
    category = request.args.get('category')
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    
    """Retrieve all businesses"""

    businesses = Business.get_all()
    results = []

    business_by_name = Business.query.filter(func.lower(Business.business_name).contains(func.lower(q)))
    business_by_location = Business.query.filter(func.lower(Business.location).contains(func.lower(location)))
    business_by_category = Business.query.filter(func.lower(Business.category).contains(func.lower(category)))

    if not businesses:
        response = jsonify({'Message': "No Businesses Available"}), 404
    
    elif q:

        b = [b for b in business_by_name]

        if not b:
            response = jsonify({"message":"Sorry, No business with that name"}), 404
        else:
            for b in business_by_name:
            
                """Retrieve a business by the given search name"""

                obj={
                "Business id":b.businessid,
                "Business Name":b.business_name,
                "Category":b.category,
                "Business location":b.location

                }
                results.append(obj)


            response=jsonify(results)
            response.status_code = 200

    elif location:

        b = [b for b in business_by_location]

        if not b:
            response = jsonify({"message":"Sorry, No business in that location"}), 404
        else:
            for b in business_by_location:
            
                """Retrieve a business in a given location """

                obj={
                "Business id":b.businessid,
                "Business Name":b.business_name,
                "Category":b.category,
                "Business location":b.location

                }
                results.append(obj)


            response=jsonify(results)
            response.status_code = 200

    elif category:

        b = [b for b in business_by_category]

        if not b:
            response = jsonify({"message":"Sorry, No business in that category"}), 404
        else:
            for b in business_by_category:
            
                """Retrieve a business in a given location """

                obj={
                "Business id":b.businessid,
                "Business Name":b.business_name,
                "Category":b.category,
                "Business location":b.location

                }
                results.append(obj)


            response=jsonify(results)
            response.status_code = 200

    elif offset and offset.isalpha() or limit and limit.isalpha():
        response = jsonify({"Message" :"Invalid Limit or offset, kindly use an integer"}), 400   

    elif limit and not offset:
        response = jsonify({"Message" :"Indicate the offset"}), 200

    elif offset and not limit:
        response = jsonify({"Message" :"Indicate the limit"}), 200

    elif limit and offset:
        business_limit = Business.businesses_pagination(offset,limit)
        
        b = [b for b in business_limit]

        if not b:
            response = jsonify({"Message" :"Sorry, No business found"}), 404
        else:
            for b in business_limit:
            
                """Retrieve a business in a given location """

                obj={
                "Business id":b.businessid,
                "Business Name":b.business_name,
                "Category":b.category,
                "Business location":b.location

                }
                results.append(obj)


            response=jsonify(results)
            response.status_code = 200


    else:
        for business in businesses:

            obj={
                "Business id":business.businessid,
                "Business Name":business.business_name,
                "Category":business.category,
                "Business location":business.location

            }
            results.append(obj)

            response =jsonify(results)
            response.status_code = 200
        
    return response


@bs.route('/api/v1/mybusinesses', methods=['GET'])
def get_my_business():
    """Display all businesses of the loggedin user"""
    token = User.validate_token()
    businesses = Business.query.filter_by(created_by=token['user_id'])
    results = []

    if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
        response = jsonify({'message': 'Invalid token, Login to obtain a new token'}), 401
        
    elif businesses.count() == 0:
        """ Checking if there is no business"""
        response = make_response(jsonify({'Message': "You have registered no businesses"}), 404)
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


@bs.route('/api/v1/businesses/<businessid>', methods=['GET'])
def get_businesses_by_id(businessid):
    """Retrieve a business of a given id"""

    business = Business.query.filter_by(businessid=businessid)
    
    if not businessid.isdigit():
        response = jsonify({"Message" :"Invalid business Id, kindly use an integer"}), 400

    elif business.count() == 0:
        response=jsonify({"Error":"No Business with that ID"}), 404

    else:
        business = business[0]
        response=jsonify({
                    "Business Id":business.businessid,
                    "Business Name":business.business_name,
                    "Category":business.category,
                    "Business location":business.location,
                    "Description":business.about,
                    "date created":business.date_created,
                    "date modified":business.date_modified,
                    "created_by":business.created_by

            })
        response.status_code = 200
        
    return response

@bs.route('/api/v1/businesses/<businessid>', methods=['DELETE'])
def delete_businesses(businessid):
    """This method deletes a business, but only by the owner while logged in"""
    token = User.validate_token()
    business = Business.query.filter_by(created_by=token['user_id'], businessid=businessid)
    reviews = Review.get_all(businessid)
    
    if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
        response = jsonify({'message': 'Invalid token, Login to obtain a new token'}), 401
    
    elif not businessid.isdigit():
        response = jsonify({"Message" :"Invalid business Id, kindly use an integer"}), 400

    elif business.count() == 0:
        response = jsonify({"Error":"You have no business with that ID"}), 404
    else:
        business[0].delete()
                    
        if reviews:
            reviews.delete()

        response = jsonify({"Success":"Business Deleted Successfully"}), 200
    return response


@bs.route('/api/v1/businesses/<businessid>', methods=['PUT'])

def update_businesses(businessid):
    """This method uses input data to update the content of a business of the ID indicated in the URL"""

    business_name1 = request.data.get('business_name')
    about1 = request.data.get('about')
    location1 = request.data.get('location')
    category1 = request.data.get('category')

    token = User.validate_token()

    all_input = business_name1 and about1 and location1 and category1
    valid = r"[a-zA-Z0-9]*[a-zA-Z][a-zA-Z0-9]*"
    business = Business.query.filter_by(businessid=businessid, created_by=token['user_id'])

    if isinstance(business_name1, int) or isinstance(about1, int) or isinstance(location1, int) or isinstance(category1, int):
        return jsonify({'message': "Invalid input, kindly use valid strings"}), 400

    if all_input:

        business_name = str(business_name1.strip(' '))
        location = str(location1.strip(' '))
        category = str(category1.strip(' '))
        about = str(about1.strip(' '))
        
        all_stripped_input = business_name and about and location and category

        existing = [bus1 for bus1 in Business.get_all() if bus1.business_name.lower() == business_name.lower() and bus1.businessid != int(businessid)]
        
    if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
        response = jsonify({'message': 'Invalid token, Login to obtain a new token'}), 401

    elif not businessid.isdigit():
        response = jsonify({"Message" :"Invalid business Id, kindly use an integer"}), 400

    elif not business:
        response = jsonify({"Error":"You have no business with that ID"}), 404
        
    elif not all_input:
        response = jsonify({'message': "Invalid input, kindly fill in all required input"}), 400

    elif not all_stripped_input:
        response = jsonify({'Message': "Fill in the Empty fields"}), 400
    
    elif not re.match(valid, business_name) or  not re.match(valid, about) or not re.match(valid, location) or not re.match(valid, category):
        response = jsonify({'message': "Input should not be only digits, kindly use letters as well"}), 400         

    elif len(business_name) < 2 or len(about) < 2 or len(location) < 2 or len(category) < 2:
        response = jsonify({'message': "Kindly use input of at least 2 characters"}), 400

    elif existing:
        response = jsonify({"Error":"Business Already Exists, use a different business name"}), 409
        
    else:
        business = business[0]
        
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
            "description":business.about,
            "modified_by":token['user_id']

        })
        response.status_code = 200
    return response

