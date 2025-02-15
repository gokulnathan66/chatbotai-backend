from flask import Flask, request, jsonify
import google.generativeai as genai
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask_cors import CORS
from waitress import serve

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key from environment variable
api = os.getenv('GEMENI_API_KEY')
if not api:
    raise ValueError("GEMENI_API_KEY environment variable is not set!")

CORS(app)  # Enable CORS for all routes

# Configure Gemini API
genai.configure(api_key=api)

# Function to get AI response
def chatbot_response(user_input):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return str(e)  # Return error message if API call fails

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")  # Use .get() to avoid KeyError
    if not user_message:
        return jsonify({"error": "No message provided"}), 400  # Return a proper error response

    bot_reply = chatbot_response(user_message)
    return jsonify({"response": bot_reply})

@app.route("/")
def home():
    return jsonify({"message": "Chatbot API is running!"})

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))