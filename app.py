from flask import Flask, request, jsonify
import datetime
import requests
import json
from flask_cors import CORS
from pushbullet import Pushbullet

app = Flask(__name__)

CORS(app)
pb = Pushbullet("o.OkjPtZACM36L86Nzlr6cRGIY5SVB3ZXca")
# Splunk HEC URL and token


@app.route('/')
def home():
    return "Welcome to the Flask API!s"

# API endpoint to handle user logs
@app.route('/log', methods=['POST'])
def log_user_query():
    data = request.get_json()  # Get the data sent by the frontend
    username = data.get('username')
    query = data.get('query')
    response = data.get('response')
    timestamp = data.get('timestamp')
    header=username+"-"+query
    pb.push_note(header, query)
    print(f"Log - {timestamp}: {username} queried {query}, got response {response}")
    
    # Prepare the log data for Splunk
    log_data = {
        "event": {
            "timestamp": timestamp,
            "username": username,
            "query": query,
            "response": response
        }
    }

    # Send log to Splunk using the HEC API
    print("Sending log data to Splunk...")
    try:
        response = requests.post(SPLUNK_HEC_URL, headers={
            "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}",
            "Content-Type": "application/json"
        }, data=json.dumps(log_data))

        # Capture the response from Splunk
        splunk_response = {
            "status_code": response.status_code,
            "response_text": response.text
        }

        # Check if Splunk received the log successfully
        if response.status_code in [200, 201]:
            print("Log successfully sent to Splunk")
        else:
            print(f"Failed to send log to Splunk. Status code: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.RequestException as e:
        splunk_response = {
            "status_code": 500,
            "response_text": f"Error sending log to Splunk: {e}"
        }

    # Respond back to the frontend with Splunk's response
    return jsonify({
        'status': 'success',
        'timestamp': timestamp,
        'splunk_response': splunk_response
    })

if __name__ == '__main__':
    app.run(debug=True)
