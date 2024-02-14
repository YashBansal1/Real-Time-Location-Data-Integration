from functools import wraps
from flask import request, jsonify, redirect, url_for, session
from flask_oauthlib.client import OAuth

def authenticate(username, password):
    """Real authentication logic using OAuth 2.0 with Google."""
    # This function should verify the credentials against your user database
    # For demonstration purposes, we'll return True if username and password match "admin" and "password"
    if username == 'admin' and password == 'password':
        return True
    return False

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

oauth = OAuth()

google = oauth.remote_app(
    'google',
    consumer_key='your_google_client_id',
    consumer_secret='your_google_client_secret',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

def login():
    return google.authorize(callback=url_for('authorized', _external=True))

def authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return jsonify({'message': 'Access denied: reason={}, error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )}), 401
    
    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo')
    session['username'] = user_info.data['email']
    return redirect(url_for('index'))

def logout():
    session.pop('username', None)
    session.pop('google_token', None)
    return redirect(url_for('index'))
