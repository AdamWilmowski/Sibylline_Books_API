from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask import jsonify
from blocklist import BLOCKLIST
from functools import wraps
from flask import request, jsonify
from instance.secrets import VALID_API_KEYS


def require_api_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('API-Key')
        if api_key and api_key in VALID_API_KEYS:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized"}), 401

    return decorated_function


def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401


def invalid_token_callback(error):
    return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401


def missing_token_callback(error):
    return jsonify({"description": "Request does not contain an access token.", "error": "authorization_required"}), 401


def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"description": "The token has been revoked.", "error": "token_revoked"}), 401
