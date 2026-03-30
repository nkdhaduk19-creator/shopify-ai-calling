from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

VAPI_API_KEY = "cb25bf63-9caa-4719-a5fc-55bd74a7116a"

# Render port
PORT = int(os.environ.get("PORT", 5000))

print("🔥🔥 LATEST CODE DEPLOYED 🔥🔥")


@app.route('/')
def home():
    return "Server Running ✅"


# =========================
# 🧪 TEST CALL (IMPORTANT)
# =========================
@app.route('/test-call')
def test_call():
    print("🚀 MANUAL TEST CALL")

    phone = "+919033074408"

    url = "https://api.vapi.ai/call"

    payload = {
        "assistantId": "d716bf80-625e-4247-b0a8-382128836042",
        "customer": {
            "number": phone
        },
        "phoneNumber": "+14782156434"
    }

    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("📞 STATUS:", response.status_code)
    print("📞 RESPONSE:", response.text)

    return "CALL TRIGGERED"


# =========================
# 🛒 SHOPIFY WEBHOOK
# =========================
@app.route('/shopify-webhook', methods=['POST', 'GET'])
def shopify_webhook():
    print("🚨 WEBHOOK TRIGGERED 🚨")

    try:
        print("📦 METHOD:", request.method)
        print("📦 HEADERS:", dict(request.headers))
        print("📦 RAW BODY:", request.data)

        data = request.get_json(force=True, silent=True)
        print("📦 JSON DATA:", data)

        # 👉 Trial fix (force verified number)
        phone = "+919033074408"

        print("📞 FINAL PHONE:", phone)

        url = "https://api.vapi.ai/call"

        payload = {
            "assistantId": "d716bf80-625e-4247-b0a8-382128836042",
            "customer": {
                "number": phone
            },
            "phoneNumber": "+14782156434"
        }

        headers = {
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json"
        }

        print("🚀 CALLING VAPI...")
        print("📤 PAYLOAD:", payload)

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=15
        )

        print("📞 STATUS:", response.status_code)
        print("📞 RESPONSE:", response.text)

    except Exception as e:
        print("❌ ERROR:", str(e))

    return "OK", 200


# =========================
# 🚀 RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
