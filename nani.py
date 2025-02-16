from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow CORS from the frontend app's URL
CORS(app, origins=["https://gray-sky-0a920b310.4.azurestaticapps.net"])

@app.route('/log', methods=['POST'])
def log_user_query():
    # Your existing code
    return jsonify({'status': 'success', 'timestamp': request.json['timestamp']})

if __name__ == '__main__':
    app.run(debug=True)
