from flask import Flask, request, jsonify
import google.generativeai as genai
import smtplib
from email.message import EmailMessage
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask_cors import CORS
GEMENI_API_KEY=AIzaSyBNw-incZieEgwAySBDZtkV54zgL3U13Oo
load_dotenv()
app = Flask(__name__)
api=os.getenv('GEMENI_API_KEY')

CORS(app)  #

# Configure Gemini API
genai.configure(api_key=api)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["shoe_shop"]
stock_collection = db["stock"]

# Function to get AI response
def chatbot_response(user_input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_input)
    return response.text

# Function to send an email
def send_email(to_email, order_details):
    email = EmailMessage()
    email["From"] = "yourshop@example.com"
    email["To"] = to_email
    email["Subject"] = "Shoe Order Confirmation"
    email.set_content(f"Your order details:\n{order_details}")

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login("yourshop@example.com", "yourpassword")
        smtp.send_message(email)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")  # Use .get() to avoid KeyError
    if not user_message:
        return jsonify({"error": "No message provided"}), 400  # Return a proper error response

    bot_reply = chatbot_response(user_message)
    return jsonify({"response": bot_reply})

@app.route("/order", methods=["POST"])
def order():
    data = request.json
    shoe = data["shoe"]
    size = data["size"]
    email = data["email"]

    stock_item = stock_collection.find_one({"name": shoe})

    if stock_item and size in stock_item["sizes"] and stock_item["stock"] > 0:
        stock_collection.update_one({"name": shoe}, {"$inc": {"stock": -1}})
        order_details = f"Shoe: {shoe}, Size: {size}, Price: {stock_item['price']}"
        send_email(email, order_details)
        return jsonify({"message": "Order placed successfully, confirmation email sent!"})
    return jsonify({"message": "Out of stock or invalid request."}), 400

if __name__ == "__main__":
    app.run(debug=True)
