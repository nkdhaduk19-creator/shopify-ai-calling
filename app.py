from flask import Flask, request
import requests
import json

app = Flask(__name__)

VAPI_API_KEY = "cb25bf63-9caa-4719-a5fc-55bd74a7116a""


@app.route('/')
def home():
    return "Server Running ✅"


@app.route('/shopify-webhook', methods=['POST'])
def shopify_webhook():
    try:
        print("\n🔥 WEBHOOK HIT 🔥")

        data = request.json
        print(json.dumps(data, indent=2))

        phone = None

        if data.get("customer") and data["customer"].get("phone"):
            phone = data["customer"]["phone"]
        elif data.get("shipping_address") and data["shipping_address"].get("phone"):
            phone = data["shipping_address"]["phone"]
        elif data.get("billing_address") and data["billing_address"].get("phone"):
            phone = data["billing_address"]["phone"]

        print("📞 RAW PHONE:", phone)

        if not phone:
            print("⚠️ NO PHONE → USING TEST")
            phone = "+919033074408"

        phone = str(phone).replace(" ", "").replace("-", "")

        if not phone.startswith("+"):
            phone = "+91" + phone

        print("📞 FINAL PHONE:", phone)

        url = "https://api.vapi.ai/call"

        payload = {
            "customer": {
                "number": phone
            },
            "phoneNumber": "+14782156434",
            "assistant": {
                "firstMessage": "Namaste! Test call hai. Kya aap sun pa rahe ho?"
            }
        }

        headers = {
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json"
        }

        print("🚀 CALLING VAPI...")

        response = requests.post(url, json=payload, headers=headers)

        print("📞 STATUS:", response.status_code)
        print("📞 RESPONSE:", response.text)

    except Exception as e:
        print("❌ ERROR:", str(e))

    return "OK", 200
    print("🚨 NEW VERSION RUNNING 🚨")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
