from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

VAPI_API_KEY = "f37d590d-8bf0-43c0-86b3-a63b76c15461"

PORT = int(os.environ.get("PORT", 5000))

print("🔥🔥 FINAL WORKING CODE 🔥🔥")


@app.route('/')
def home():
    return "Server Running ✅"


@app.route('/test-call')
def test_call():
    phone = "+919033074408"

    url = "https://api.vapi.ai/call"

    payload = {
        "assistant": {
            "model": {
                "provider": "openai",
                "model": "gpt-4.1"
            },
            "firstMessage": "Namaste! Test call hai. Kya aap sun pa rahe ho?"
        },
        "customer": {
            "number": phone
        },
        "phoneNumber": "+14782156434"
    }

    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    print("🚀 SENDING REQUEST...")
    print("📦 PAYLOAD:", payload)

    response = requests.post(url, json=payload, headers=headers)

    print("📞 STATUS:", response.status_code)
    print("📞 RESPONSE:", response.text)

    return "CALL TRIGGERED", 200


@app.route('/shopify-webhook', methods=['POST'])
def shopify_webhook():
    print("🔥 SHOPIFY WEBHOOK HIT")

    try:
        data = request.get_json(force=True, silent=True)
        print(json.dumps(data, indent=2))

        phone = "+919033074408"

        url = "https://api.vapi.ai/call"

        payload = {
            "assistant": {
                "model": {
                    "provider": "openai",
                    "model": "gpt-4.1"
                },
                "firstMessage": "Namaste! Aapne NR Skins se order place kiya hai. Kya aap confirm karte ho?"
            },
            "customer": {
                "number": phone
            },
            "phoneNumber": "+14782156434"
        }

        headers = {
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json"
        }

        print("🚀 SENDING FROM WEBHOOK...")

        response = requests.post(url, json=payload, headers=headers)

        print("📞 STATUS:", response.status_code)
        print("📞 RESPONSE:", response.text)

    except Exception as e:
        print("❌ ERROR:", str(e))

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
