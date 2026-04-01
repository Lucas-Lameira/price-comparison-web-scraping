import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv

load_dotenv()

_initialized = False

def init_firebase():
    global _initialized
    if _initialized:
        return True

    creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    db_url = os.getenv("FIREBASE_DATABASE_URL")

    if not creds_json or not db_url:
        print("Firebase credentials or Database URL missing from environment variables.")
        return False

    try:
        # Parse the JSON string from the environment variable
        cert_dict = json.loads(creds_json)
        cred = credentials.Certificate(cert_dict)
        firebase_admin.initialize_app(cred, {
            'databaseURL': db_url.strip("/")
        })
        _initialized = True
        print("Firebase initialized successfully.")
        return True
    except Exception as e:
        print(f"Failed to initialize Firebase: {e}")
        return False

def get_previous_prices():
    """Retrieve the 'prices' node from Firebase Realtime Database."""
    if not init_firebase():
        return {}
    
    try:
        ref = db.reference('/prices')
        data = ref.get()
        if data is None:
            return {}
        return data
    except Exception as e:
        print(f"Error reading from Firebase: {e}")
        return {}


def save_previous_prices(prices_dict):
    """Save the updated prices to the 'prices' node in Firebase."""
    if not init_firebase():
        return False
        
    try:
        ref = db.reference('/prices')
        ref.set(prices_dict)
        print("Successfully saved prices to Firebase.")
        return True
    except Exception as e:
        print(f"Error writing to Firebase: {e}")
        return False
