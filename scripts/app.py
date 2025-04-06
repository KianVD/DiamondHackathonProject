from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # Importing CORS
import random
from functools import wraps
import importlib.util
import sys
from predictFromUploaded import make_preds
from gemini_functions import generate_concise_report
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import json


# Load environment variables from .env file
load_dotenv()
# Now you can use the module as follows

app = Flask(__name__)

# Enable CORS for all domains (for development purposes, use specific domains in production)
CORS(app)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'  # You can change this to any path you prefer
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'zip'}

# Make sure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return jsonify({'message': 'File uploaded successfully', 'filename': file.filename}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/random-status', methods=['GET'])
def random_status():
    # Return a random status: "less", "medium", or "high"
    status = make_preds()
    return jsonify({'status': status.split(' ')[0].lower()})



def verify_token(token):
    auth0_domain = os.getenv("AUTH_DOMAIN")  # Example: 'dev-xxxxx.auth0.com'
    auth0_api_identifier = os.getenv("API_IDENTIFIER")
    auth0_url = f'https://{auth0_domain}/userinfo'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Sending a GET request to Auth0's userinfo endpoint to verify the token
    response = requests.get(auth0_url, headers=headers)
    if response.status_code == 200:
        return response.json()  # The user information if the token is valid
    return None  # If invalid token

# A decorator to check if the user is authenticated before accessing the route
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Try to get the token from the Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        # Verify token and check its validity
        user = verify_token(token)
        if not user:
            return jsonify({"message": "Token is invalid or expired!"}), 403

        return f(*args, **kwargs)

    return decorated_function

@app.route('/download', methods=['GET'])
@token_required
def download_file():
    try:
        # Path to the file to be downloaded
        file_name = 'concise_credit_risk_report.pdf'  # Example: 'file.pdf'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)

        return jsonify({"message": "File not found!"}), 404

    except Exception as e:
        return jsonify({"message": f"Error downloading file: {str(e)}"}), 500

@app.route('/generate-report', methods=['GET'])
def generate_report():
    try:
        # Load user data from JSON file
        with open('new_user_features.json', 'r') as file:
            user_data = json.load(file)
        
        # Generate the concise report (this function should handle generating the PDF or any other report internally)
        generate_concise_report(user_data)
        
        # Return a JSON response indicating success
        return jsonify({
            "message": "Concise credit risk report generated successfully."
        }), 200
    except FileNotFoundError:
        return jsonify({
            "error": "The user data file was not found."
        }), 404
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
