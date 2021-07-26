from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import datetime
import jwt

app = Flask(__name__)
app.debug = True
app.secret_key = b"'`D\x96\xf3m\xeb\x01b\x11\xb5\x05\x14S\x96\xbd"
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['UPLOAD_FOLDER'] = 'uploads'
bcrypt = Bcrypt(app)
client = MongoClient('mongodb://admin:password@mongodb')
db = client.webapp

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms=["HS256"])
    is_blacklisted_token = check_blacklist(auth_token)
    if is_blacklisted_token:
        return 'Token blacklisted. Please log in again.'
    else:
        return payload['sub']


def check_blacklist(auth_token):
    res = db.blacklistTokens.find_one({"token" : str(auth_token)})
    if res:
        return True  
    else:
        return False

def remove_blacklist(auth_token):
    db.blacklistTokens.delete_many({"token": str(auth_token)})



class User:

    user_idx = 1

    def register(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        r_id = post_data.get('id', '')
        r_name = post_data.get('name', '')
        r_password = post_data.get('password', '')
        user = db.users.find_one({"id": r_id})
        
        if not user:
            try:
                r_pw = bcrypt.generate_password_hash(r_password).decode('utf-8')
                user = {
                    "user_idx": User.user_idx, # token에 넣을 user_idx
                    "name": r_name,
                    "id": r_id,
                    "password": r_pw
                }
                User.user_idx += 1
                # insert the user
                db.users.insert_one(user)
                # generate the auth token
                auth_token = encode_auth_token(user['user_idx'])
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.'
            }
            return make_response(jsonify(responseObject)), 202

    def login(self):
        # get the post data
        post_data = request.get_json()
        try:
            r_id = post_data.get('id', '')
            r_password = post_data.get('password', '')
            # fetch the user data
            user = db.users.find_one({"id": r_id})
            if user and bcrypt.check_password_hash(user['password'], r_password):
                auth_token = encode_auth_token(user['user_idx'])
                if auth_token:
                    remove_blacklist(auth_token) # 블랙리스트에서 삭제
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500

    def checkAuth(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = db.users.find_one({"user_idx": resp})
                if user:
                    responseObject = {
                        'status': 'success',
                        'data': {
                            'name': user['name'],
                            'id': user['id']
                        }
                    }
                return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401

    def logout(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token) 
            if not isinstance(resp, str):
            # if db.users.find_one({"user_idx": resp}):
                # mark the token as blacklisted
                try:
                    # insert the token
                    db.blacklistTokens.insert_one({"token": str(auth_token)})
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403
