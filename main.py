from flask import ( 
    Flask,
    make_response,
    url_for,
    request,
    redirect
)
import requests
import json
import os
import jwt

tenant_id = os.getenv('AZURE_TENANT_ID', '')
client_id = os.getenv('AZURE_CLIENT_ID', '')
client_secret = os.getenv('AZURE_CLIENT_SECRET', '')
redirect_uri = 'http://localhost:5000/callback'
scope = ['https://graph.microsoft.com/.default']
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
auth_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize'

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    url = auth_url + (
        f"?client_id={client_id}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&response_mode=query"
        f"&scope={' '.join(scope)}"
    )
    return redirect(url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    # Exchange the authorization code for an access token
    response = requests.post(token_url, data={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    })
    token_response = json.loads(response.content.decode('utf-8'))
    for key, value in token_response.items():
        print(f"{key}: {value}")

    token_data = jwt.decode(token_response['access_token'], options={"verify_signature": False})
    print("Decoded Access Token:")
    for key, value in token_data.items():
        print(f"{key}: {value}")

    return make_response("ok")

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
