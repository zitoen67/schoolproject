from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__)

categories = [
    {"name": "Jassen", "slug": "Jassen"},
    {"name": "Hoodies", "slug": "Hoodies"},
    {"name": "Truien", "slug": "Truien"},
    {"name": "T-shirts", "slug": "T-shirts"},
    {"name": "Broeken", "slug": "Broeken"},
    {"name": "Jeans", "slug": "Jeans"},
    {"name": "Sneakers", "slug": "Sneakers"},
    {"name": "Outfits", "slug": "Outfits"},
]

# Per categorie zes producten.
product_names = {
    "Jassen": [
        "Black Puffer Jacket", "Urban Winter Jacket", "Oversized Bomber",
        "Essential Puffer", "Streetwear Parka", "Classic Black Jacket"
    ],
    "Hoodies": [
        "Essential Oversized Hoodie", "Dark Street Hoodie", "Heavyweight Hoodie",
        "Core Logo Hoodie", "Relaxed Fit Hoodie", "Urban Zip Hoodie"
    ],
    "Truien": [
        "Premium Knit Sweater", "Basic Crewneck", "Oversized Knit",
        "Minimal Sweater", "Heavy Cotton Sweater", "Relaxed Pullover"
    ],
    "T-shirts": [
        "Essential White Tee", "Oversized Black Tee", "Graphic Street Tee",
        "Heavyweight T-shirt", "Boxy Fit Tee", "Minimal Logo Tee"
    ],
    "Broeken": [
        "Black Cargo Pants", "Baggy Utility Pants", "Relaxed Track Pants",
        "Wide Leg Trousers", "Urban Cargo Pants", "Essential Joggers"
    ],
    "Jeans": [
        "Light Blue Baggy Jeans", "Washed Black Jeans", "Grey Loose Jeans",
        "Dark Blue Denim", "Relaxed Straight Jeans", "Vintage Baggy Jeans"
    ],
    "Sneakers": [
        "Classic White Sneakers", "Black Street Sneakers", "Retro Runner",
        "Minimal Leather Sneakers", "Urban High Tops", "Everyday Trainers"
    ],
    "Outfits": [
        "Black Essential Set", "Grey Tracksuit Set", "Urban Street Outfit",
        "Oversized Everyday Set", "Neutral Matching Set", "All Black Outfit"
    ],
}

product_images = {
    "Jassen": [
        "photo-1544923246-77307dd654cb",
        "photo-1591047139829-d91aecb6caea",
        "photo-1551028719-00167b16eac5",
        "photo-1543076447-215ad9ba6923",
        "photo-1548126032-079a0fb0099d",
        "photo-1592878904946-b3cd8ae243d0",
    ],
    "Hoodies": [
        "photo-1556821840-3a63f95609a7",
        "photo-1578681994506-b8f463449011",
        "photo-1556821840-3a63f95609a7",
        "photo-1578768079052-aa76e52ff62e",
        "photo-1556821840-3a63f95609a7",
        "photo-1578681994506-b8f463449011",
    ],
    "Truien": [
        "photo-1618354691373-d851c5c3a990",
        "photo-1576566588028-4147f3842f27",
        "photo-1618354691229-88d47f285158",
        "photo-1620799140408-edc6dcb6d633",
        "photo-1576566588028-4147f3842f27",
        "photo-1618354691373-d851c5c3a990",
    ],
    "T-shirts": [
        "photo-1521572163474-6864f9cf17ab",
        "photo-1503341504253-dff4815485f1",
        "photo-1521572163474-6864f9cf17ab",
        "photo-1581655353564-df123a1eb820",
        "photo-1503341455253-b2e723bb3dbb",
        "photo-1521572163474-6864f9cf17ab",
    ],
    "Broeken": [
        "photo-1473966968600-fa801b869a1a",
        "photo-1517438476312-10d79c077509",
        "photo-1473966968600-fa801b869a1a",
        "photo-1506629905607-d9e2f6b1a8c7",
        "photo-1517438476312-10d79c077509",
        "photo-1473966968600-fa801b869a1a",
    ],
    "Jeans": [
        "photo-1542272604-787c3835535d",
        "photo-1541099649105-f69ad21f3246",
        "photo-1542272604-787c3835535d",
        "photo-1541099649105-f69ad21f3246",
        "photo-1542272604-787c3835535d",
        "photo-1541099649105-f69ad21f3246",
    ],
    "Sneakers": [
        "photo-1542291026-7eec264c27ff",
        "photo-1495555961986-6d4c1ecb7be3",
        "photo-1542291026-7eec264c27ff",
        "photo-1460353581641-37baddab0fa2",
        "photo-1495555961986-6d4c1ecb7be3",
        "photo-1460353581641-37baddab0fa2",
    ],
    "Outfits": [
        "photo-1515886657613-9f3515b0c78f",
        "photo-1529139574466-a303027c1d8b",
        "photo-1515886657613-9f3515b0c78f",
        "photo-1539109136881-3be0616acf4b",
        "photo-1529139574466-a303027c1d8b",
        "photo-1539109136881-3be0616acf4b",
    ],
}


products = []
product_id = 1

for category in categories:
    category_name = category["name"]

    for number, product_name in enumerate(product_names[category_name]):
        price = 39.95 + (number * 10) + (categories.index(category) * 2)

        products.append({
            "id": product_id,
            "name": product_name,
            "category": category_name,
            "price": round(price, 2),
            "description": (
                f"Maak je outfit compleet met de {product_name}. "
                "Een stijlvolle toevoeging aan de VÉRRO collectie, "
                "met een comfortabele pasvorm en een moderne streetwear uitstraling."
            ),
           "image": (
    f"https://images.unsplash.com/"
    f"{product_images[category_name][number]}"
    "?auto=format&fit=crop&w=1000&q=85"
),
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

    # Dit is alleen een demo. Er wordt geen betaling uitgevoerd
    # en er worden geen persoonsgegevens opgeslagen.
    return jsonify({
        "message": "Je demo-bestelling is ontvangen!"
    })


@app.errorhandler(404)
def page_not_found(error):
    return "Deze pagina bestaat niet.", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
