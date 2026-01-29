from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)  # enables CORS for all routes

ATTENDANCE_FILE = "attendance.csv"

# Create CSV with headers if it doesn't exist
if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Status"])

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    # Avoid duplicate registration
    with open(ATTENDANCE_FILE, "r") as f:
        existing_names = [row[0] for row in csv.reader(f)]
    if name in existing_names:
        return jsonify({"error": f"{name} is already registered"}), 400

    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, "Registered"])
    return jsonify({"message": f"{name} registered successfully"})

@app.route("/attendance", methods=["POST"])
def attendance():
    data = request.json
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, "Present"])
    return jsonify({"message": f"Attendance marked for {name}"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
