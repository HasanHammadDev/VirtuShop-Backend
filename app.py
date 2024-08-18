from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from Models import db
from flask_cors import CORS
from Blueprints.Routes.products import products_bp
from Blueprints.Routes.register import register_bp
from Blueprints.Routes.login import login_bp
from Blueprints.Routes.logout import logout_bp
from Blueprints.Routes.profile import profile_bp
from Blueprints.Routes.cart import cart_bp
from Blueprints.Routes.reviews import reviews_bp


load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

app.register_blueprint(products_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(reviews_bp)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)