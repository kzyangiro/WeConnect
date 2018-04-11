from flask import request, make_response, jsonify
from . import bs
from .. models import Business, Review, User

@bs.route('/api/v1/businesses/<int:businessid>/review', methods=['POST'])
def create_a_business_review(businessid):

    # Obtain token from header
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        """If accessed, decode token to get userid"""
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):

            """Endpoint to create a review for a given business"""
            title = str(request.data.get('title'))
            content = str(request.data.get('content'))
            
            if title and content:
                

                businesses = Business.get_all()
                for business in businesses:
                    if business.businessid == businessid:

                        review = Review(title=title, content=content, created_by=user_id, businessid=businessid)
                        review.save()
                        response =make_response(
                        jsonify({
                            'message':'Review added successfully',
                            'title': review.title,
                            'content': review.content,
                            "created_by":user_id
                            
                            }), 201)
                        return response
                            
                    else:
                        response = make_response(
                        jsonify({
                            'message':'No business with the given id'
                            
                            }), 404)
                        return response
                response = make_response(
                jsonify({
                    'message':'No business available'
                    
                    }), 404)
                return response
            else:
                response = make_response(jsonify({
                        'message': "Incomplete Information"
                        }
                ), 400)
                return response

        else:
            # user is not legit, so the payload is an error message
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401 


@bs.route('/api/v1/businesses/<int:businessid>/review', methods=['GET'])
def get_all_business_reviews(businessid):
    """Endpoint to retrieve all reviews for a business"""
    businesses = Business.get_all()
    for business in businesses:
        if business.businessid == businessid:
            if len(business.reviews) == 0:
                response = make_response(jsonify({
                    'message': "No reviews found"
                    }
                ), 404)
                return response

            for reviews in business.reviews:
                business_reviews = []
                business_review = {}
                business_review[reviews.title]= reviews.content
                business_reviews.append(business_review)
            response = make_response(jsonify({
                'Business reviews':business_reviews
                }
                ), 302)
            return response

        else:
             response =make_response(
                jsonify({
                    'message':'No business with the id'
                    
                    }), 404)
        return response    
       

    response = make_response(
            jsonify({
            'message':'No businesses found'
            
            }), 404)
            
    return response
