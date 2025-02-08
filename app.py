from datetime import datetime, timedelta
from functools import wraps
import os

from flask import Flask, request, jsonify, make_response, abort
from flask_migrate import Migrate
from sqlalchemy import and_, text, func, nullslast
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from dotenv import load_dotenv

from models import User, Character
from database import db


def create_app():
    """function to create flask app"""
    flask_app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # Set the database URI
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URL")

    # Initialize the db instance with the app
    db.init_app(flask_app)

    return flask_app


app = create_app()

# # Create database tables
# with app.app_context():
#     db.create_all()

# Initialize database migration
# migrate = Migrate(app, db)


def create_filtering_query(filters):
    """
    function to create the sqlalchemy query applying the filters provided.
    :param filters: dictionary with different attributes (default values None).
    :return: a sqlalchemy query.
    """
    query = Character.query
    filters = {key: value for key, value in filters.items() if value is not None}
    conditions = []

    try:
        if "age" in filters:
            conditions.append(Character.age == int(filters['age']))

        if "age_less_than" in filters:
            conditions.append(Character.age < int(filters['age_less_than']))

        if "age_more_than" in filters:
            conditions.append(Character.age >= int(filters['age_more_than']))

        if "house" in filters:
            conditions.append(func.lower(Character.house) == func.lower(filters['house']))

        if "animal" in filters:
            conditions.append(func.lower(Character.animal) == func.lower(filters['animal']))

        if "death" in filters:
            conditions.append(Character.death == int(filters['death']))

        if "name" in filters:
            conditions.append(func.lower(Character.name) == func.lower(filters['name']))

        if "nickname" in filters:
            conditions.append(func.lower(Character.nickname) == func.lower(filters['nickname']))

        if "role" in filters:
            conditions.append(func.lower(Character.role) == func.lower(filters['role']))

        if "symbol" in filters:
            conditions.append(func.lower(Character.symbol) == func.lower(filters['symbol']))

        if "strength" in filters:
            conditions.append(func.lower(Character.strength) == func.lower(filters['strength']))

        # Apply all conditions using AND
        if conditions:
            query = query.filter(and_(*conditions))

        return query

    except ValueError as e:
        # Handle invalid numeric values
        raise ValueError(f"Invalid numeric value in filters: {str(e)}")


def token_required(f):
    """
    decorator function for verifying JWT token.
    :param f: the original function being wrapped by this decorator.
    :return: - returns a JSON response with a 401 status if the token is missing or invalid.
             - calls and returns the original function's response if the token is valid.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        jwt_key = os.getenv("JWT_KEY")
        if not jwt_key:
            raise ValueError("Missing JWT_KEY environment variable")

        token = None
        # jwt is passed in the request headers as Authorization
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, jwt_key, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data["id"]).first()
        except Exception as e:
            return jsonify({
                "message": f"Token is invalid. {e}"
            }), 401
        return f(*args, **kwargs)

    return decorated


@app.route('/login', methods=['POST'])
def login():
    """
    login endpoint for user login
    :return: - if login fails: HTTP response 401 and message
             - if login successful: generated JWT token and HTTP response 201
    """
    auth = request.json
    jwt_key = os.getenv("JWT_KEY")
    if not jwt_key:
        raise ValueError("Missing JWT_KEY environment variable")

    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response(
            'Proper credentials not provided',
            401
        )
    user = User.query.filter_by(username=auth.get('username')).first()
    if not user:
        return make_response(
            'Please create an account',
            401
        )

    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, jwt_key, "HS256")
        return make_response(jsonify({'token': token}), 201)
    #  password is wrong
    return make_response(
        'Please check your credentials',
        401
    )


@app.route("/signup", methods=['POST'])
def signup():
    """
    signup endpoint for user creation.
    :return: - if the account exists: a 409 response.
             - if user created: a 201 response
             - if otherwise failed: a 500 response
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username and password:
        user = User.query.filter_by(username=username).first()
        if user:
            return make_response(
                {"message": 'Username already taken. Choose a different one, or log in.'},
                409
            )
        user = User(
            username=data['username'],
            password=generate_password_hash(data['password'])
        )
        db.session.add(user)
        db.session.commit()
        return make_response(
            {"message": 'User created'},
            201
        )
    return make_response(
        {"message": 'Unable to create user'},
        500
    )


