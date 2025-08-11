import os
import sys
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

# exact keys as in your .env
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v22.0")

# 🔍 Debug prints
print("------ ENV VAR DEBUG ------")
print(f"WHATSAPP_TOKEN: {repr(WHATSAPP_TOKEN)}")
print(f"WHATSAPP_PHONE_NUMBER_ID: {repr(WHATSAPP_PHONE_NUMBER_ID)}")
print(f"WHATSAPP_VERIFY_TOKEN: {repr(WHATSAPP_VERIFY_TOKEN)}")
print(f"GRAPH_API_VERSION: {repr(GRAPH_API_VERSION)}")
print("---------------------------")

if not all([WHATSAPP_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_VERIFY_TOKEN]):
    print("ERROR: Missing one or more required env vars:")
    print("  WHATSAPP_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_VERIFY_TOKEN")
    sys.exit(1)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp bot running", 200

# Webhook verification endpoint
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
        print("✅ Webhook verified")
        return challenge, 200
    return "Verification failed", 403

# Receive incoming webhooks and reply
@app.route("/webhook", methods=["POST"])
def receive_webhook():
    data = request.get_json()
    print("Webhook payload:", data)

    if not data:
        return "No data", 400

    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            messages = value.get("messages") or []
            for msg in messages:
                from_number = msg.get("from")
                # try to extract text safely
                text = None
                msg_type = msg.get("type")

                if msg_type == "text":
                    text = msg.get("text", {}).get("body")
                elif msg_type == "interactive":
                    interactive = msg.get("interactive", {})
                    if interactive.get("type") == "button_reply":
                        text = interactive.get("button_reply", {}).get("title") or interactive.get("button_reply", {}).get("id")
                    elif interactive.get("type") == "list_reply":
                        text = interactive.get("list_reply", {}).get("title") or interactive.get("list_reply", {}).get("id")
                else:
                    # fallback for media or unsupported types
                    text = "<non-text message>"

                print(f"Received from {from_number}: {text}")

                # simple reply logic (customize as needed)
                if text and text.strip().lower() in ["hi", "hello", "hey"]:
                    reply = "Hello! 👋 How can I help you today?"
                elif text and text.strip().lower() == "menu":
                    reply = "Menu:\n1. Hours\n2. Contact\nReply with number."
                else:
                    reply = f"Auto-reply: I got your message: {text}"

                send_whatsapp_message(to=from_number, message_text=reply)

    return "EVENT_RECEIVED", 200

def send_whatsapp_message(to: str, message_text: str):
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message_text}
    }
    resp = requests.post(url, headers=headers, json=payload)
    print("Send status:", resp.status_code, resp.text)
    return resp

if __name__ == "__main__":
    app.run(port=5000, debug=True)
