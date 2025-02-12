from flask import Flask, request, jsonify
import google.generativeai as genai
import smtplib
from email.message import EmailMessage
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key from environment variable
api = os.getenv('GEMENI_API_KEY')

CORS(app)  # Enable CORS for all routes

# Configure Gemini API
genai.configure(api_key=api)

# Connect to MongoDB (commented out for now)
# client = MongoClient("mongodb://localhost:27017")
# db = client["shoe_shop"]
# stock_collection = db["stock"]

# Function to get AI response
def chatbot_response(user_input):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return str(e)  # Return error message if API call fails

# # Function to send an email (commented out)
# def send_email(to_email, order_details):
#     email = EmailMessage()
#     email["From"] = "yourshop@example.com"
#     email["To"] = to_email
#     email["Subject"] = "Shoe Order Confirmation"
#     email.set_content(f"Your order details:\n{order_details}")

#     with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
#         smtp.starttls()
#         smtp.login("yourshop@example.com", "yourpassword")
#         smtp.send_message(email)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")  # Use .get() to avoid KeyError
    if not user_message:
        return jsonify({"error": "No message provided"}), 400  # Return a proper error response

    bot_reply = chatbot_response(user_message)
    return jsonify({"response": bot_reply})

# @app.route("/order", methods=["POST"])  # Uncomment this for order functionality
# def order():
#     data = request.json
#     shoe = data["shoe"]
#     size = data["size"]
#     email = data["email"]
#     # Handle stock and order logic
#     return jsonify({"message": "Order placed successfully, confirmation email sent!"})

if __name__ == "__main__":
    app.run(debug=True)  # This line is for local development only.
