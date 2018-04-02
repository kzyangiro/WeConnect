from flask import request, make_response, jsonify
from . import bs
from .. models import Business

@bs.route('/', methods=['POST', 'GET'])
def homepage():
    """This is the home endpoint"""
    res = make_response(
        jsonify({
        'message':'Welcome to Weconnect'
        
        }))
                
    return res
@bs.route('/api/v1/businesses', methods=['POST', 'GET'])
def register_business():
    if request.method == 'POST':

        business_name = str(request.data.get('business_name').strip(' '))
        about = str(request.data.get('about').strip(' '))
        location = str(request.data.get('location').strip(' '))
        category = str(request.data.get('category').strip(' '))
        
        if business_name and about and location and category:
            businesses = Business.get_all()
            for business in businesses:
                if business.business_name == business_name:
                    res = jsonify({
                        "Error":"Business Already Exists"
                    })
                    res.status_code = 409
                    return res

            business = Business(business_name=business_name, about=about, location=location, category=category)
            business.save()
            response = jsonify({
                "Success":"Business Created successfully",
                "business Name":business.business_name,
                "category":business.category,
                "location":business.location

            })
            response.status_code = 201
            return response

        response = make_response(jsonify({
                'Message': "Kindly input the missing fields"
                }
            ), 400)
        return response


    elif request.method == 'GET':
        #Retrieve all businesses
        businesses = Business.get_all()
        results = []

        if len(businesses)==0:
            response = make_response(jsonify({
                'Message': "No Businesses Available"
                }
            ), 404)
            return response

        else:


            for business in businesses:
                obj={
                    business.businessid:business.business_name
                }
                results.append(obj)

                response=jsonify(results)
                response.status_code = 200
            return response


@bs.route('/api/v1/businesses/<int:businessid>', methods=['GET'])
def get_businesses_by_id(businessid):
    """This endpoint retrieves a business by the given id"""
    businesses = Business.get_all()

    if len(businesses)==0:
        response = make_response(jsonify({
            'Message': "No Businesses Available"
            }
        ), 404)
        return response

    else:
        for business in businesses:
            if businessid == business.businessid:
                obj={
                    "Business Name":business.business_name,
                    "Category":business.category,
                    "Location":business.location,
                    "about":business.about
                }
                response=jsonify(obj)
                response.status_code = 200
                return response

        response=jsonify({"Error":"No Business with that ID"})
        response.status_code = 200
        return response

@bs.route('/api/v1/businesses/<int:businessid>', methods=['DELETE'])
def delete_businesses(businessid):
    businesses=Business.get_all()


    if len(businesses)==0:
        response = make_response(jsonify({
            'Message': "No Businesses Available"
            }
        ), 404)
        return response

    else:
        for business in businesses:
            if businessid == business.businessid:
                business.delete()
                response=jsonify({"Success":"Business Deleted Successfully"})
                response.status_code = 200
                return response

        response=jsonify({"Error":"No Business with that ID"})
        response.status_code = 200
        return response


@bs.route('/api/v1/businesses/<int:businessid>', methods=['PUT'])

def update_businesses(businessid):
    """This endpoint uses input data to update the content of a business of the ID indicated in the URL"""
    business_name = str(request.data.get('business_name').strip(' '))
    location = str(request.data.get('location').strip(' '))
    category = str(request.data.get('category').strip(' '))
    about = str(request.data.get('about').strip(' '))

    businesses=Business.get_all()

    if business_name and location and category and about:

        for business in businesses:
            if businessid == business.businessid:
                business.business_name=business_name
                business.location=location
                business.category=category
                business.about=about 

                business.save()

                response = make_response(
                            jsonify({
                            'message':'Business Updated Successfully'
                            
                            }), 200)
                        
                return response
        response = make_response(
                        jsonify({
                        'message':'No Business with that ID'
                        
                        }), 404)
                    
        return response

    response = make_response(
                    jsonify({
                    'message':'Fill in the Empty fields'
                    
                    }), 400)
                
    return response

