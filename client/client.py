import os
import requests
import logging
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# HTML template for the web form
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ASCII Art Client</title>
</head>
<body>
    <h1>ASCII Art Generator</h1>
    <form method="get" action="/convert">
        <label for="sentence">Enter a sentence:</label>
        <input type="text" id="sentence" name="sentence" required>
        <button type="submit">Convert to ASCII Art</button>
    </form>
    {% if ascii_art %}
        <h2>ASCII Art:</h2>
        <pre>{{ ascii_art }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    # Serve the HTML form
    return render_template_string(HTML_TEMPLATE)

@app.route("/convert", methods=["GET"])
def convert_to_ascii():
    # Get the query parameter from the URL
    sentence = request.args.get("sentence", "")
    if not sentence:
        app.logger.error("No sentence provided, aborting...")
        return "No sentence provided!", 400
    app.logger.info(f"got {sentence}, converting to ascii...")
    # Communicate with the server
    server_hostname = os.getenv("SERVER_HOSTNAME")
    server_port = os.getenv("SERVER_PORT")
    server_url = f"http://{server_hostname}:{server_port}/ascii"
    try:
        response = requests.post(server_url, json={"sentence": sentence})
        response.raise_for_status()
        ascii_art = response.json().get("ascii_art", "No ASCII art returned.")
    except requests.RequestException as e:
        logger.error(f"Error connecting to server: {e}")
        ascii_art = f"Error connecting to server: {e}"
        return ascii_art,500
    app.logger.info("rendering response")
    # Render the form again with the ASCII art result
    return render_template_string(HTML_TEMPLATE, ascii_art=ascii_art)

if __name__ == "__main__":
    client_port = int(os.getenv("CLIENT_PORT", 5001))
    app.run(host="0.0.0.0", port=client_port)
