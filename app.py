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
        "Glock 17 Display Replica",
        "Beretta 92 Display Replica",
        "Colt 1911 Display Replica",
        "Desert Eagle Display Replica",
        "SIG Sauer P226 Display Replica",
        "Walther PPK Display Replica",
        "CZ 75 Display Replica",
        "Browning Hi-Power Display Replica"
    ],
    "Messen": [
        "Classic Bowie Display",
        "Tanto Display Knife",
        "Karambit Display Prop",
        "Hunting Knife Display",
        "Combat Knife Display Prop",
        "Butterfly Knife Display",
        "Dagger Collectible",
        "Survival Knife Display"
    ],
    "Kogels": [
        "Brass Ammunition Display",
        "Silver Bullet Collectible",
        "Vintage Cartridge Display",
        "Golden Bullet Prop",
        "Military Ammunition Display",
        "Classic Cartridge Set",
        "Collector Bullet Display",
        "Inert Ammunition Set"
    ],
    "Boksbeugels": [
        "Chrome Knuckle Display",
        "Black Metal Display Prop",
        "Vintage Knuckle Collectible",
        "Silver Collector Prop",
        "Classic Display Knuckles",
        "Matte Black Display",
        "Steel Finish Collectible",
        "Retro Knuckle Display"
    ],
    "Pistoolmagazijnen": [
        "Glock Magazine Display",
        "Beretta Magazine Display",
        "Colt Magazine Display",
        "SIG Sauer Magazine Display",
        "Walther Magazine Display",
        "CZ Magazine Display",
        "Browning Magazine Display",
        "Universal Magazine Display"
    ],
    "Bommen": [
        "Vintage Bomb Display Prop",
        "Classic Grenade Display",
        "Industrial Explosive Display",
        "Retro Game Bomb Prop",
        "Military Collectible Display",
        "Fictional Timer Prop",
        "Vintage Ordnance Display",
        "Museum Bomb Replica"
    ],
}

# Tijdelijke afbeeldingen met productnamen.
product_images = {
    category: [
        f"https://placehold.co/900x1100/111111/eeeeee?text={name.replace(' ', '+')}"
        for name in names
    ]
    for category, names in product_names.items()
}


products = []
product_id = 1

for category_index, category in enumerate(categories):
    category_name = category["name"]

    for number, product_name in enumerate(product_names[category_name]):
        price = 39.95 + (number * 10) + (category_index * 2)



        products.append({
            "id": product_id,
            "name": product_name,
            "category": category_name,
            "price": round(price, 2),
            "description": (
                f"Maak je outfit compleet met de {product_name}. "
                "Een stijlvolle toevoeging aan de VÉRRO collectie, "
                "met een comfortabele pasvorm en moderne uitstraling."
            ),
         "image": f"https://images.unsplash.com/{product_images[category_name][number]}?w=900&auto=format&fit=crop",
            "sizes": ["S", "M", "L", "XL"]
        })

        product_id += 1


@app.route("/")
def home():
    return render_template("index.html", categories=categories)


@app.route("/producten")
def product_list():
    selected_category = request.args.get("categorie", "")
    return render_template(
        "products.html",
        products=products,
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
        return jsonify({"error": "Geen bestelgegevens ontvangen"}), 400

    required = ["name", "address", "city", "email", "paymentMethod", "items"]

    if any(not data.get(field) for field in required):
        return jsonify({"error": "Vul alle verplichte gegevens in"}), 400

    if not isinstance(data["items"], list) or len(data["items"]) == 0:
        return jsonify({"error": "Je winkelmand is leeg"}), 400

    return jsonify({
        "message": "Je demo-bestelling is ontvangen!"
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
