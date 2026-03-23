from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
SAVE_DIR = "submissions"

os.makedirs(SAVE_DIR, exist_ok=True)


def normalize_dob_fields(data):
    dob_value = data.get("dob")
    if not isinstance(dob_value, str):
        return data

    try:
        parsed_dob = datetime.strptime(dob_value, "%Y-%m-%d")
    except ValueError:
        return data

    normalized = dict(data)
    normalized.setdefault("dobIso", dob_value)
    normalized["dob"] = parsed_dob.strftime("%m/%d/%Y")
    return normalized

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400

    data = normalize_dob_fields(data)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{data.get('firstName', 'unknown')}_{data.get('lastName', 'unknown')}_{timestamp}.json"
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    return jsonify({"status": "success", "saved": filename}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
