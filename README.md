# python_whatsapp_chatbot
# 📱 WhatsApp Bot — Flask + WhatsApp Cloud API

A simple WhatsApp chatbot built using **Flask** and the **Meta WhatsApp Cloud API**.  
This bot listens for incoming WhatsApp messages and replies automatically.

---

## 🚀 Features
- Receive incoming WhatsApp messages via webhook
- Send automatic replies using WhatsApp Cloud API
- Built with Python (Flask)
- Uses ngrok for local development
- Secure credentials with `.env` file

---

## 📦 Prerequisites
Before starting, install:
- [Python 3.9+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Git](https://git-scm.com/downloads)
- [ngrok](https://ngrok.com/download)

Also, you’ll need:
- A **Meta for Developers** account → [https://developers.facebook.com/](https://developers.facebook.com/)
- A **WhatsApp Cloud API test number** from your app dashboard

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/whatsapp-bot-flask.git
cd whatsapp-bot-flask
```

###2️⃣ Create a virtual environment
```
python -m venv venv
```
Activate it:
```
Windows : venv\Scripts\activate
macos/linux : source venv/bin/activate
```
###3️⃣ Install dependencies
```
pip install -r requirements.txt
if requirements.txt not there create one
pip freeze > requirements.txt
```
###4️⃣ Create .env file
```
WHATSAPP_TOKEN=YOUR_LONG_LIVED_ACCESS_TOKEN
WHATSAPP_PHONE_NUMBER_ID=YOUR_PHONE_NUMBER_ID
WHATSAPP_VERIFY_TOKEN=mywhatsapptestbot123
GRAPH_API_VERSION=v22.0
```

🌍 Webhook Setup
5️⃣ Start ngrok
In a new terminal: ngrok http 5000

6️⃣ Configure Meta Webhook
Go to Meta Developer Dashboard > WhatsApp > Configuration

Callback URL → https://YOUR_NGROK_URL/webhook

Verify Token → must match WHATSAPP_VERIFY_TOKEN in .env

Subscribe to messages.

▶️ Run the bot
python app.py

If successful, you’ll see:
✅ Webhook verified
WhatsApp bot running

💬 Testing
Add your WhatsApp number as a test user in the Meta dashboard.
Send a message (e.g., hi) to your WhatsApp test number.
The bot will reply.

🛠 Built With
```
Flask
Requests
WhatsApp Cloud API
```