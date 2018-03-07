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

@bs.route('/api/businesses', methods=['GET'])
def retrieve_all_businesses():
        Business.business_list
    

        if len(Business.business_list) == 0:
            response = make_response(jsonify({
                'message': "No businesses found"
                }
            ), 404)
            return response

        else:
            businesses={}
            for business in Business.business_list:
                business.business_name
                business.businessid
                businesses.update({business.businessid:business.business_name})


            response = make_response(
                jsonify({
                'message':'Available Businesses',
                'businesses': businesses
                
                }), 200)
            
            return response