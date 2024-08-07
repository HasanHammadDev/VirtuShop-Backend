from flask import Blueprint, jsonify, request, make_response
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta, UTC
from Models import User
from dotenv import load_dotenv
import os
from Auth.utils import token_required

load_dotenv()

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    try:
        # Check if the request is in JSON format
        if not request.is_json:
            return jsonify({'message': 'Missing JSON in request', 'success': False}), 400
        
        login_info = request.get_json()
        email = login_info.get('email')
        password = login_info.get('password')
        
        # Check if email or password is missing
        if not email or not password:
            return jsonify({'message': 'All fields must be filled.', 'success': False}), 400

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Generate JWT token
            token = jwt.encode(
                {
                    'sub': user.id,
                    'iat': datetime.now(UTC),
                    'exp': datetime.now(UTC) + timedelta(days=1)
                },
                os.getenv('JWT_SECRET_KEY'),
                algorithm='HS256'
            )
            # Set token in an httpOnly cookie
            response = make_response(jsonify({'message': 'Login Successful', 'success': True}), 200)
            response.set_cookie('token', token, httponly=True, secure=True, samesite='Lax')
            return response, 200
        
        return jsonify({'message': 'Login Failed', 'success': False}), 401
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'message': 'An error occurred.', 'success': False}), 500
    
@login_bp.route('/validate-token', methods=['GET'])
@token_required
def validate_token(current_user):
    try:
        return jsonify({'message': 'Token validated','success': True})
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'message': 'Token was not validated', 'success': False})