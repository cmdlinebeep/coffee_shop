import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
'''
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    try:
        # Anyone can get the drinks list, so don't decorate with requires_auth()
        drinks = Drink.query.all()

        # Frontend expects a LIST of drinks (formatted as short() since doesn't need component name details)
        # Could be many drinks on the menu
        drinks = [drink.short() for drink in drinks]

        return ({
            'success': True,
            'drinks': drinks
        })
    
    except:
        abort(500)  # Catchall


'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth(permission='get:drinks-detail')
def get_drinks_detail(payload):     # We don't use the payload but the decorator returns it
    try:
        # Only Managers and Baristas should see our top-secret recipe
        drinks = Drink.query.all()

        # Here Frontend expects a list of drinks but with the long() formatting (which includes
        # more details on the recipe names of ingredients)
        drinks = [drink.long() for drink in drinks]

        return ({
            'success': True,
            'drinks': drinks
        })
    
    except:
        abort(500)  # Catchall


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=["POST"])
@requires_auth(permission='post:drinks')
def post_drink(payload):
    # Get the recipe from the body data
    pass

#     new_drink = Drink()



# use dumps to convert json to a string

# title = Column(String(80), unique=True)
#     # the ingredients blob - this stores a lazy json blob
#     # the required datatype is [{'color': string, 'name':string, 'parts':number}]   # NOTE: Here they are storing a list of dictionaries as a string for the recipe
#     recipe =  Column(String(180), nullable=False)



# FIXME: Keep an eye out someday for a postman test that isn't looking for an array (but should be!)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def edit_drink():
    pass


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drink():
    pass



## Error Handling.  Returns tuple of JSON data and integer status code

'''
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def auth_error(excpt):
    # This decorator is called when an exception is thrown of AuthError type
    # (unlike standard aborts which accept integer status error codes)
    # This is for authentication errors only (our decorator)
    response = jsonify(excpt.error)
    response.status_code = excpt.status_code
    return response


@app.errorhandler(400)
def bad_request(error):
    '''Server cannot process request due to client error, such as malformed request'''
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
        }), 400

@app.errorhandler(401)
def unauthorized(error):
    '''Authentication has not yet been provided'''
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "unauthorized"
        }), 401

@app.errorhandler(403)
def forbidden(error):
    '''Server is refusing action, often because user does not have permissions for request'''
    return jsonify({
        "success": False, 
        "error": 403,
        "message": "forbidden"
        }), 403

@app.errorhandler(404)
def not_found(error):
    '''Requested resource could not be found on the server'''
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "not found"
        }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    '''Request method (i.e. GET or POST) is not allowed for this resource'''
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "method not allowed"
        }), 405

@app.errorhandler(422)
def unprocessable(error):
    '''The request was well-formed but unable to be followed due to semantic errors'''
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

@app.errorhandler(500)
def server_error(error):
    '''Catch-all for server error on our end'''
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "internal server error"
        }), 500