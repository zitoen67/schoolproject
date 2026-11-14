from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.before_request
def log_request():
    if request.method == "GET":
        with open("data.txt", "a", encoding="utf-8") as file:
            file.write(
                f"\nTijd: {datetime.now()}\n"
                f"Pagina: {request.path}\n"
            )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/location", methods=["POST"])
def location():
    data = request.get_json()

    if not data or data.get("consent") is not True:
        return {"error": "Toestemming vereist"}, 400

    with open("data.txt", "a", encoding="utf-8") as file:
        file.write(
            f"\nLocatie met toestemming ontvangen\n"
            f"ID: {data.get('session_id')}\n"
            f"Latitude: {data.get('latitude')}\n"
            f"Longitude: {data.get('longitude')}\n"
        )

    return {"message": "Opgeslagen"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
