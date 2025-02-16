from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

CORS(app)


@app.route('/log', methods=['POST'])
def log_user_query():
    data = request.get_json()
    # Your code to process the data
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True)
