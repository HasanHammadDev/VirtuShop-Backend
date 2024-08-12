from flask import Blueprint, jsonify
from Auth.utils import token_required
from Models import Order, OrderItem


profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    try:
        # Fetch the user's pending order
        order = Order.query.filter_by(user_id=current_user.id, status='pending').first()

        # Get the count of order items if an order exists
        item_count = 0
        if order:
            item_count = OrderItem.query.filter_by(order_id=order.id).count()

        return jsonify({
            'email': current_user.email,
            'username': current_user.username,
            'created_at': current_user.created_at,
            'item_count': item_count  # Add the item count to the response
        }), 200
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'message': 'An error occurred.', 'success': False}), 500