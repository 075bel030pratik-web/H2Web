from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Replace with your MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://PratikON:h2datasend@h2data.laizkto.mongodb.net/?appName=H2Data"
client = MongoClient(MONGO_URI)

db = client["esp32_data"]
collection = db["adc_readings"]

@app.route("/")
def home():
    return "Server running"


@app.post("/reading")
def reading():
    data = request.get_json(force=True)

    device = data.get("device", "unknown")
    batch_time = data.get("batch_time")
    samples = data.get("samples", [])

    docs = []
    for s in samples:
        docs.append({
            "device": device,
            "batch_time": batch_time,
            "time": s.get("time"),
            "adc_raw": int(s.get("adc_raw", 0)),
            "created_at": datetime.utcnow()
        })

    if docs:
        collection.insert_many(docs)

    return jsonify({"ok": True, "inserted": len(docs)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)