from flask import Flask, request, jsonify
import subprocess
import logging

app = Flask(__name__)

@app.route('/ascii', methods=['POST'])
def ascii_art():
    # Get the sentence from the client's request
    data = request.get_json()
    sentence = data.get('sentence', '')

    if not sentence:
        app.logger.debug("Received request for ASCII art")
        return jsonify({"error": "No sentence provided"}), 400

    # Generate ASCII art using figlet
    try:
        result = subprocess.run(['figlet', sentence], capture_output=True, text=True, check=True)
        ascii_art = result.stdout
        return jsonify({"ascii_art": ascii_art})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
