import os
from flask import Flask, render_template, request, abort

app = Flask(__name__)

# De zes bestaande categorieën
categories = [
    {"name": "Pistolen", "slug": "Pistolen"},
    {"name": "Messen", "slug": "Messen"},
    {"name": "Kogels", "slug": "Kogels"},
    {"name": "Boksbeugels", "slug": "Boksbeugels"},
    {"name": "Pistoolmagazijnen", "slug": "Pistoolmagazijnen"},
    {"name": "Bommen", "slug": "Bommen"},
]

# Alle 48 bestaande productnamen
product_names = {
    "Pistolen": [
        "Glock 17",
        "Beretta 92FS",
        "Colt M1911",
        "Desert Eagle",
        "SIG Sauer P226",
        "Walther PPK",
        "CZ 75",
        "FN Browning Hi-Power",
    ],
    "Messen": [
        "Victorinox Swiss Army Knife",
        "Opinel No. 8",
        "Wüsthof Classic",
        "Leatherman Wave+",
        "Morakniv Companion",
        "Buck 110",
        "Spyderco Paramilitary 2",
        "KA-BAR USMC",
    ],
    "Kogels": [
        "9x19mm Parabellum",
        ".22 Long Rifle",
        "5.56x45mm NATO",
        "7.62x39mm",
        ".45 ACP",
        "7.62x51mm NATO",
        "12 Gauge",
        ".50 BMG",
    ],
    "Boksbeugels": [
        "Klassieke Boksbeugel",
        "Viervinger Boksbeugel",
        "Tweekleurige Boksbeugel",
        "Tekko",
        "Apache Revolver Boksbeugel",
        "Mark I Trench Knife Boksbeugel",
        "Tactische Boksbeugel",
        "Vechtsport Boksbeugel",
    ],
    "Pistoolmagazijnen": [
        "Glock 17 Magazijn",
        "Beretta 92 Magazijn",
        "Colt M1911 Magazijn",
        "SIG Sauer P226 Magazijn",
        "CZ 75 Magazijn",
        "Walther PPK Magazijn",
        "FN Browning Magazijn",
        "Universeel Magazijn",
    ],
    "Bommen": [
        "Mills Bomb",
        "Stielhandgranate M24",
        "Mk 2 Fragmentation Grenade",
        "F1 Hand Grenade",
        "RGD-5 Hand Grenade",
        "M67 Hand Grenade",
        "DM51 Hand Grenade",
        "M26 Hand Grenade",
    ],
}

# Realistische prijzen per categorie
product_prices = {
    "Pistolen": [695.00, 890.00, 1150.00, 2450.00, 1395.00, 950.00, 850.00, 1250.00],
    "Messen": [39.95, 14.95, 119.00, 149.95, 19.95, 89.95, 235.00, 135.00],
    "Kogels": [18.50, 7.50, 16.00, 14.50, 29.50, 24.00, 15.00, 65.00],
    "Boksbeugels": [25.00, 29.95, 34.95, 65.00, 1850.00, 195.00, 39.95, 27.50],
    "Pistoolmagazijnen": [32.00, 39.00, 35.00, 55.00, 45.00, 49.00, 52.00, 29.95],
    "Bommen": [145.00, 175.00, 125.00, 115.00, 95.00, 135.00, 155.00, 110.00],
}

