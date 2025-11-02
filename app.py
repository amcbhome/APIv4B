import streamlit as st
import requests
import base64

st.set_page_config(page_title="HMRC OAuth Hello App", page_icon="🔐")
st.title("🔐 HMRC Hello Application (OAuth Client Credentials)")
st.write("This calls the HMRC Sandbox using a secure access token.")

TOKEN_URL = "https://test-api.service.hmrc.gov.uk/oauth/token"
HELLO_APP_URL = "https://test-api.service.hmrc.gov.uk/hello/application"

# ✅ Load secrets from Streamlit Cloud
client_id = st.secrets["HMRC_CLIENT_ID"]
client_secret = st.secrets["HMRC_CLIENT_SECRET"]

st.write("✅ ID Loaded:", "HMRC_CLIENT_ID" in st.secrets)
st.write("✅ Secret Loaded:", "HMRC_CLIENT_SECRET" in st.secrets)

def get_access_token(client_id, client_secret):
    auth_str = f"{client_id}:{client_secret}"
    encoded_auth = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "hello"
    }

    return requests.post(TOKEN_URL, headers=headers, data=data)


if st.button("Request Access Token"):
    token_response = get_access_token(client_id, client_secret)

    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        st.success("✅ Token Retrieved Successfully")
        st.json(token_data)

        if st.button("Call Hello Application API"):
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.hmrc.1.0+json"
            }
            api_response = requests.get(HELLO_APP_URL, headers=headers)

            if api_response.status_code == 200:
                st.success("✅ API Call Successful")
                st.json(api_response.json())
            else:
                st.error(f"API Error {api_response.status_code}")
                st.write(api_response.text)

    else:
        st.error(f"Token Error {token_response.status_code}")
        st.write(token_response.text)
