from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
SAVE_DIR = "submissions"

os.makedirs(SAVE_DIR, exist_ok=True)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{data.get('firstName', 'unknown')}_{data.get('lastName', 'unknown')}_{timestamp}.json"
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    return jsonify({"status": "success", "saved": filename}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
