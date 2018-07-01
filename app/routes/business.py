from flask import request, make_response, jsonify
from . import bs
from .. models import Business, User, Review, Tokens
import re
from sqlalchemy import func 

@bs.route('/')
def homepage():
    """Home endpoint"""
          
    return jsonify({'message':'Welcome to Weconnect'})

@bs.route('/api/v1/businesses', methods=['POST'])
def register_business():
    """Create a new business"""

    business_name1 = request.data.get('business_name')
    about1 = request.data.get('about')
    location1 = request.data.get('location')
    category1 = request.data.get('category')

    token = User.validate_token()

    all_input = business_name1 and about1 and location1 and category1
    int_input = isinstance(business_name1, int) or isinstance(about1, int) or isinstance(location1, int) or isinstance(category1, int)

    valid = r"[a-zA-Z0-9]*[a-zA-Z][a-zA-Z0-9]*"

    if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
        return jsonify({'Error': 'Invalid token, Login to obtain a new token'}), 401

    if int_input or not all_input:
        return jsonify({'Error': "Invalid input, fill in all required input and kindly use valid strings"}), 400

    business_name = str(business_name1.strip(' '))
    location = str(location1.strip(' '))
    category = str(category1.strip(' '))
    about = str(about1.strip(' '))

    all_stripped_input = business_name and about and location and category

    if not all_stripped_input:
        response = jsonify({'Error': "Kindly input the missing fields"}), 400
    
    elif not re.match(valid, business_name) or  not re.match(valid, about) or not re.match(valid, location) or not re.match(valid, category):
        response = jsonify({'Error': "Input should not be only digits, kindly use letters as well"}), 400         

    elif len(business_name) < 3 or len(about) < 3 or len(location) < 3 or len(category) < 3:
        response = jsonify({'Error': "Kindly use input of at least 3 characters"}), 400

    elif [b for b in Business.get_all() if b.business_name.lower() == business_name.lower()]:
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
    """Retrieve all businesses. Filter businesses by name, location, category and pagination"""

    q = request.args.get('q')
    location = request.args.get('location')
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    businesses = Business.get_all()

    if not businesses:
        response = jsonify({'message': "No Businesses Available"}), 404
    
    elif q:
        """Search business by name"""

        business_by_name = Business.query.filter(func.lower(Business.business_name).contains(func.lower(q)))
        b = [b for b in business_by_name]
        if not b:
            response = jsonify({"message":"Sorry, No business with that name"), 404
        else:
            response = jsonify([business.serialize for business in business_by_name]), 200

    elif location:
        """Retrieve businesses in a given location """

        business_by_location = Business.query.filter(func.lower(Business.location).contains(func.lower(location)))
        b = [b for b in business_by_location]
        if not b:
            response = jsonify({"message":"Sorry, No business in that location"}), 404
        else:
            response = jsonify([business.serialize for business in business_by_location]), 200


    elif category:
        """Retrieve businesses in a given category """

        business_by_category = Business.query.filter(func.lower(Business.category).contains(func.lower(category)))
        b = [b for b in business_by_category]
        if not b:
            response = jsonify({"message":"Sorry, No business in that category"}), 404
        else:
            response = jsonify([business.serialize for business in business_by_category]), 200

    elif limit and page:
        """ Retrieve businesses of the indicated page with the indicated limit"""
        
        business_limit = Business.query.paginate(int(page), int(limit), False)
        b = [b for b in business_limit.items]
        if not b:
            response = jsonify({"message" :"Sorry, No business found"}), 404
        else:
            response = jsonify([business.serialize for business in business_limit.items]), 200

    else:
        response = jsonify([business.serialize for business in businesses]), 200
        
    return response


@bs.route('/api/v1/mybusinesses', methods=['GET'])
def get_my_business():
    """Display all businesses of the loggedin user"""
    token = User.validate_token()
    
    if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
        return jsonify({'Error': 'Invalid token, Login to obtain a new token'}), 401

    businesses = Business.query.filter_by(created_by=token['user_id'])

    if businesses.count() == 0:
        """ Checking if there is no business"""
        response = jsonify({'message': "You have registered no businesses"}), 404
    else:
        response = jsonify(business=[business.serialize for business in businesses]), 200
    return response


@bs.route('/api/v1/businesses/<businessid>', methods=['GET'])
def get_businesses_by_id(businessid):
    """Retrieve a business of a given id"""

    
    if not businessid.isdigit():
        return jsonify({"Error" :"Invalid business Id, kindly use an integer"}), 400

    business = Business.query.filter_by(businessid=businessid)

    if business.count() == 0:
        response=jsonify({"message":"No Business with that ID"}), 404

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

            }),200
        
    return response

@bs.route('/api/v1/businesses/<businessid>', methods=['DELETE'])
def delete_businesses(businessid):
    """Delete a business by the owner while logged in"""
    token = User.validate_token()
    
    
    
    if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
        return jsonify({'Error': 'Invalid token, Login to obtain a new token'}), 401
    
    if not businessid.isdigit():
        return jsonify({"Error" :"Invalid business Id, kindly use an integer"}), 400

    business = Business.query.filter_by(created_by=token['user_id'], businessid=businessid)

    if business.count() == 0:
        response = jsonify({"Error":"You have no business with that ID"}), 404
    else:
        business[0].delete()
        response = jsonify({"Success":"Business Deleted Successfully"}), 200
    return response


@bs.route('/api/v1/businesses/<businessid>', methods=['PUT'])

def update_businesses(businessid):
    """Update a business of the ID indicated in the URL"""

    business_name1 = request.data.get('business_name')
    about1 = request.data.get('about')
    location1 = request.data.get('location')
    category1 = request.data.get('category')

    token = User.validate_token()
    all_input = business_name1 and about1 and location1 and category1

    if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
        return jsonify({'Error': 'Invalid token, Login to obtain a new token'}), 401
    
    if not businessid.isdigit():
        return jsonify({"Error" :"Invalid business Id, kindly use an integer"}), 400

    business = Business.query.filter_by(businessid=businessid, created_by=token['user_id'])  

    if business.count() == 0:
        return jsonify({"Error":"You have no business with that ID"}), 404

    if not all_input:
        return jsonify({'Error': "Invalid input, fill in all required input and kindly use valid strings"}), 400

    business_name = str(business_name1.strip(' '))
    location = str(location1.strip(' '))
    category = str(category1.strip(' '))
    about = str(about1.strip(' '))
    all_stripped_input = business_name and about and location and category

    if not all_stripped_input:
        response = jsonify({'Error': "Fill in the Empty fields"}), 400
    elif business[0].business_name == business_name and business[0].location == location and business[0].category==category and business[0].about==about:
        response = jsonify({'Error': "No changes made, kindly make changes to effect a valid update"}), 400

    elif [bus1 for bus1 in Business.get_all() if bus1.business_name.lower() == business_name.lower() and bus1.businessid != int(businessid)]:
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

