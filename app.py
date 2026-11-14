from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/producten")
def products():
    return render_template("products.html")
@app.route("/location", methods=["POST"])
def location():
    data = request.get_json(silent=True)

    if not data or data.get("consent") is not True:
        return jsonify({"error": "Toestemming vereist"}), 400

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return jsonify({"error": "Locatie ontbreekt"}), 400

    app.logger.info("Locatie vrijwillig gedeeld")
    app.logger.info("Tijd: %s", datetime.now(timezone.utc).isoformat())
    app.logger.info("Latitude: %s", latitude)
    app.logger.info("Longitude: %s", longitude)

    return jsonify({"message": "Locatie ontvangen"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
