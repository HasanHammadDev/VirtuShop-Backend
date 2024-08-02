from flask import Blueprint, jsonify, request
from Models import User
from werkzeug.security import generate_password_hash
from Models import db


register_bp = Blueprint('user', __name__)

@register_bp.route('/register', methods=['POST'])
def register_user():
    try:
        user = request.get_json()
        username = user.get('username')
        password = user.get('password')
        email = user.get('email')

        if not username or not password or not email:
            return jsonify({'message': 'All fields must be filled.', 'success': False}), 400
        
        #Check if user is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'Registration Failed.', 'success': False}), 409
        
        # Hash the password before registering it into the db
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User Registered Successfully!', 'success': True}), 201
    except Exception as e:
        # Handle errors (such as database errors)
        db.session.rollback()  # Roll back any changes if an error occurs
        return jsonify({'message': 'An error occurred.', 'error': str(e), 'success': False}), 500
        



    