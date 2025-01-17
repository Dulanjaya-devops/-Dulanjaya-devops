from flask import Flask, request, jsonify, send_from_directory, send_file
from pymongo import MongoClient
from openpyxl import Workbook
from datetime import datetime, timedelta
import os

app = Flask(__name__, static_folder="frontend")

# MongoDB connection details
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URI)
db = client["it_equipment"]
collection = db["warranties"]

# Serve the frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

# API endpoint to add warranty
@app.route('/add_warranty', methods=['POST'])
def add_warranty():
    data = request.json

    # Validate required fields
    if not all(key in data for key in ('equipment_id', 'equipment_name', 'warranty_period', 'purchase_date')):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Convert purchase_date to a datetime object
        purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Calculate warranty expiration date
    warranty_period_days = int(data['warranty_period']) * 365
    expiration_date = purchase_date + timedelta(days=warranty_period_days)

    # Prepare the record for insertion
    warranty_record = {
        "equipment_id": data['equipment_id'],
        "equipment_name": data['equipment_name'],
        "warranty_period": data['warranty_period'],
        "purchase_date": data['purchase_date'],
        "expiration_date": expiration_date.strftime('%Y-%m-%d')
    }

    collection.insert_one(warranty_record)
    return jsonify({"message": "Warranty added successfully", "data": warranty_record}), 201

# API endpoint to list warranties
@app.route('/list_warranties', methods=['GET'])
def list_warranties():
    warranties = list(collection.find({}, {"_id": 1, "equipment_id": 1, "equipment_name": 1, "warranty_period": 1, "purchase_date": 1, "expiration_date": 1}))
    for warranty in warranties:
        warranty["_id"] = str(warranty["_id"])  # Convert ObjectId to string for JSON serialization
    return jsonify({"warranties": warranties})

# API endpoint to update warranty
@app.route('/update_warranty/<warranty_id>', methods=['PUT'])
def update_warranty(warranty_id):
    data = request.json

    try:
        # Update warranty details
        collection.update_one({"_id": ObjectId(warranty_id)}, {"$set": data})
        return jsonify({"message": "Warranty updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# API endpoint to delete warranty
@app.route('/delete_warranty/<warranty_id>', methods=['DELETE'])
def delete_warranty(warranty_id):
    try:
        collection.delete_one({"_id": ObjectId(warranty_id)})
        return jsonify({"message": "Warranty deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
