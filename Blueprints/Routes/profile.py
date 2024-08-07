from flask import Blueprint, jsonify, request, make_response
from Models import User
from Auth.utils import token_required


profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    try:
        return jsonify({
            'email': current_user.email,
            'username': current_user.username,
            'created_at': current_user.created_at
        }), 200
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'message': 'An error occurred.', 'success': False}), 500