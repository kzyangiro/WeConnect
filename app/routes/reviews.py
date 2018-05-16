from flask import request, make_response, jsonify
from . import bs
from .. models import Business, Review, User, BlacklistToken

@bs.route('/api/v1/businesses/<businessid>/review', methods=['POST'])
def create_a_business_review(businessid):

    try:
        businessid = int(businessid)

    except ValueError:
        return make_response(jsonify({"message" :"Invalid business Id, kindly use an integer for business ID"}), 400)


    """Add review for a business, only a logged in user can add a review"""
    title1 = request.data.get('title')
    content1 = request.data.get('content')

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
                return jsonify({'status':'You are already Logged Out'}),401

        """If accessed, decode token to get userid"""
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):

            if title1 and content1:
                title = str(title1.strip(' '))
                content = str(content1.strip(' '))


                businesses = Business.get_all()

                if len(businesses) == 0:
                    return jsonify({'message':'No business available'}), 404

                else:
                    for business in businesses:
                        if business.businessid == businessid:

                            review = Review(title=title, content=content, created_by=user_id, businessid=businessid)
                            review.save()
                            response =make_response(
                            jsonify({
                                'Message':'Review added successfully',
                                'Title': review.title,
                                'content': review.content,
                                "created By":user_id,
                                "creation date":review.date_created
                                
                                }), 201)
                            return response
                                
                        
                    response = make_response(
                    jsonify({
                        'message':'No business with the given id'
                        
                        }), 404)
                    return response

            else:
                return make_response(jsonify({'message': "Invalid input, kindly fill in all required variables"}), 400)

        else:
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401 


@bs.route('/api/v1/businesses/<businessid>/review', methods=['GET'])
def get_all_business_reviews(businessid):

    try:
        businessid = int(businessid)

    except ValueError:
        return make_response(jsonify({"Message" :"Invalid Id, kindly use an integer for business ID"}), 400)


    """Retrieve all reviews for a business"""
    businesses = Business.get_all()
    for business in businesses:
        if business.businessid == businessid:
            reviews = Review.get_all(businessid)
            results=[]

            if reviews.count() == 0:
                
                return make_response(jsonify({'message':'No reviews found'}), 404)
            else:

                for review in reviews:
                    
                    obj={
                        "Title":review.title,
                        "content":review.content,
                        "created by":review.created_by,
                        "creation date":review.date_created
                    }

                    results.append(obj)
                    
                return make_response(jsonify(results)),200

    return jsonify({'message':'No business with the given id'}), 404 
       


