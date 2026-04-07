from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Replace with your MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://PratikON:h2datasend@h2data.laizkto.mongodb.net/?appName=H2Data"
client = MongoClient(MONGO_URI)

db = client["esp32_data"]
collection = db["adc_readings"]

@app.post("/reading")
def reading():
    data = request.get_json(force=True)

    doc = {
        "device": data.get("device", "esp32"),
        "time": data.get("time"),
        "adc_raw": int(data.get("adc_raw", 0)),
        "created_at": datetime.utcnow()
    }

    collection.insert_one(doc)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)