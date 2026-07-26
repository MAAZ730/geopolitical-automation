import json
import os
import requests


def exchange_code():
    """Exchange an OAuth authorization code for refreshable Drive credentials."""
    with open("credentials.json", "r") as f:
        creds = json.load(f)["installed"]

    # Keep the auth code outside source control so we never commit one-time secrets.
    code = os.getenv("GOOGLE_OAUTH_AUTH_CODE", "").strip()
    if not code:
        print("Error: GOOGLE_OAUTH_AUTH_CODE is not set.")
        return

    data = {
        "code": code,
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "redirect_uri": "http://localhost",
        "grant_type": "authorization_code"
    }
    
    response = requests.post(creds["token_uri"], data=data)
    token_data = response.json()
    
    if "error" in token_data:
        print(f"Error exchanging code: {token_data}")
        return
        
    final_creds = {
        "token": token_data.get("access_token"),
        "refresh_token": token_data.get("refresh_token"),
        "token_uri": creds["token_uri"],
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "scopes": ["https://www.googleapis.com/auth/drive.file"],
        # This is intentionally synthetic; google-auth refresh flow keeps it current.
        "expiry": "2030-01-01T00:00:00.000000Z"
    }
    
    with open("token.json", "w") as f:
        json.dump(final_creds, f, indent=4)
        
    print("\n✅ SUCCESS! Google OAuth 2.0 Token Generated.")
    print("--- RAW JSON (COPY EVERYTHING BELOW) ---")
    print(json.dumps(final_creds, indent=2))
    print("--- COPY ABOVE THIS LINE ---\n")

if __name__ == "__main__":
    exchange_code()
