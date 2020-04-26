import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth, get_token_auth_header

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


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    if len(drinks) == 0:
        abort(404)

    drinks_shorts = [drink.short() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': drinks_shorts
    })


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_details(jwt):
    drinks = Drink.query.all()

    drink_long = [drink.long() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': drink_long
    })



@app.route('/drinks', methods=['POST'])
@requires_auth("post:drinks")
def create_drink(jwt):
    body = request.get_json()
    title = body['title']
    recipe = body['recipe']

    new_drink = Drink(title=title, recipe=json.dumps(recipe))

    try:
        new_drink.insert()
    except Exception as e:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': new_drink.long()
    })


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth("patch:drinks")
def edit_drink(*args, **kwargs):
    id = kwargs['id']

    update_drink = Drink.query.filter_by(id=id).one_or_none()
    if update_drink is None:
        abort(404)

    body = request.get_json()
    if 'title' in body:
        update_drink.title = body['title']
    if 'recipe' in body:
        update_drink.recipe = json.dumps(body['recipe'])
    try:
        update_drink.insert()
    except Exception as e:
        abort(400)

    drink = [update_drink.long()]
    return jsonify({
        'success': True,
        'drinks': drink
    })


@app.route('/drinks/<id>', methods=['Delete'])
@requires_auth("delete:drinks")
def delete_drink(*args, **kwargs):
    id = kwargs['id']

    delete_drink = Drink.query.filter_by(id=id).one_or_none()
    if delete_drink is None:
        abort(404)
    try:
        delete_drink.delete()
    except Exception as e:
        abort(500)

    return jsonify({
        'success': True,
        'deleted': id,
    })


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"

    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
