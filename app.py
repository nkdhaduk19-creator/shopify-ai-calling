from flask import Flask, request
import requests

app = Flask(__name__)

# 🔑 IMPORTANT — yaha apna VAPI API KEY daal
VAPI_API_KEY = "cb25bf63-9caa-4719-a5fc-55bd74a7116a"


# 🟢 HOME ROUTE (TEST)
@app.route('/')
def home():
    return "Server Running ✅"


# 🟢 EXTRA TEST ROUTE
@app.route('/test')
def test():
    return "Working ✅"


# 🟢 SHOPIFY WEBHOOK
@app.route('/shopify-webhook', methods=['POST'])
def shopify_webhook():
    data = request.json

    print("🔥 WEBHOOK HIT:", data)

    # 🧠 Customer details extract
    customer = data.get("customer", {})
    phone = customer.get("phone")
    name = customer.get("first_name", "Customer")

    print("Customer:", name, phone)

    # ❗ Agar phone nahi hai to skip
    if not phone:
        print("❌ No phone number found")
        return "No phone", 200

    # 📞 Phone format fix (+91 add agar missing)
    if not phone.startswith("+"):
        phone = "+91" + phone

    try:
        # 📞 VAPI CALL TRIGGER
        response = requests.post(
            "https://api.vapi.ai/call",
            json={
                "customer": {
                    "number": phone
                },
                "assistant": {
                    "firstMessage": f"Namaste {name}, aapne NR Skins se order place kiya hai. Kya aap apna order confirm karte ho?"
                }
            },
            headers={
                "Authorization": f"Bearer {VAPI_API_KEY}",
                "Content-Type": "application/json"
            }
        )

        print("📞 Call API Response:", response.text)

    except Exception as e:
        print("❌ Error while calling:", str(e))

    return "OK", 200


# 🟢 SERVER START
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
