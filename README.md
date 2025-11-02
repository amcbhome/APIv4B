# APIv4B
# HMRC OAuth Hello Application Streamlit App 🔐

This app demonstrates Client Credentials OAuth flow using the HMRC Developer Hub Sandbox.

## ✅ Steps
1️⃣ Enter your sandbox `client_id` and `client_secret`  
2️⃣ Click "Get Access Token"  
3️⃣ Click "Call Hello Application API"

## 🔗 Endpoints
- Token: `https://test-api.service.hmrc.gov.uk/oauth/token`
- Hello App: `https://test-api.service.hmrc.gov.uk/hello/application`

## 🧑‍💻 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
