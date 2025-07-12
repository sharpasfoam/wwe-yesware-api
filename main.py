from flask import Flask, request, jsonify
import csv
import os
import tempfile
import requests
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return "WWE Yesware CSV Generator is running!"

@app.route("/generate-csv", methods=["POST"])
def generate_csv():
    data = request.get_json()
    contacts = data.get("contacts", [])
    tone = data.get("tone", "friendly")
    message_context = data.get("messageContext", "budget stability")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"yesware_{tone}_{timestamp}.csv"

    message_template = f"""WWE outreach: Tone = {tone.capitalize()}, Context = {message_context.capitalize()}.
This message highlights:
- WWE's Cancel Anytime protection
- Long-term gas rate certainty
- Urgency to act before Nov 1 rate reset
"""

    with tempfile.NamedTemporaryFile(mode='w+', newline='', delete=False, suffix=".csv") as temp_csv:
        writer = csv.writer(temp_csv)
        writer.writerow(["To", "First Name", "Company", "Message"])
        for contact in contacts:
            writer.writerow([
                contact.get("email", ""),
                contact.get("firstName", ""),
                contact.get("company", ""),
                message_template
            ])
        temp_csv_path = temp_csv.name

    with open(temp_csv_path, 'rb') as f:
        response = requests.post("https://file.io/?expires=1d", files={"file": (filename, f)})

    os.remove(temp_csv_path)

    if response.status_code == 200:
        result = response.json()
        return jsonify({
            "downloadUrl": result["link"],
            "message": f"[Download CSV for Yesware ({tone.title()} Tone)]({result['link']})"
        })
    else:
        return jsonify({"error": "Failed to upload file"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
