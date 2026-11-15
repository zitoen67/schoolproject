from flask import Flask, render_template, request, abort

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
            "price": round(
                9.95 + number * 5 + category_index * 2, 2
            ),
            "description": (
                f"{product_name}. Onderdeel van de D-WEB "
                "historische collectie. Een informatieve "
                "presentatie over geschiedenis en industrieel design."
            ),
            "image": (
    "/static/images/products/product_09.png"
    if product_id == 9
    else f"/static/images/products/product_{product_id:02d}.jpg"
),
        })

        product_id += 1


@app.route("/")
def home():
    return render_template(
        "index.html",
        categories=categories
    )


@app.route("/producten")
def product_list():
    selected_category = request.args.get("categorie", "")

    filtered_products = products

    if selected_category in product_names:
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

    return render_template(
        "product.html",
        product=product
    )


@app.errorhandler(404)
def page_not_found(error):
    return "Deze pagina bestaat niet.", 404


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
