from flask import Flask, render_template, request, jsonify, abort

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
        "Historische pistoolpresentatie",
        "Vintage pistooldisplay",
        "Pistoolmuseumdisplay",
        "Historische wapenillustratie",
        "Pistoolwanddecoratie",
        "Militaire geschiedenisprint",
        "Historische collectiepresentatie",
        "Pistoolvormige decoratie",
    ],
    "Messen": [
        "Victorinox Swiss Army Knife",
        "Opinel No. 8",
        "Wüsthof Classic Chef's Knife",
        "Leatherman Wave+",
        "Morakniv Companion",
        "Buck 110 Heritage Display",
        "Spyderco Design Display",
        "Historische messenprint",
    ],
    "Kogels": [
        "9mm munitiegeschiedenisprint",
        ".22 kaliber geschiedenisdisplay",
        "5.56 NATO geschiedenisprint",
        "7.62 kaliber museumdisplay",
        ".45 ACP geschiedenisprint",
        "12 Gauge geschiedenisdisplay",
        "Historische munitieposter",
        "Munitiecollectie presentatie",
    ],
    "Boksbeugels": [
        "Historische boksbeugelillustratie",
        "Boksbeugel museumdisplay",
        "Vintage vechtsportposter",
        "Historische vechtsportprint",
        "Metalen vechtsportdecoratie",
        "Underground designprint",
        "Historische collectieposter",
        "Vechtsport wanddecoratie",
    ],
    "Pistoolmagazijnen": [
        "Historische magazijnillustratie",
        "Magazijn museumdisplay",
        "Vintage wapenonderdelenposter",
        "Historische onderdelenprint",
        "Militaire geschiedenisdisplay",
        "Wapenhistorie wanddecoratie",
        "Technische onderdelenillustratie",
        "Historische collectieposter",
    ],
    "Bommen": [
        "Historische Mills-granaat illustratie",
        "Stielhandgranate museumprint",
        "Historische Tallboy-poster",
        "Little Boy geschiedenisprint",
        "Fat Man geschiedenisprint",
        "Tsar Bomba informatieposter",
        "MOAB geschiedenisillustratie",
        "Historische luchtvaartposter",
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
                f"{product_name} — onderdeel van de D-WEB collectie. "
                "Een historisch geïnspireerd decoratief object "
                "voor liefhebbers van geschiedenis en industrieel design."
            ),
            "image": (
                f"/static/images/products/product_{product_id:02d}.jpg"
            ),
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
        return jsonify({
            "error": "Geen bestelgegevens ontvangen"
        }), 400

    required = [
        "name", "address", "city",
        "email", "paymentMethod", "items"
    ]

    if any(not data.get(field) for field in required):
        return jsonify({
            "error": "Vul alle verplichte gegevens in"
        }), 400

    if not isinstance(data["items"], list) or not data["items"]:
        return jsonify({
            "error": "Je winkelmand is leeg"
        }), 400

    return jsonify({
        "message": "Je demo-bestelling is ontvangen!"
    })


@app.route("/location", methods=["POST"])
def receive_location():
    data = request.get_json(silent=True)

    if not data or data.get("consent") is not True:
        return jsonify({
            "error": "Geen toestemming ontvangen"
        }), 400

    try:
        latitude = float(data.get("latitude"))
        longitude = float(data.get("longitude"))

        if not (-90 <= latitude <= 90 and
                -180 <= longitude <= 180):
            raise ValueError("Ongeldige coördinaten")

    except (TypeError, ValueError):
        return jsonify({
            "error": "Ongeldige locatie"
        }), 400

    app.logger.info(
        "Locatie ontvangen met toestemming: "
        "breedtegraad=%s, lengtegraad=%s",
        latitude,
        longitude
    )

    return jsonify({
        "message": "Locatie ontvangen"
    }), 200


@app.errorhandler(404)
def page_not_found(error):
    return "Deze pagina bestaat niet.", 404


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
