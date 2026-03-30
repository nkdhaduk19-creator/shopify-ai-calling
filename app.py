from flask import Flask, request
import requests

app = Flask(__name__)

# 🔑 API KEY (CHANGE THIS)
VAPI_API_KEY = "cb25bf63-9caa-4719-a5fc-55bd74a7116a"


# 🟢 HOME ROUTE
@app.route('/')
def home():
    return "Server Running ✅"


# 🟢 TEST ROUTE
@app.route('/test')
def test():
    return "Working ✅"


# 🟢 SHOPIFY WEBHOOK (ORDER CREATE)
@app.route('/shopify-webhook', methods=['POST'])
def shopify_webhook():
    data = request.json

    print("🔥 SHOPIFY WEBHOOK:", data)

    customer = data.get("customer", {})
    phone = customer.get("phone")
    name = customer.get("first_name", "Customer")
    order_id = data.get("id")

    print("Customer:", name, phone, "Order ID:", order_id)

    if not phone:
        print("❌ No phone number")
        return "No phone", 200

    # 📞 Fix phone format
    if not phone.startswith("+"):
        phone = "+91" + phone

    try:
        response = requests.post(
            "https://api.vapi.ai/call",
            json={
                "customer": {
                    "number": phone
                },
                "assistant": {
                    "firstMessage": f"Namaste {name}, aapne NR Skins se order place kiya hai. Kya aap apna order confirm karte ho?"
                },
                "metadata": {
                    "order_id": order_id
                },
                "server": {
                    "url": "https://shopify-ai-calling.onrender.com/vapi-response"
                }
            },
            headers={
                "Authorization": f"Bearer {VAPI_API_KEY}",
                "Content-Type": "application/json"
            }
        )

        print("📞 VAPI CALL RESPONSE:", response.text)

    except Exception as e:
        print("❌ Call error:", str(e))

    return "OK", 200


# 🟢 VAPI RESPONSE WEBHOOK
@app.route('/vapi-response', methods=['POST'])
def vapi_response():
    data = request.json

    print("🧠 VAPI RESPONSE:", data)

    transcript = data.get("transcript", "").lower()
    metadata = data.get("metadata", {})

    order_id = metadata.get("order_id")

    if not order_id:
        print("❌ No order ID")
        return "OK", 200

    # 🧠 YES / NO detection
    if any(word in transcript for word in ["yes", "haan", "confirm", "kar do"]):
        print(f"✅ Order {order_id} CONFIRMED")

    elif any(word in transcript for word in ["no", "nahi", "cancel", "mat"]):
        print(f"❌ Order {order_id} CANCELLED")

    else:
        print(f"⚠️ Order {order_id} unclear response")

    return "OK", 200


# 🚀 RUN SERVER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
