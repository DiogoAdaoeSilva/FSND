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
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''


# db_drop_and_create_all()

## ROUTES


'''
[DONE]
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint [DONE - requires_auth decorator not added]
        it should contain only the drink.short() data representation [DONE]
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks [DONE]
        or appropriate status code indicating reason for failure [DONE]
'''



@app.route('/drinks')
def get_drink():
    try:
        drinks = Drink.query.all()
        result = [drink.short() for drink in drinks]
        
        if len(result) == 0:
            abort(404) # Not found - when there are no drink
        return jsonify({'success': True, 'drinks': result})
    except:
        abort(404) # not found

    


'''
[DONE]
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission [DONE]
        it should contain the drink.long() data representation [DONE]
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks [DONE]
        or appropriate status code indicating reason for failure [DONE]
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(self):
    try:
        drinks = Drink.query.all()
        result = [drink.long() for drink in drinks]

        if len(result) == 0:
            abort(404) # Not found

        return jsonify({'success': True, 'drinks': result})
    except:
        abort(404) #Not found




'''
[DONE]
@TODO implement endpoint 
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(self):
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)
    print('>>> title:', title)
    print('>>> recipe:', recipe)

    try:
        print('>>> adding to db')
        drink = Drink(title=title, recipe=json.dumps([recipe])) # recipe has to be passed as a list to work with the short() method
        print('>>> Drink added')
        drink.insert()
        print('>>> Drink inserted in DB')

        return jsonify({
            'success': True,
            'drink': drink.long()
            })
    except:
        abort(404) # Not found



'''
[DONE]
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
@requires_auth('patch:drinks')
def patch_drink(self, id):
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)
    try:
      drink = Drink.query.filter(Drink.id == id).one_or_none()
      if drink is None:
        abort(404) # Not found
      else:
        if title is not None:
            drink.title = title
        if recipe is not None:
            drink.recipe = json.dumps(recipe)
        drink.update()

        long_drink = drink.long() # necessary to pass in funciton return json

        return jsonify({
          'success': True,
          'drinks': [long_drink]
          })

    except:
      abort(422)



'''
[DONE]
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:id>',methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(self,id):
    error = False
    try:
      drink = Drink.query.filter(Drink.id == id).one_or_none()
      if drink is None:
        abort(404) # Not found
      else:
        drink.delete()

        return jsonify({
          'success': True,
          'deleted': id
          })


    except:
      abort(422)


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

''' [DONE]
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request'
      }), 400

'''
[DONE]
@TODO implement error handler for 404
    error handler should conform to general task above''' 

@app.errorhandler(404)
def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Not found' 
      }), 404



'''
[DONE]
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''

# credit to Udacity mentor' answer here: https://knowledge.udacity.com/questions/204223
@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify(e.error), e.status_code
