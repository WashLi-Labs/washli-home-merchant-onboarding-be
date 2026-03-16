import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import firestore as gc_firestore
from app.config import get_settings

settings = get_settings()
_db = None

def init_firebase():
    global _db
    if not firebase_admin._apps:
        if settings.firebase_credentials_path:
            cred = credentials.Certificate(settings.firebase_credentials_path)
            app = firebase_admin.initialize_app(cred)
            print(f"✓ Connected to Firebase (Firestore)")
        else:
            print("Warning: FIREBASE_CREDENTIALS_PATH not set in environment. Using default application credentials.")
            app = firebase_admin.initialize_app()
    else:
        app = firebase_admin.get_app()
        
    # Get project info
    project_id = app.project_id or cred.project_id if 'cred' in locals() else None
    
    # Initialize the Firestore client with the named database
    _db = gc_firestore.Client(
        project=project_id,
        database=settings.firestore_database_id,
        credentials=app.credential.get_credential() if app.credential else None
    )

def get_firestore():
    if _db is None:
        init_firebase()
    return _db
