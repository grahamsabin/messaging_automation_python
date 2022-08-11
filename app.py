from functools import wraps

import jwt
from flask import Flask, request, make_response, jsonify
import pymysql.cursors
import pymysql
import os
import uuid # for public id
from datetime import datetime, timedelta


from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.secret_key = 'graham app'

DB_host = os.getenv('CLEARDB_HOST')
DB_user = os.getenv('CLEARDB_USER')
DB_password = os.getenv('CLEARDB_PASSWORD')
DB_database = os.getenv('CLEARDB_DATABASE')

mysql = pymysql.connect(host=DB_host,  # potentially change the name back to 'connection'
                        user=DB_user,
                        password=DB_password,
                        database=DB_database,
                        cursorclass=pymysql.cursors.DictCursor)


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header as "x-access-token"
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the public_id
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms="HS256")

            # search for the user the jwt belongs to by public_id
            with mysql.cursor() as JWTcursor:
                sql = "SELECT * FROM `users` WHERE `public_id`=%s"
                JWTcursor.execute(sql, data['public_id'])
                current_user = JWTcursor.fetchone()
                print(current_user)
                JWTcursor.close()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401

        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


# login route
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # creates a variable to collect the whole request body
    auth = request.form

    # checks for a valid call to the endpoint
    if not auth or not auth.get('phone_number') or not auth.get('password'):
        return make_response(
            'Could not verif - provide proper login information',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    with mysql.cursor() as cursor:
        sql = "SELECT * FROM `users` WHERE `phone_number`=%s"
        cursor.execute(sql, auth.get('phone_number'))
        user = cursor.fetchone()
        print(user)

        cursor.close()

    if not user:
        return make_response(
            'Could not verify - User does not exist',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )
    print(user['password'])
    pwhash = user['password']

    if check_password_hash(pwhash, auth.get('password')):
        token = jwt.encode({
            'public_id': user['public_id'],
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, os.getenv('SECRET_KEY'))

        return make_response(jsonify({'token': token}), 201)

    return make_response(
        'Could not verify - wrong password',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


# signup route
@app.route('/signup', methods=['POST'])
def signup():
    # creates a variable to collect the whole request body
    data = request.form

    # get name, phone number, and password
    name, phone_number = data.get('name'), data.get('phone_number')
    password = data.get('password')

    # check if the user already exists
    with mysql.cursor() as searchCursor:
        sql = "SELECT * FROM `users` WHERE `phone_number`=%s"
        searchCursor.execute(sql, data.get('phone_number'))
        user = searchCursor.fetchone()
        print(user)
        searchCursor.close()

    if not user:
        # add the new user to the database
        with mysql.cursor() as updateCursor:
            sql = "INSERT INTO `users` (`public_id`, `name`, `phone_number`, `password`) VALUES (%s, %s, %s, %s)"
            updateCursor.execute(sql, (str(uuid.uuid4()), name, phone_number, generate_password_hash(password)))
            mysql.commit()
            updateCursor.close()

        return make_response('Successfully registered.', 201)
    else:
        # returns a response if the user already exists - asks them to login
        return make_response('User already exists. Please Log in.', 202)


# this route sends back the current message that is set in the users DB
# use the @token_required annotation for anything you need to be locked for non-logged in users
@app.route('/getUserMessage', methods=['GET'])
@token_required
def get_user_message(current_user):
    # current user is passed in by the JWT verification
    print("this is meant to priunt current user")
    print(current_user)

    return 'This will return the json version of the user message'


# this doesn't work but I'm not sure why
# just use flask run
if __name__ == "__main__":
    app.run(debug=True)