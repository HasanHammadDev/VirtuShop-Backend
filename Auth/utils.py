from functools import wraps
from flask import request, jsonify
import jwt
from Models import User
import os

SECRET_KEY = os.getenv('JWT_SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check for token in cookies
        if 'token' in request.cookies:
            token = request.cookies.get('token')

        if not token:
            return jsonify({'message': 'Token is missing!', 'success': False}), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['sub']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Authorization Failed', 'success': False}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Authorization Failed', 'success': False}), 401
        except Exception as e:
            return jsonify({'message': f'An error occurred: {str(e)}', 'success': False}), 500

        return f(current_user, *args, **kwargs)
    return decorated