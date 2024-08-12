from flask import Blueprint, jsonify, request
from Models import Order, OrderItem, Product, db
from Auth.utils import token_required

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add-to-cart', methods=['POST'])
@token_required
def add_to_cart(current_user):
    try:
        product_info = request.get_json()
        product_id = product_info.get('product_id')
        quantity = product_info.get('quantity')

        # Retrieve product and calculate the price
        product = Product.query.get(product_id)
        # Return an error if the products doesnt exist
        if not product:
            return jsonify({'message': 'Product not found', 'success': False}), 404

        price = product.price
        total_price = price * quantity

        # Find the user's existing pending order or create a new one
        existing_order = Order.query.filter_by(user_id=current_user.id, status='pending').first()

        if not existing_order:
            new_order = Order(user_id=current_user.id, total_price=total_price)
            db.session.add(new_order)
            db.session.flush()
            order_id = new_order.id
        else:
            new_order = existing_order
            new_order.total_price += total_price
            order_id = new_order.id

        # Check if the product is already in the order
        existing_item = OrderItem.query.filter_by(order_id=order_id, product_id=product_id).first()
        if existing_item:
            existing_item.quantity += quantity
            existing_item.price = product.price * existing_item.quantity
        else:
            new_item = OrderItem(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity,
                price=total_price
            )
            db.session.add(new_item)

        db.session.commit()

        return jsonify({'message': 'Item added successfully', 'success': True})

    except Exception as e:
        # Rollback any changes in case of an error
        db.session.rollback()
        print(f"An error occurred: {str(e)}")
        return jsonify({'message': 'An error occurred.', 'success': False}), 500
    
@cart_bp.route('/cart', methods=['GET'])
@token_required
def get_cart(current_user):
    try:
        order = Order.query.filter_by(user_id=current_user.id, status='pending').first()

        if not order:
            return jsonify({'message': 'No pending orders found.', 'success': False}), 404

        order_items = OrderItem.query.filter_by(order_id=order.id).all()

        # Get all product_ids to fetch them in one go
        product_ids = [order_item.product_id for order_item in order_items]
        products = Product.query.filter(Product.id.in_(product_ids)).all()

        # Map products by their id for quick access
        product_map = {product.id: product for product in products}

        # Construct the order items list
        order_items_list = [
            {
                'order_id': order_item.id,
                'quantity': order_item.quantity,
                'price': order_item.price,
                'created_at': order_item.created_at,
                'products_information': {
                    'product_name': product_map[order_item.product_id].name,
                    'description': product_map[order_item.product_id].description,
                    'price': product_map[order_item.product_id].price,
                    'image_url': product_map[order_item.product_id].image_url
                }
            }
            for order_item in order_items
        ]

        return jsonify({'success': True, 'order_items': order_items_list})
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'message': 'An error occurred.', 'success': False}), 500