from flask import Flask, request, jsonify
from datetime import datetime, timezone
import uuid

app = Flask(__name__)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Metro Mock Payment API",
        "status": "RUNNING",
        "message": "Metro Payment API is online"
    }), 200


# ---------------------------------------------------------
# Payment API
# ---------------------------------------------------------
@app.route("/api/payment", methods=["POST"])
def process_payment():

    # Get JSON request body
    data = request.get_json(silent=True)

    # Check if request body is missing or invalid
    if not data:
        return jsonify({
            "success": False,
            "status": "FAILED",
            "message": "Request body is missing"
        }), 400

    # Get payment details
    booking_number = data.get("booking_number")
    amount = data.get("amount")
    payment_method = data.get("payment_method")

    # Check required fields
    if not booking_number or amount is None or not payment_method:
        return jsonify({
            "success": False,
            "status": "FAILED",
            "message": "Missing required payment information"
        }), 400

    # Validate amount
    if (
        isinstance(amount, bool)
        or not isinstance(amount, (int, float))
        or amount <= 0
    ):
        return jsonify({
            "success": False,
            "status": "FAILED",
            "message": "Amount must be greater than 0"
        }), 400

    # Generate mock transaction ID
    transaction_id = "MOCK-" + uuid.uuid4().hex[:10].upper()

    # Generate transaction timestamp
    transaction_date = datetime.now(timezone.utc).isoformat()

    # Simulated successful payment
    return jsonify({
        "success": True,
        "status": "SUCCESS",
        "transaction_id": transaction_id,
        "booking_number": booking_number,
        "amount": amount,
        "payment_method": payment_method,
        "transaction_date": transaction_date
    }), 200


# ---------------------------------------------------------
# Local Development Server
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )