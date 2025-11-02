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

# ✅ Check secrets loaded
st.write("✅ ID Loaded:", "HMRC_CLIENT_ID" in st.secrets)
st.write("✅ Secret Loaded:", "HMRC_CLIENT_SECRET" in st.secrets)


def get_access_token(client_id, client_secret):
    auth_str = f"{client_id}:{client_secret}"
    
    # ✅ Strong explicit Base64 Encoding
    encoded_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Accept": "application/json"
    }

    data = {"grant_type": "client_credentials"}

    return requests.post(TOKEN_URL, headers=headers, data=data), encoded_auth


if st.button("Request Access Token"):
    token_response, encoded_auth = get_access_token(client_id, client_secret)

    # ✅ Debug header fragment to help diagnose 400 errors safely
    st.write("🔐 Encoded Auth:", encoded_auth[:10] + "... (hidden)")

    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        st.success("✅ Token Retrieved Successfully!")
        st.json(token_data)

        if st.button("Call Hello Application API"):
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.hmrc.1.0+json"
            }

            api_response = requests.get(HELLO_APP_URL, headers=headers)

            if api_response.status_code == 200:
                st.success("✅ API Call Successful!")
                st.json(api_response.json())
            else:
                st.error(f"❌ API Error: {api_response.status_code}")
                st.code(api_response.text)

    else:
        st.error(f"❌ Token Error: {token_response.status_code}")
        st.code(token_response.text)