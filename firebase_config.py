import firebase_admin
from firebase_admin import credentials, storage
import os

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        # Check if Firebase is already initialized
        firebase_admin.get_app()
    except ValueError:
        # Firebase not initialized, so initialize it
        # You need to download your Firebase service account key JSON file
        # and place it in the project root as 'firebase-service-account.json'
        cred_path = os.path.join(os.path.dirname(__file__), 'firebase-service-account.json')

        if os.path.exists(cred_path):
            try:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred, {
                    'storageBucket': 'demo-project.appspot.com'  # Demo bucket
                })
                print("Firebase initialized successfully!")
            except Exception as e:
                print(f"Firebase initialization failed: {e}")
                return False
        else:
            print("Firebase service account key not found. Audio storage will be disabled.")
            return False

    return True

def upload_audio_to_firebase(audio_data, filename):
    """Upload audio data to Firebase Storage"""
    try:
        bucket = storage.bucket()
        blob = bucket.blob(f'audio/{filename}')
        blob.upload_from_string(audio_data, content_type='audio/webm')
        blob.make_public()
        return blob.public_url
    except Exception as e:
        print(f"Error uploading to Firebase: {e}")
        return None

def download_audio_from_firebase(url):
    """Download audio from Firebase Storage URL"""
    try:
        import requests
        response = requests.get(url)
        return response.content
    except Exception as e:
        print(f"Error downloading from Firebase: {e}")
        return None