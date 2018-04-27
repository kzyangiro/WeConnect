from flask import request, make_response, jsonify
from . import bs
from .. models import Business, Review, User

@bs.route('/api/v1/businesses/<int:businessid>/review', methods=['POST'])
def create_a_business_review(businessid):

    """Add review for a business, only a logged in user can add a review"""
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        """If accessed, decode token to get userid"""
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):

            title = str(request.data.get('title'))
            content = str(request.data.get('content'))
            
            if title and content:

                businesses = Business.get_all()

                if len(businesses) == 0:
                    response = make_response(
                    jsonify({
                        'message':'No business available'
                        
                        }), 404)
                    return response

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
                response = make_response(jsonify({
                        'message': "Incomplete Information"
                        }
                ), 400)
                return response

        else:
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401 


@bs.route('/api/v1/businesses/<int:businessid>/review', methods=['GET'])
def get_all_business_reviews(businessid):
    """Retrieve all reviews for a business"""
    businesses = Business.get_all()
    for business in businesses:
        if business.businessid == businessid:
            reviews = Review.get_all(businessid)
            results=[]

            if reviews.count() == 0:
                
                response = make_response(jsonify({
                    'message':'No reviews found'
                    }
                    ), 404)
                return response
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


    response =make_response(
            jsonify({
                'message':'No business with the given id'
                
                }), 404)
    return response    
       


