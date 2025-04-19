from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Secure values from Replit secrets
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
TABLE_NAME = os.environ.get("AIRTABLE_TABLE_NAME", "Multi-Channel Flow")

@app.route("/send-to-airtable", methods=["POST"])
def send_to_airtable():
    data = request.json

    title = data.get("title", "")
    core_message = data.get("core_message", "")
    trigger_ai = data.get("trigger_ai", "")

    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME.replace(' ', '%20')}"

    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "fields": {
            "Title": title,
            "Core Message": core_message,
            "Trigger AI": trigger_ai
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code in [200, 201]:
        return jsonify({"success": True, "message": "Content sent to Airtable"}), 200
    else:
        return jsonify({"success": False, "error": response.text}), response.status_code

@app.route("/", methods=["GET"])
def index():
    return "Airtable Action API is live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
