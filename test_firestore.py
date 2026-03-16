from app.firebase import init_firebase, get_firestore

def run_test():
    print("Initializing Firebase...")
    init_firebase()
    
    # Get the firestore client
    db = get_firestore()
    
    print("Writing a test document to the 'merchant-onboarding' database...")
    # Reference to a test collection and document
    doc_ref = db.collection('test_collection').document('test_doc')
    
    # Write data
    doc_ref.set({
        'message': 'Hello from FastAPI!',
        'status': 'Connected successfully'
    })
    print("✓ Successfully wrote to Firestore!")
    
    # Read the data back
    print("Reading the document back...")
    doc = doc_ref.get()
    
    if doc.exists:
        print(f"✓ Success! Document data: {doc.to_dict()}")
    else:
        print("❌ Failed to read document.")

if __name__ == "__main__":
    run_test()