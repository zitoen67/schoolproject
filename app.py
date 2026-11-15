from flask import Flask, render_template, request, jsonify, abort
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os
app = Flask(__name__)

categories = [
    {"name": "Pistolen", "slug": "Pistolen"},
    {"name": "Messen", "slug": "Messen"},
    {"name": "Kogels", "slug": "Kogels"},
    {"name": "Boksbeugels", "slug": "Boksbeugels"},
    {"name": "Pistoolmagazijnen", "slug": "Pistoolmagazijnen"},
    {"name": "Bommen", "slug": "Bommen"},
]

product_names = {
    "Pistolen": [
        "Glock 17 - historische documentatie",
        "Beretta 92FS - historische documentatie",
        "Colt M1911 - historische documentatie",
        "Desert Eagle - historische documentatie",
        "SIG Sauer P226 - historische documentatie",
        "Walther PPK - historische documentatie",
        "CZ 75 - historische documentatie",
        "FN Browning Hi-Power - historische documentatie",
    ],
    "Messen": [
        "Victorinox Swiss Army Knife",
        "Opinel No. 8",
        "Wüsthof Classic",
        "Leatherman Wave+",
        "Morakniv Companion",
        "Buck 110",
        "Spyderco Paramilitary 2",
        "KA-BAR historische documentatie",
    ],
    "Kogels": [
        "9×19mm Parabellum - geschiedenis",
        ".22 Long Rifle - geschiedenis",
        "5.56×45mm NATO - geschiedenis",
        "7.62×39mm - geschiedenis",
        ".45 ACP - geschiedenis",
        "7.62×51mm NATO - geschiedenis",
        "12 Gauge - geschiedenis",
        ".50 BMG - geschiedenis",
    ],
    "Boksbeugels": [
        "Historische boksbeugel - museumillustratie",
        "Klassieke viervingerboksbeugel - geschiedenis",
        "Tweekleurige boksbeugel - museumillustratie",
        "Tekko - historische documentatie",
        "Apache revolver - historische documentatie",
        "Mark I Trench Knife - geschiedenis",
        "Historische vechtsportillustratie",
        "Vechtsportmuseum - collectieprint",
    ],
    "Pistoolmagazijnen": [
        "Glock magazijn - technische illustratie",
        "Beretta 92 magazijn - technische illustratie",
        "Colt M1911 magazijn - technische illustratie",
        "SIG Sauer P226 magazijn - technische illustratie",
        "CZ 75 magazijn - technische illustratie",
        "Walther PPK magazijn - technische illustratie",
        "FN Browning Hi-Power magazijn - technische illustratie",
        "Historische magazijnillustratie",
    ],
    "Bommen": [
        "Mills Bomb - historische documentatie",
        "Stielhandgranate - historische documentatie",
        "Tallboy - historische documentatie",
        "Little Boy - historische documentatie",
        "Fat Man - historische documentatie",
        "Tsar Bomba - historische documentatie",
        "JDAM - historische documentatie",
        "MOAB - historische documentatie",
    ],
}

products = []
product_id = 1

for category_index, category in enumerate(categories):
    category_name = category["name"]

    for number, product_name in enumerate(product_names[category_name]):
        products.append({
            "id": product_id,
            "name": product_name,
            "category": category_name,
            "price": round(9.95 + number * 5 + category_index * 2, 2),
            "description": (
                f"{product_name}. Onderdeel van de D-WEB "
                "historische collectie. Een informatieve "
                "presentatie over geschiedenis en industrieel design."
            ),
            "image": f"/static/images/products/product_{product_id:02d}.jpg",
        })

        product_id += 1


@app.route("/")
def home():
    return render_template("index.html", categories=categories)


@app.route("/producten")
def product_list():
    selected_category = request.args.get("categorie", "")

    filtered_products = products

    if selected_category:
        filtered_products = [
            product for product in products
            if product["category"] == selected_category
        ]

    return render_template(
        "products.html",
        products=filtered_products,
        categories=categories,
        selected_category=selected_category
    )


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next(
        (item for item in products if item["id"] == product_id),
        None
    )

    if product is None:
        abort(404)

    return render_template("product.html", product=product)


@app.route("/afrekenen")
def checkout():
    return render_template("checkout.html")


@app.route("/order", methods=["POST"])
def order():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Geen gegevens ontvangen"}), 400

    required = ["name", "email", "items"]

    if any(not data.get(field) for field in required):
        return jsonify({"error": "Vul alle verplichte gegevens in"}), 400

    if not isinstance(data["items"], list) or not data["items"]:
        return jsonify({"error": "De winkelmand is leeg"}), 400



    order_number = datetime.now().strftime("%Y%m%d%H%M%S")

    message = EmailMessage()
    message["Subject"] = f"D-WEB bestelling {order_number}"
    message["From"] = os.environ.get("SMTP_LOGIN")
    message["To"] = os.environ.get("ADMIN_EMAIL")

    message.set_content(
        f"""
Nieuwe D-WEB bestelling

Bestelnummer: {order_number}
Naam: {data['name']}
E-mailadres: {data['email']}

Producten:
{chr(10).join(str(item) for item in data['items'])}


"""
    )

    try:
        with smtplib.SMTP(
            os.environ.get("SMTP_SERVER"),
            int(os.environ.get("SMTP_PORT", 587))
        ) as server:
            server.starttls()
            server.login(
                os.environ.get("SMTP_LOGIN"),
                os.environ.get("SMTP_PASSWORD")
            )
            server.send_message(message)

    except Exception:
        app.logger.exception("e-mail kon niet worden verstuurd")
        return jsonify({"error": "E-mail versturen is niet gelukt"}), 500

    return jsonify({
        "message": "Je bestelling is ontvangen!",
        "orderNumber": order_number
    })


@app.route("/location", methods=["POST"])
def receive_location():
    data = request.get_json(silent=True)

    if not data or data.get("consent") is not True:
        return jsonify({"error": "Geen toestemming ontvangen"}), 400

    try:
        latitude = float(data.get("latitude"))
        longitude = float(data.get("longitude"))

        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            raise ValueError("Ongeldige coördinaten")

    except (TypeError, ValueError):
        return jsonify({"error": "Ongeldige locatie"}), 400

    app.logger.info(
        "Locatie ontvangen met toestemming: breedtegraad=%s, lengtegraad=%s",
        latitude,
        longitude
    )

    return jsonify({"message": "Locatie ontvangen"}), 200


@app.errorhandler(404)
def page_not_found(error):
    return "Deze pagina bestaat niet.", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
