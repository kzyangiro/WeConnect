from flask import request, make_response, jsonify
from . import bs
from .. models import Business, User, Review, BlacklistToken

@bs.route('/')
def homepage():
    """This is the home endpoint"""
    res = make_response(
        jsonify({
        'message':'Welcome to Weconnect'
        
        }))
                
    return res

@bs.route('/api/v1/businesses', methods=['POST'])
def register_business():
    """This method Creates a business by only authorised users"""
    

    business_name1 = request.data.get('business_name')
    about1 = request.data.get('about')
    location1 = request.data.get('location')
    category1 = request.data.get('category')


    """ Confirm user is authorised """
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
                return jsonify({'status':'You are logged out kindly login to get a new token'}),401


        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            
            try:

                if business_name1 and about1 and location1 and category1:

                    business_name = str(business_name1.strip(' '))
                    location = str(location1.strip(' '))
                    category = str(category1.strip(' '))
                    about = str(about1.strip(' '))
                else:
                    return jsonify({'message': "Invalid input, kindly fill in all required input"}), 400

                if business_name and about and location and category:
                    businesses = Business.get_all()
                    for business in businesses:
                        if business.business_name == business_name:
                            return jsonify({"Error":"Business already exists, use a different business name"}), 409

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

                return jsonify({'Message': "Kindly input the missing fields"}), 400

            except Exception as e:
                return jsonify({'message': e}), 401
        else:
            return jsonify({'message': 'Invalid token, Login to obtain a new token'}), 401

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

    if len(businesses) == 0:
        """ Checking if there is no business"""

        return make_response(jsonify({'Message': "No Businesses Available"}), 404)
        
    else:

        if q:
            
            """Retrieve a business by the given search name"""
            businesses = Business.query.filter(Business.business_name.contains(q))
            results = []

            business = [bus for bus in businesses]
            if not business:
                return make_response(jsonify({"message":"Sorry, No business with that name"}), 404)
            for business in businesses:

                obj={
                "Business id":business.businessid,
                "Business Name":business.business_name,
                "Category":business.category,
                "Business location":business.location

                }
                results.append(obj)


                response=jsonify(results)
                response.status_code = 200
            
                return response

        elif location:

            """Retrieve businesses in a given location"""
            businesses = Business.query.filter(Business.location.contains(location))
            results = []

            business = [bus for bus in businesses]
            if not business:
                return make_response(jsonify({"Message" :"Sorry, No business in that location"}), 404)
            for business in businesses:

                obj={
                "Business id":business.businessid,
                "Business Name":business.business_name,
                "Category":business.category,
                "Business location":business.location

                }
                results.append(obj)


                response=jsonify(results)
                response.status_code = 200
            
            return response


        elif category:

            """Retrieve businesses in a given location"""
            businesses = Business.query.filter(Business.category.contains(category))
            results = []

            business = [bus for bus in businesses]
            if not business:
                return make_response(jsonify({"Message" :"Sorry, No business in that category"}), 404)
            for business in businesses:

                obj={
                "Business id":business.businessid,
                "Business Name":business.business_name,
                "Category":business.category,
                "Business location":business.location

                }
                results.append(obj)


                response=jsonify(results)
                response.status_code = 200
            
            return response

        elif limit and not offset:
            return make_response(jsonify({"Message" :"Indicate the offset"}), 200)

        elif offset and not limit:
            return make_response(jsonify({"Message" :"Indicate the limit"}), 200)

        elif limit and offset:
            try:
                limit = int(limit)
                offset = int(offset)

            except ValueError:
                return make_response(jsonify({"Message" :"Invalid Limit or offset, kindly use an integer"}), 400)

            """Retrieve businesses in a given location"""
            businesses = Business.businesses_pagination(offset,limit)
            results = []

            business = [bus for bus in businesses]
            if not business:
                return make_response(jsonify({"Message" :"Sorry, No business found"}), 404)
            for business in businesses:

                obj={
                "Business id":business.businessid,
                "Business Name":business.business_name,
                "Category":business.category,
                "Business location":business.location

                }
                results.append(obj)


                response=jsonify(results)
                response.status_code = 200
            
            return response


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
                return jsonify({'status':'You are logged out kindly login to get a new token'}),401

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



@bs.route('/api/v1/businesses/<businessid>', methods=['GET'])
def get_businesses_by_id(businessid):
    try:
        businessid = int(businessid)

    except ValueError:
        return make_response(jsonify({"Message" :"Invalid business Id, kindly use an integer"}), 400)


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


@bs.route('/api/v1/businesses/<businessid>', methods=['DELETE'])
def delete_businesses(businessid):
    """This method deletes a business, but only by the owner while logged in"""
    try:
        businessid = int(businessid)

    except ValueError:
        return make_response(jsonify({"Message" :"Invalid business Id, kindly use an integer"}), 400)

    
    """Obtain token from header"""
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
                return jsonify({'status':'You are logged out kindly login to get a new token'}),401
        
        """If accessed, decode token to get userid"""
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            
            
            businesses = Business.query.filter_by(created_by=user_id)

            reviews = Review.get_all(businessid)

            for business in businesses:

                if businessid == business.businessid:
                    
                    business.delete()
                    
                    if reviews:
                        reviews.delete()
                    else:
                        pass

                    return jsonify({"Success":"Business Deleted Successfully"}), 200

            return jsonify({"Error":"You have no business with that ID"}), 404

        else:
            """Invalid Access token, payload error"""
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401

    return make_response(jsonify({'message': 'Invalid token, Login to obtain a new token'})), 401
        
@bs.route('/api/v1/businesses/<businessid>', methods=['PUT'])

def update_businesses(businessid):
    """This method uses input data to update the content of a business of the ID indicated in the URL"""

    try:
        businessid = int(businessid)

    except ValueError:
        return make_response(jsonify({"Message" :"Invalid business Id, kindly use an integer"}), 400)

    
    business_name1 = request.data.get('business_name')
    about1 = request.data.get('about')
    location1 = request.data.get('location')
    category1 = request.data.get('category')


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
                return jsonify({'status':'You are logged out kindly login to get a new token'}),401


        """Decode token"""
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            
            try:
                if business_name1 and about1 and location1 and category1:

                    business_name = str(business_name1.strip(' '))
                    location = str(location1.strip(' '))
                    category = str(category1.strip(' '))
                    about = str(about1.strip(' '))
                else:
                    return jsonify({'message': "Fill in the empty fields"}), 400

                if business_name and about and location and category:
                    businesses = Business.query.filter_by(created_by=user_id)

                    all_businesses = Business.get_all()
                    business = [bus for bus in businesses if bus.businessid == businessid]

                    existing = [bus1 for bus1 in all_businesses if bus1.business_name == business_name and bus1.businessid != businessid]

                    if not business:
                            return jsonify({'Message': "You have no business with that ID"}), 404

                    else:
                        
                        if existing:
                            return jsonify({"Error":"Business Already Exists, use a different business name"}), 409

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
                                "modified_by":user_id

                            })
                            response.status_code = 200
                            return response
                
                return jsonify({'Message': "Fill in the Empty fields"}), 400

            except Exception as e:
                return make_response(jsonify({'message': e})), 401

        return make_response(jsonify({'message': 'Invalid token, Login to obtain a new token'})), 401
