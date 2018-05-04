from flask import request, make_response, jsonify
from . import bs
from .. models import Review, Business, User, BlacklistToken

@bs.route('/api/v1/businesses/<int:businessid>/review', methods=['POST'])
def create_a_business_review(businessid):
    """Endpoint to create a review for a given business"""
    title = str(request.data.get('title'))
    content = str(request.data.get('content'))
    
    """ Confirm user is authorised """
    auth_header = request.headers.get('Authorization')

    if auth_header:
        access_token = auth_header.split(' ')[1]
    else:
        access_token = 'Invalid Token'

    if access_token:

        for token in BlacklistToken.blacklist_tokens:
            "Check if input access token is blacklisted, if yes, prompt new login"
            if token == access_token:
                responce = make_response(jsonify({'status':'You are already Logged Out, kindly login first'}),400)
                return responce 
          
  
        """Decode token"""
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            
            try:
                            
                if title and content:
                    review = Review(title, content)
                    for business in Business.business_list:
                        if business.businessid == businessid:
                            
                            business.reviews.append(review)

                            return jsonify({'message': 'Review added successfully'}), 201
                                
                        return jsonify({'message': 'No business with the given id'}), 404

                return jsonify({'message': 'Incomplete Information'}), 400

            except Exception as e:
                return jsonify({'message': e}), 401
        return jsonify({'message': 'Invalid token, Login to obtain a new token'}), 401


@bs.route('/api/v1/businesses/<int:businessid>/review', methods=['GET'])
def get_all_business_reviews(businessid):
    """Endpoint to retrieve all reviews for a business"""
    for business in Business.business_list:
        if business.businessid == businessid:
            business_reviews = []
            
            if len(business.reviews) == 0:
                return jsonify({'message': 'No review found'}), 404

            for reviews in business.reviews:
                
                business_review = {}
                business_review[reviews.title]= reviews.content
                business_reviews.append(business_review)
            
            return jsonify({'Business reviews':business_reviews}), 200

        return jsonify({'message': 'No business with that id'}), 404   
 
            
    return jsonify({'message': 'No businesses found'}), 404
 