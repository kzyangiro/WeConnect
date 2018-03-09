from flask import request, make_response, jsonify
from . import bs
from .. models import Business

@bs.route('/',methods=['POST'])
def homepage():
    res = make_response(
        jsonify({
        'message':'Welcome to Weconnect'
        
        }))
                
    return res

@bs.route('/api/v1/businesses', methods=['POST'])
def register_business():

    business_name = str(request.data.get('business_name').strip(' '))
    about = str(request.data.get('about').strip(' '))
    location = str(request.data.get('location').strip(' '))
    category = str(request.data.get('category').strip(' '))
          
    if business_name and about and location and category:
        for business in Business.business_list:
            if business.business_name == business_name:
                response =make_response(
                jsonify({
                    'message':'Business already exists'
                    
                    
                    }), 400)
                return response
        business = Business(business_name=business_name, about=about, location=location, category=category)

        mybusinesses={'Business Name':business.business_name,'Description':business.about,'Location':business.location,'Category':business.category}

        business.save(business)
        response =make_response(
            jsonify({
                'business details': mybusinesses,
                'Message':'Business created successfully',
                "status-code": 201
                
                
                
                }), 201)
        return response
    else:
        response = make_response(jsonify({
                'message': "Incomplete information"
                }
        ), 404)
        return response 

@bs.route('/api/v1/businesses', methods=['GET'])
def retrieve_all_businesses():
        
    

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
                'Message':'Available Businesses',
                'businesses': businesses
                
                }), 200)
            
            return response

@bs.route('/api/v1/businesses/<int:businessid>', methods=['GET'])
def get_businesses_by_id(businessid):
    
        if len(Business.business_list) == 0:
            response = make_response(jsonify({
                'message': "No businesses available"
                }
            ), 404)
            return response

        else:
            businesses={}
            for business in Business.business_list:
                if businessid == business.businessid:
                    business.business_name
                    business.businessid
                    businesses.update({business.businessid:business.business_name})


                    response = make_response(
                        jsonify({
                        'Message':'Business found:',
                        'businesses': businesses
                        
                        }), 200)
                    
                    return response
            response = make_response(
                jsonify({
                'message':'Business not found:'
                
                }), 404)
                
            return response

@bs.route('/api/v1/businesses/<int:businessid>', methods=['PUT'])

def update_businesses(businessid):
    business_name = str(request.data.get('business_name').strip(' '))
    location = str(request.data.get('location').strip(' '))
    category = str(request.data.get('category').strip(' '))
    about = str(request.data.get('about').strip(' '))

    for business in Business.business_list:
        if businessid == business.businessid:
            business.business_name=business_name
            business.location=location
            business.category=category
            business.about=about

            response = make_response(
                        jsonify({
                        'message':'Business Updated'
                        
                        }), 200)
                    
            return response
    response = make_response(
                    jsonify({
                    'message':'Business not found'
                    
                    }), 404)
                
    return response

@bs.route('/api/v1/businesses/<int:businessid>', methods=['DELETE'])
def delete_businesses(businessid):
    
    for business in Business.business_list:
        if businessid == business.businessid:
            Business.business_list.remove(business)

        response = make_response(
                    jsonify({
                    'message':'The business deleted successful'
                    
                    }), 204)
                
        return response
    response = make_response(
        jsonify({
        'message':'The business not found'
        
        }), 404)
            
    return response
