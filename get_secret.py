import os
from dotenv import load_dotenv

load_dotenv()
google_id = os.getenv("google_client_id")
google_secret = os.getenv("google_client_secret")
app_secret_key = os.getenv("session_secret")