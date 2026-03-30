from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Server Running ✅"

@app.route('/shopify-webhook', methods=['POST'])
def shopify_webhook():
    data = request.json
    print("🔥 WEBHOOK HIT:", data)

    phone = data.get("customer", {}).get("phone")
    name = data.get("customer", {}).get("first_name")

    print("Customer:", name, phone)

    return "OK", 200

app.run(host="0.0.0.0", port=5000)
