import streamlit as st
import requests
import base64

st.set_page_config(page_title="HMRC OAuth Hello App", page_icon="🔐")
st.title("🔐 HMRC Hello Application (OAuth Client Credentials)")
st.write("This calls the HMRC Sandbox using secure access token authentication.")

TOKEN_URL = "https://test-api.service.hmrc.gov.uk/oauth/token"
HELLO_APP_URL = "https://test-api.service.hmrc.gov.uk/hello/application"

# ✅ Load secrets from Streamlit Cloud
client_id = st.secrets["HMRC_CLIENT_ID"]
client_secret = st.secrets["HMRC_CLIENT_SECRET"]

st.write("✅ Secrets Loaded ✔")

def get_access_token(client_id, client_secret):
    # Create Basic Auth header
    auth_str = f"{client_id}:{client_secret}"
    encoded_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Accept": "application/json"
    }

    # ✅ FINAL FIX: HMRC sandbox requires BOTH id & secret in POST body
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    return requests.post(TOKEN_URL, headers=headers, data=data), encoded_auth


if st.button("Request Access Token ✅"):
    token_response, encoded_auth = get_access_token(client_id, client_secret)

    # Debugging display (safe)
    st.write("🔐 Encoded Auth Header (partial):", encoded_auth[:10] + "... (hidden)")

    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        st.success("✅ Token Retrieved Successfully!")
        st.json(token_data)

        if st.button("Call Hello Application API 🟢"):
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.hmrc.1.0+json"
            }

            api_response = requests.get(HELLO_APP_URL, headers=headers)

            if api_response.status_code == 200:
                st.success("✅ HMRC API call succeeded!")
                st.json(api_response.json())
            else:
                st.error(f"❌ API Error: {api_response.status_code}")
                st.code(api_response.text)

    else:
        st.error(f"❌ Token Error: {token_response.status_code}")
        st.code(token_response.text)