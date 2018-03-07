from flask import request, make_response, jsonify
from . import bs
from .. models import Business

@bs.route('/')
@bs.route('/api/businesses', methods=['POST'])
def register_business():

    business_name = str(request.data.get('business_name'))
    about = str(request.data.get('about'))
    location = str(request.data.get('location'))
    contacts = str(request.data.get('contacts'))
    if business_name and about and location and contacts:
        business = Business(business_name=business_name, about=about, location=location, contacts=contacts)
        business.save(business)
        response =make_response(
            jsonify({
                'message':'business added successfully'
                
                }), 201)
        return response
    else:
        response = make_response(jsonify({
                'message': "incomplete information"
                }
        ), 404)
        return response 