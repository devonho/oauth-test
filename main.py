from flask import ( 
    Flask,
    make_response,
    request,
    redirect
)
import requests
import os

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
    return "Hello from oauth-test!"

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
    return make_response(response.json())

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
