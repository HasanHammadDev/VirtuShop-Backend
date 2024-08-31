from collections import defaultdict
from flask import Blueprint, jsonify, request
from Models import Product, Review
from sqlalchemy.exc import SQLAlchemyError

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        reviews = Review.query.all()
        
        # Create a dictionary to store all ratings per product
        product_reviews = defaultdict(list)
        
        # Populate the product_reviews dictionary
        for review in reviews:
            product_reviews[review.product_id].append(review.rating)
        
        # Prepare the product list with ratings
        products_list = []
        for product in products:
            ratings = product_reviews[product.id]
            total_rating = sum(ratings)
            average_rating = total_rating / len(ratings) if ratings else 0
            
            products_list.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "category": product.category,
                "imageUrl": product.image_url,
                "created_at": product.created_at.isoformat(),
                "rating": round(average_rating, 2),
                "isOnSale": product.on_sale,
                "salePrice": str(product.sale_price) if product.sale_price else None
            })
        return jsonify(products_list), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500

@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    try:
        # Fetch the product
        product = Product.query.get(id)
        
        # Check if the product exists
        if not product:
            return jsonify({"error": "Product Not Found"}), 404

        # Fetch product reviews
        product_reviews = Review.query.filter_by(product_id=id).all()

        total_rating = sum(review.rating for review in product_reviews)
        product_rating = total_rating / len(product_reviews) if product_reviews else 0
        
        product_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "category": product.category,
            "imageUrl": product.image_url,
            "created_at": product.created_at.isoformat(),
            "rating": product_rating,
            "isOnSale": product.on_sale,
            "salePrice": product.sale_price
        }
        return jsonify(product_data), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500
