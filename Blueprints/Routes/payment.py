from flask import Blueprint, jsonify, request
from Auth.utils import token_required
import stripe, os
import logging

payment_bp = Blueprint('payment', __name__)

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@payment_bp.route('/create-payment-intent', methods=['POST'])
@token_required
def create_payment(current_user):
    try:
        data = request.json
        amount = data.get('amount')
        currency = data.get('currency', 'usd')

        if not amount or float(amount) <= 0:
            return jsonify(error="Invalid payment amount"), 400

        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(float(amount) * 100),  # Stripe expects amount in cents
            currency=currency,
            automatic_payment_methods={
                'enabled': True,
            },
        )

        return jsonify({
            'clientSecret': intent.client_secret
        })

    except Exception as e:
        logging.error(f"Payment intent creation failed: {str(e)}")
        return jsonify(error="Payment intent creation failed"), 403