# Geverifieerde, directe afbeeldingslinks per specifiek product
product_images = {
    "Pistolen": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Glock_17_%286825676904%29.jpg/800px-Glock_17_%286825676904%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Beretta_92FS-9mm-pistol-2.jpg/800px-Beretta_92FS-9mm-pistol-2.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/M1911A1.jpg/800px-M1911A1.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Desert-Eagle-pistol.jpg/800px-Desert-Eagle-pistol.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/SIG_Sauer_P226_%282%29.jpg/800px-SIG_Sauer_P226_%282%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Walther_PPK_7%2C65mm.jpg/800px-Walther_PPK_7%2C65mm.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/CZ_75_B_9mm.jpg/800px-CZ_75_B_9mm.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Browning_Hi-Power.jpg/800px-Browning_Hi-Power.jpg",
    ],
    "Messen": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Swiss_Army_Knife.jpg/800px-Swiss_Army_Knife.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Opinel_No_08_Inox.jpg/800px-Opinel_No_08_Inox.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Wusthof_Chef%27s_Knife.jpg/800px-Wusthof_Chef%27s_Knife.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Leatherman_Wave.jpg/800px-Leatherman_Wave.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Mora_Companion_MG.jpg/800px-Mora_Companion_MG.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Buck_110_Folding_Hunter.jpg/800px-Buck_110_Folding_Hunter.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Spyderco_Paramilitary_2.jpg/800px-Spyderco_Paramilitary_2.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Ka-Bar_USMC.jpg/800px-Ka-Bar_USMC.jpg",
    ],
    "Kogels": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/9x19mm_Parabellum.jpg/800px-9x19mm_Parabellum.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/.22_Long_Rifle.jpg/800px-.22_Long_Rifle.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/5.56x45mm_NATO.jpg/800px-5.56x45mm_NATO.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/7.62x39mm.jpg/800px-7.62x39mm.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/.45_ACP.jpg/800px-.45_ACP.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/7.62x51mm_NATO.jpg/800px-7.62x51mm_NATO.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/12_gauge_shotgun_shells.jpg/800px-12_gauge_shotgun_shells.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/.50_BMG_cartridge.jpg/800px-.50_BMG_cartridge.jpg",
    ],
    "Boksbeugels": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Brass_knuckles_1.jpg/800px-Brass_knuckles_1.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Brass_knuckles.jpg/800px-Brass_knuckles.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Schlagring_Eisen.jpg/800px-Schlagring_Eisen.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Tekko_1.jpg/800px-Tekko_1.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Apache_revolver_IMG_4254.jpg/800px-Apache_revolver_IMG_4254.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/US_M1918_Mark_I_Trench_Knife.jpg/800px-US_M1918_Mark_I_Trench_Knife.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Poing_americain.jpg/800px-Poing_americain.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Cestus_Roman.jpg/800px-Cestus_Roman.jpg",
    ],
    "Pistoolmagazijnen": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Glock_17_magazine.jpg/800px-Glock_17_magazine.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Beretta_92_magazine.jpg/800px-Beretta_92_magazine.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/M1911_magazine.jpg/800px-M1911_magazine.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/SIG_P226_magazine.jpg/800px-SIG_P226_magazine.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/CZ_75_magazine.jpg/800px-CZ_75_magazine.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Walther_PPK_magazine.jpg/800px-Walther_PPK_magazine.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Browning_Hi-Power_magazine.jpg/800px-Browning_Hi-Power_magazine.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Pistol_magazines.jpg/800px-Pistol_magazines.jpg",
    ],
    "Bommen": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Mills_bomb_N%C2%B0_36.jpg/800px-Mills_bomb_N%C2%B0_36.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Stielhandgranate_M24.jpg/800px-Stielhandgranate_M24.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Mk_II_hand_grenade.jpg/800px-Mk_II_hand_grenade.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/F1_grenade.jpg/800px-F1_grenade.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/RGD-5_grenade.jpg/800px-RGD-5_grenade.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/M67_hand_grenade.jpg/800px-M67_hand_grenade.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/DM51_Handgranate.jpg/800px-DM51_Handgranate.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/M26_hand_grenade.jpg/800px-M26_hand_grenade.jpg",
    ],
}

# Automatisch genereren van de productlijst
products = []
product_id = 1

for category_index, category in enumerate(categories):
    category_name = category["name"]

    for number, product_name in enumerate(product_names[category_name]):
        products.append({
            "id": product_id,
            "name": product_name,
            "category": category_name,
            "price": product_prices[category_name][number],
            "description": f"Hoogwaardig exemplaar uit de exclusieve D-WEB catalogus: {product_name}.",
            "image": product_images[category_name][number],
        })
        product_id += 1

# Routes
@app.route("/")
def home():
    return render_template("index.html", categories=categories)


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

    return render_template("product.html", product=product)


@app.errorhandler(404)
def page_not_found(error):
    return "Deze pagina bestaat niet.", 404


# Render-compatibele server start (leest dynamische PORT van Render of gebruikt 5000 lokaal)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
