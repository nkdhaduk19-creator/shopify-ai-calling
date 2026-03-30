from flask import Flask, request
import requests
import json

app = Flask(__name__)

VAPI_API_KEY = "cb25bf63-9caa-4719-a5fc-55bd74a7116a"


@app.route('/')
def home():
    return "Server Running ✅"


@app.route('/shopify-webhook', methods=['POST'])
def shopify_webhook():
    try:
        data = request.json

        print("\n🔥🔥 WEBHOOK HIT 🔥🔥")
        print(json.dumps(data, indent=2))

        # 🔍 GET PHONE FROM ALL POSSIBLE PLACES
        phone = None

        if data.get("customer") and data["customer"].get("phone"):
            phone = data["customer"]["phone"]

        elif data.get("shipping_address") and data["shipping_address"].get("phone"):
            phone = data["shipping_address"]["phone"]

        elif data.get("billing_address") and data["billing_address"].get("phone"):
            phone = data["billing_address"]["phone"]

        print("📞 RAW PHONE:", phone)

        if not phone:
            print("❌ PHONE NOT FOUND")
            return "No phone", 200

        # 🔧 CLEAN PHONE
        phone = str(phone).replace(" ", "").replace("-", "")

        if not phone.startswith("+"):
            phone = "+91" + phone

        print("📞 FINAL PHONE:", phone)

        # 🚀 CALL VAPI
        url = "https://api.vapi.ai/call"

       payload = {
    "customer": {
        "number": phone
    },
    "phoneNumber": "+14782156434",  # 👈 VERY IMPORTANT (tera Twilio number)
    "assistant": {
        "firstMessage": "Namaste! Aapne NR Skins se order place kiya hai. Kya aap confirm karte ho?"
    }
}

        headers = {
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json"
        }

        print("🚀 SENDING TO VAPI...")

        response = requests.post(url, json=payload, headers=headers)

        print("📞 VAPI STATUS:", response.status_code)
        print("📞 VAPI RESPONSE:", response.text)

    except Exception as e:
        print("❌ ERROR:", str(e))

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
