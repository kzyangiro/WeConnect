from flask import request, jsonify
from . import bs
import re
from .. models import Business, Review, User,   Tokens

@bs.route('/api/v1/businesses/<businessid>/review', methods=['POST'])
def create_a_business_review(businessid):
    """Create a business review, only a logged in user can add a review"""

    content1 = request.data.get('content')
    token = User.validate_token()

    if not token['access_token']or token['decodable_token'] or token['blacklisted_token']:
        return jsonify({'Error': 'Invalid token, Login to obtain a new token'}), 401

    if not businessid.isdigit():
        return jsonify({"Error" :"Invalid business Id, kindly use an integer for business ID"}), 400
    business = Business.query.filter_by(businessid=businessid).first()

    if not business:
        return jsonify({'Error':'No business with the given id', 'status_code': 204})

    if business.created_by== token['user_id']:
        return jsonify({'Error':'Sorry, You should not review your own business'}), 400

    if isinstance(content1, int) or not content1:
        return jsonify({'Error': "Invalid input, fill in all required input and kindly use a valid string"}), 400

    content = str(content1.strip(' '))

    if len(content) < 4 or content.isnumeric() or not content:
        response = jsonify({'Error': "Kindly add a valid review and use at least 4 characters"}), 400
    
    else:
        review = Review(content=content, created_by=token['user_id'], businessid=businessid)
        review.save()
        response = jsonify({
            'Success':'Review added successfully',
            'content': review.content,
            "created By":token['user_id'],
            "creation date":review.date_created }), 201

    return response

         
@bs.route('/api/v1/businesses/<businessid>/review', methods=['GET'])
def get_all_business_reviews(businessid):
    """Retrieve all reviews for a business using business id"""

    results = []

    if not businessid.isdigit():
        return jsonify({"Error" :"Invalid business Id, kindly use an integer for business ID"}), 400

    if not Business.query.filter_by(businessid=businessid).first():
        return jsonify({'Error':'No business with the given id', 'status_code': 204})
    reviews = Review.get_all(businessid)

    if reviews.count() == 0:
        response = jsonify({'message':'No reviews found', 'status_code': 204})

    else:
        for review in reviews:
            
            obj={
                "Review":review.content,
                "created by":review.created_by,
                "creation date":review.date_created
            }

            results.append(obj)
            
        response = jsonify(results),200

    return response
