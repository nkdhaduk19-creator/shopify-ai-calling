from flask import Flask, request
import requests

app = Flask(__name__)

# 🔑 API KEY (CHANGE THIS)
VAPI_API_KEY = "cb25bf63-9caa-4719-a5fc-55bd74a7116a"


# 🟢 HOME
@app.route('/')
def home():
    return "Server Running ✅"


# 🟢 TEST
@app.route('/test')
def test():
    return "Working ✅"


# 🟢 SHOPIFY WEBHOOK
@app.route('/shopify-webhook', methods=['POST'])
def shopify_webhook():
    data = request.json

    print("🔥 SHOPIFY WEBHOOK HIT")
    print("📦 FULL DATA:", data)

    customer = data.get("customer", {})

    # 🔥 STRONG PHONE EXTRACTION
    phone = (
        customer.get("phone") or
        data.get("billing_address", {}).get("phone") or
        data.get("shipping_address", {}).get("phone") or
        data.get("phone")
    )

    print("📞 RAW PHONE:", phone)

    name = customer.get("first_name", "Customer")
    order_id = data.get("id")

    if not phone:
        print("❌ NO PHONE FOUND")
        return "No phone", 200

    # 📞 CLEAN PHONE
    phone = str(phone).replace(" ", "").replace("-", "")
    
    if not phone.startswith("+"):
        phone = "+91" + phone

    print("📞 FINAL PHONE:", phone)

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
        print("❌ VAPI ERROR:", str(e))

    return "OK", 200


# 🟢 VAPI RESPONSE
@app.route('/vapi-response', methods=['POST'])
def vapi_response():
    data = request.json

    print("🧠 VAPI RESPONSE:", data)

    transcript = data.get("transcript", "").lower()
    metadata = data.get("metadata", {})

    order_id = metadata.get("order_id")

    if not order_id:
        print("❌ NO ORDER ID")
        return "OK", 200

    # 🧠 YES / NO LOGIC
    if any(word in transcript for word in ["yes", "haan", "confirm", "kar do"]):
        print(f"✅ ORDER {order_id} CONFIRMED")

    elif any(word in transcript for word in ["no", "nahi", "cancel", "mat"]):
        print(f"❌ ORDER {order_id} CANCELLED")

    else:
        print(f"⚠️ ORDER {order_id} UNCLEAR RESPONSE")

    return "OK", 200


# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
