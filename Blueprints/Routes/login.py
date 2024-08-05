from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
import jwt
import datetime
from Models import User, db
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/login', methods=['POST'])
def login():
    try:
        login_info = request.get_json()
        email = login_info.get('email')
        password = login_info.get('password')
        
        #Check if email or password is missing
        if not email or not password:
            return jsonify({'message': 'All fields must be filled.', 'success': False}), 400
        user = User.query.filter(email).first()
        if user and check_password_hash(user.password, password):
            # Generate JWT token
            token = jwt.encode(
                {
                    'sub': user.id,
                    'iat': datetime.datetime.utcnow(),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
                },
                os.getenv('JWT_SECRET_KEY'),
                algorithm='HS256'
            )
            return jsonify({'message': 'Login Successful', 'token': token, 'success': True}), 200
        
        return jsonify({'message': 'Login Failed', 'success': False}), 401
    except Exception as e:
        return jsonify({'message': 'An error occurred.', 'success': False}), 500