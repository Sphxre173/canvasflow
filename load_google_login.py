from authlib.integrations.flask_client import OAuth
import flask
import os
from get_secret import google_id, google_secret
from dotenv import load_dotenv

load_dotenv()
google_id = os.getenv("google_client_id")
google_secret = os.getenv("google_client_secret")

def register_oath(app:flask.Flask):
    oauth = OAuth(app)
    google = oauth.register(
        name='google',
        client_id= str(google_id),
        client_secret=str(google_secret),
        access_token_url='https://oauth2.googleapis.com/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )
    return google