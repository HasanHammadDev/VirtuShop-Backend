from flask import Blueprint, jsonify, request
from Models import Review, Product, User, db
from Auth.utils import token_required

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/add-review/<int:id>', methods=['POST'])
@token_required
def add_review(current_user, id):
    try:
        review_info = request.get_json()
        comment = review_info.get('comment')
        rating = review_info.get('rating')
        
        product = Product.query.get(id)
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'})
        
        if not comment or not rating:
            return jsonify({'success': False, 'message': 'Review did not include a rating and/or comment. Please try again!'})
        
        new_review = Review(product_id=id, user_id=current_user.id, rating=rating, comment=comment)
        
        db.session.add(new_review)
        db.session.commit()
        
        return jsonify({'message': 'Review Added Successfully!', 'success': True}), 201
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'message': 'An error occurred.', 'success': False}), 500
    
@reviews_bp.route('/get-product-reviews/<int:id>', methods=['GET'])
@token_required
def get_product_reviews(current_user, id):
    try:
        product = Product.query.get(id)
        
        if not product:
            return jsonify({'message': 'Product not found.', 'success': False}), 404
        
        reviews = Review.query.filter_by(product_id=product.id).all()
        
        reviews_list = []
        for review in reviews:
            user = User.query.get(review.user_id)
            reviews_list.append({
                'id': review.id,
                'username': user.username,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at
            })

        return jsonify({
            'message': 'Product reviews fetched successfully!',
            'success': True,
            'reviews': reviews_list
        }), 200
    except Exception as e:
        print(f"An error occurred while fetching product reviews: {str(e)}")
        return jsonify({'message': 'An error occurred while fetching product reviews.', 'success': False}), 500
        