@app.route('/api/characters', methods=['GET'])
# @limiter.limit("10/minute")  # possible request limiter, deactivated for development
def get_characters():
    """
    fetches characters according to query, allowing for filtering, sorting and pagination.
    :return: list of fetched characters
    """
    app.logger.info('GET request received for /api/characters')
    filters = dict(age=request.args.get('age'), age_more_than=request.args.get('age_more_than'),
                   age_less_than=request.args.get('age_less_than'), animal=request.args.get('animal'),
                   death=request.args.get('death'), house=request.args.get('house'), name=request.args.get('name'),
                   nickname=request.args.get('nickname'), strength=request.args.get('strength'),
                   symbol=request.args.get('symbol'), role=request.args.get('role'))

    skip = request.args.get('skip')
    limit = request.args.get('limit')
    is_reverse = request.args.get('sort_des') is not None
    sort_by = request.args.get('sort_by')

    valid_sorting_attributes = ['age', 'animal', 'death', 'house', 'name', 'nickname', 'strength', 'symbol', 'role']
    if sort_by and sort_by not in valid_sorting_attributes:
        abort(code=400,
              description=f"Invalid Input. Attribute {sort_by} doesn't exist.")

    query = create_filtering_query(filters)

    # Apply sorting
    if sort_by:
        direction = 'desc' if is_reverse else 'asc'
        query = query.order_by(nullslast(text(f'{sort_by} {direction}')))
    elif is_reverse:
        query = query.order_by(text('id desc'))
    elif not skip and not limit:  # if no sorting and no pagination, then fetch random
        query = query.order_by(func.random())

    # Apply pagination
    limit = int(limit) if limit else 20
    if skip:
        if len(query.all()) <= int(skip):
            abort(code=400,
                  description="Next page is empty (skip larger than results).")
        query = query.offset(int(skip))
    query = query.limit(limit)

    result = query.all()
    return jsonify([character.serialize for character in result])


@app.route('/api/characters/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    """
    fetches a character from storage by its id
    :param character_id: the character's id
    :return: the character
    """
    app.logger.info('GET request received for /api/characters')
    character = Character.query.filter_by(id=character_id).one_or_none()
    if character is None:
        return jsonify({"error": "Couldn't find character"}), 404

    return jsonify(character.serialize)


@app.route('/api/characters', methods=['POST'])
@token_required
def add_character():
    """
    adds a character to the database, after input validation
    :return: the added character
    """
    app.logger.info('POST request received for /api/characters')  # Log a message
    new_character = request.get_json()

    # input validation
    mandatory_fields = ['name']
    str_fields = ['name', 'house', 'animal', 'symbol', 'nickname', 'role', 'strength']
    int_fields = ['age', 'death']
    for mandatory_field in mandatory_fields:
        if mandatory_field not in new_character:
            abort(code=400,
                  description=f"Bad Input. {mandatory_field.capitalize()} must be specified")
    for str_field in str_fields:
        if str_field in new_character and not isinstance(new_character[str_field], str):
            abort(code=400,
                  description=f"Bad Input. {str_field.capitalize()} must be a string")
    for int_field in int_fields:
        if int_field in new_character and not isinstance(new_character[int_field], int):
            abort(code=400,
                  description=f"Bad Input. {int_field.capitalize()} must be an integer")

    try:
        db_character = Character(**new_character)
    except TypeError as e:
        abort(code=400,
              description=f"Bad Input. {e}")

    try:
        db.session.add(db_character)
        db.session.commit()
        return jsonify(db_character.serialize), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        if e.code == "gkpj":  # sqlalchemy error: duplicate key value violates unique constraint...
            abort(code=400,
                  description="Integrity error. Character with this name already exists in the database")


@app.route('/api/characters/<int:character_id>', methods=['PUT'])
@token_required
def put_character(character_id):
    """
    updates a character's information in the database
    :param character_id: character-id
    :return: the updated character
    """
    app.logger.info('PUT request received for /api/characters')
    new_character_data = request.get_json()
    db_character = Character.query.filter_by(id=character_id).one_or_none()
    if db_character is None:
        abort(code=404,
              description="Character not found")

    if "id" in new_character_data:
        abort(code=400,
              description="ID cannot be updated")

    for key, value in new_character_data.items():
        if value is not None:
            setattr(db_character, key, value)

    try:
        db.session.commit()
        db.session.refresh(db_character)
        return jsonify(db_character.serialize), 200
    except SQLAlchemyError as e:
        if e.code == "9h9h":
            db.session.rollback()
            abort(422, description="Invalid input.")


@app.route('/api/characters/<int:character_id>', methods=['DELETE'])
@token_required
def delete_character(character_id):
    """
    deletes a character from the database
    :param character_id: the character's id
    :return: the deleted character
    """
    app.logger.info('DELETE request received for /api/characters')
    db_character = Character.query.filter_by(id=character_id).one_or_none()
    if db_character is None:
        abort(code=404,
              description="Character not found")

    db.session.delete(db_character)
    db.session.commit()
    return jsonify({"success": "Character successfully deleted"}), 204


@app.errorhandler(400)
def bad_request_error(error):
    """handle 400 errors"""
    return jsonify({"error": "400 Bad request", "description": str(error)}), 400


@app.errorhandler(404)
def not_found_error(error):
    """handle 404 errors"""
    return jsonify({"error": "404 Not found", "description": str(error)}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    """handle 405 errors"""
    return jsonify({"error": "405 Method not allowed", "description": str(error)}), 405


@app.errorhandler(422)
def unprocessable_request_error(error):
    """handle 422 errors"""
    return jsonify({"error": "422 Unprocessable Entity", "description": str(error)}), 422


@app.errorhandler(429)  # Handle 429 Too Many Requests
def ratelimit_error(error):
    """handle 429 errors"""
    return jsonify({"error": "429 Rate limit exceeded", "description": str(error)}), 429


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
