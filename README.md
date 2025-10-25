# OAuth 2.0 authorization code flow

The OAuth 2.0 authorization code flow is a secure method for web applications to get user consent and **access protected resources on behalf of a user**, without needing the user's password. It involves a user-initiated redirect to an authorization server to log in and grant permission, after which the user is sent back to the client with a short-lived authorization code. The client application then exchanges this code with its client ID and secret for an access token and potentially other tokens like refresh or ID tokens. 

## Step 1: Redirect to the authorization server 
* The client application redirects the user's browser to the authorization server's authorization endpoint.
* This initial request includes the client ID, the requested permissions (scope), a redirect URI, and a unique state parameter to protect against cross-site request forgery (CSRF).
* The response_type is set to code to specify this flow. 

## Step 2: User authenticates and grants consent 
* The user logs into the authorization server.
* The user is presented with a consent screen detailing the requested permissions.
* The user approves or denies the request. 

## Step 3: User is redirected back to the client 
* If approved, the authorization server redirects the user back to the specified redirect URI on the client application's server.
* The authorization code is included as a query parameter in the redirect URL, along with the original state parameter.
* The client application verifies the state parameter to ensure the request originated from it. 

## Step 4: Client exchanges the code for tokens 
* The client application makes a secure, back-channel request to the authorization server's token endpoint.
* This request includes the authorization code, its client ID, and its client secret.
* If successful, the authorization server returns an access token, a refresh token (optional), and an ID token (for OpenID Connect).
* The authorization code is invalidated after being used once. 

## Step 5: Client uses the access token 
* The client uses the access token to make authenticated requests to the resource server (e.g., an API) to access user data on their behalf. 