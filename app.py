from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from Models.models import db, User, Product, Order, OrderItem, Review
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

@app.route('/products', methods=['GET'])
def get_products():
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

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({'message': 'Product Not Found', }), 404
    
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)