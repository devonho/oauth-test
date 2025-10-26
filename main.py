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
#scope = ['User.Read','https://graph.microsoft.com/.default']
scope = ["User.Read","openid","profile","offline_access"]
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
        f"&response_type=code+id_token"
        f"&redirect_uri={redirect_uri}"
        #f"&response_mode=query"
        f"&response_mode=form_post"
        f"&scope={' '.join(scope)}"
        f"&nonce=12345"
    )
    return redirect(url)

@app.route("/callback", methods=["POST"])
def callback():
    code = request.form.get("code")
    # Exchange the authorization code for an access token
    response = requests.post(token_url, data={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    })

    if response.status_code != 200:
        return make_response(f"Error fetching token: {response.text}", 400)
    else:
        token_response = response.json()

        id_token = jwt.decode(token_response['id_token'], options={"verify_signature": False})
        with open("id_token.json", "w") as f:
            json.dump(id_token, f, indent=4)

        access_token = jwt.decode(token_response['access_token'], options={"verify_signature": False})
        with open("access_token.json", "w") as f:
            json.dump(access_token, f, indent=4)
        return make_response("ok")

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
