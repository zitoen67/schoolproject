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
        "black,puffer,jacket",
        "winter,jacket,streetwear",
        "oversized,bomber,jacket",
        "black,puffer,coat",
        "streetwear,parka,jacket",
        "classic,black,jacket",
    ],
    "Hoodies": [
        "oversized,hoodie",
        "dark,streetwear,hoodie",
        "heavyweight,hoodie",
        "minimal,logo,hoodie",
        "relaxed,fit,hoodie",
        "zip,up,hoodie",
    ],
    "Truien": [
        "premium,knit,sweater",
        "basic,crewneck,sweatshirt",
        "oversized,knit,sweater",
        "minimal,sweater",
        "heavy,cotton,sweatshirt",
        "relaxed,pullover,sweater",
    ],
    "T-shirts": [
        "white,basic,tshirt",
        "black,oversized,tshirt",
        "graphic,streetwear,tshirt",
        "heavyweight,cotton,tshirt",
        "boxy,fit,tshirt",
        "minimal,logo,tshirt",
    ],
    "Broeken": [
        "black,cargo,pants",
        "baggy,utility,pants",
        "relaxed,track,pants",
        "wide,leg,trousers",
        "urban,cargo,pants",
        "essential,joggers",
    ],
    "Jeans": [
        "light,blue,baggy,jeans",
        "washed,black,jeans",
        "grey,loose,jeans",
        "dark,blue,denim,jeans",
        "relaxed,straight,jeans",
        "vintage,baggy,jeans",
    ],
    "Sneakers": [
        "classic,white,sneakers",
        "black,streetwear,sneakers",
        "retro,running,shoes",
        "minimal,white,leather,sneakers",
        "urban,high,top,sneakers",
        "everyday,trainers,sneakers",
    ],
    "Outfits": [
        "black,matching,tracksuit,set",
        "grey,tracksuit,set",
        "urban,streetwear,outfit",
        "oversized,casual,outfit",
        "neutral,matching,outfit",
        "all,black,streetwear,outfit",
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
    f"https://loremflickr.com/1000/1200/"
    f"{product_images[category_name][number]}"
    f"?lock={product_id}"
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
