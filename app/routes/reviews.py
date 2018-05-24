from flask import request, jsonify
from . import bs
import re
from .. models import Business, Review, User, BlacklistToken

@bs.route('/api/v1/businesses/<businessid>/review', methods=['POST'])
def create_a_business_review(businessid):
    """Create a business review, only a logged in user can add a review"""

    content1 = request.data.get('content')
    business = Business.query.filter_by(businessid=businessid).first()
    token = User.validate_token()

    valid = r"[a-zA-Z0-9]*[a-zA-Z][a-zA-Z0-9]*"
    if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
        return jsonify({'message': 'Invalid token, Login to obtain a new token'}), 401

    if isinstance(content1, int):
        return jsonify({'message': "Invalid input, kindly input a valid review"}), 400
        
    if content1:
        content = str(content1.strip(' '))

    if not businessid.isdigit():
        response = jsonify({"message" :"Invalid business Id, kindly use an integer for business ID"}), 400

    elif not business:
        response = jsonify({'message':'No business with the given id', 'status_code': 204})

    elif business.created_by== token['user_id']:
        response = jsonify({'message':'Sorry, You should not review your own business'}), 400

    elif not content1:
        response = jsonify({'message': "Invalid input, kindly fill in all required input"}), 400
    
    elif not re.match(valid, content1):
        response = jsonify({'message': "Invalid input, kindly use alphabets also for input "}), 400


    elif len(content1) < 4:
        response = jsonify({'message': "Kindly add review of at least 4 characters"}), 400
    
    else:
        review = Review(content=content, created_by=token['user_id'], businessid=businessid)
        review.save()
        response = jsonify({
            'Message':'Review added successfully',
            'content': review.content,
            "created By":token['user_id'],
            "creation date":review.date_created
            
            }), 201

    return response

         
@bs.route('/api/v1/businesses/<businessid>/review', methods=['GET'])
def get_all_business_reviews(businessid):
    """Retrieve all reviews for a business using business id"""

    business = Business.query.filter_by(businessid=businessid).first()
    reviews = Review.get_all(businessid)
    results = []

    if not businessid.isdigit():
        response = jsonify({"Message" :"Invalid business Id, kindly use an integer for business ID"}), 400
    elif not business:
        response = jsonify({'message':'No business with the given id', 'status_code': 204})

    elif reviews.count() == 0:
        response = jsonify({'message':'No reviews found', 'status_code': 204})

    else:
        for review in reviews:
            
            obj={
                "Review":review.content,
                "created by":review.created_by,
                "creation date":review.date_created,
                "business_owner":business.created_by
            }

            results.append(obj)
            
        response = jsonify(results),200

    return response
