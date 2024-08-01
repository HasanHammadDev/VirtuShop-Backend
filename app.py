from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from Models import db, User, Product, Order, OrderItem, Review
from flask_cors import CORS
from Blueprints.Routes.products import products_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

app.register_blueprint(products_bp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)