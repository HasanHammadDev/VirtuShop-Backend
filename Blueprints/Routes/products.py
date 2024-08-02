from flask import Blueprint, jsonify, request
from Models import Product
from sqlalchemy.exc import SQLAlchemyError

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        products_list = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "category": product.category,
                "imageUrl": product.image_url,
                "created_at": product.created_at.isoformat()
            }
            for product in products
        ]
        return jsonify(products_list), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500

@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({"error": "Product Not Found"}), 404
        
        product_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "category": product.category,
            "imageUrl": product.image_url,
            "created_at": product.created_at.isoformat()
        }
        return jsonify(product_data), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500