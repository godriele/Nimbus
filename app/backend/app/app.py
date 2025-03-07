from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a secure random key in production

# Initialize OAuth
oauth = OAuth(app)

# Register the OAuth app with AWS Cognito
oauth.register(
    name='oidc',
    authority='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_TcqiaNQSu',
    client_id='3snvum8hd990384u743joh3edt',
    client_secret='1nt3m52f5s89iku57heu487ptdfsk0ftgelnlk8vopik9jek4o2m',
    server_metadata_url='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_TcqiaNQSu/.well-known/openid-configuration',
    client_kwargs={'scope': 'email openid phone'}
)

# Routes
@app.route('/')
def index():
    """Home route, checks if user is logged in."""
    user = session.get('user')
    if user:
        return f'Hello, {user["email"]}. <a href="/logout">Logout</a>'
    else:
        return f'Welcome! Please <a href="/login">Login</a>.'

@app.route('/login')
def login():
    """Initiates login process and redirects to Cognito."""
    redirect_uri = url_for('authorize', _external=True)
    return oauth.oidc.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    """Handles the callback from Cognito after successful authentication."""
    token = oauth.oidc.authorize_access_token()
    user = oauth.oidc.parse_id_token(token)
    session['user'] = user
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Logs the user out by clearing the session."""
    session.pop('user', None)
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
