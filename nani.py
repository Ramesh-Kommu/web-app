from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for the entire app or specific routes
CORS(app)  # This will enable CORS for all routes in your Flask app

# If you want to be more restrictive and only allow certain origins, you can use:
# CORS(app, resources={r"/log": {"origins": "http://yourfrontenddomain.com"}})

@app.route('/')
def home():
    return "Welcome to the Flask API!"

# Define the /log route to handle POST requests
@app.route('/log', methods=['POST'])
def log_user_query():
    data = request.get_json()  # Get the JSON data sent by the frontend
    username = data.get('username')
    query = data.get('query')
    response = data.get('response')
    timestamp = data.get('timestamp')

    # Print the log data to the console (you can save it to a file or database if needed)
    print(f"Log - {timestamp}: {username} queried {query}, got response {response}")

    # Return a response back to the frontend
    return jsonify({'status': 'success', 'timestamp': timestamp})

# Handle the preflight OPTIONS request for CORS
@app.route('/log', methods=['OPTIONS'])
def options_log():
    response = jsonify({'status': 'success'})
    # Add necessary headers for CORS preflight handling
    response.headers.add('Access-Control-Allow-Origin', '*')  # Allow any origin
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')  # Allow POST and OPTIONS methods
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')  # Allow the Content-Type header
    return response

if __name__ == '__main__':
    # Run the Flask app, making sure it's accessible on all network interfaces
    app.run(debug=True, host='0.0.0.0', port=5000)
