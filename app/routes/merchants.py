from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timezone
import base64
import uuid
import re
from app.models import MerchantRegistration, MerchantResponse
from app.firebase import get_firestore, get_storage_bucket

router = APIRouter(prefix="/merchants", tags=["Merchant Management"])


def upload_base64_to_storage(base64_str: str, folder: str, filename_prefix: str) -> str:
    """
    Uploads a Base64 string to Firebase Storage and returns the public URL.
    """
    if not base64_str or not isinstance(base64_str, str) or not base64_str.startswith("data:"):
        return base64_str # Not a base64 image or already a URL

    try:
        # Extract format and data
        # Format: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...
        match = re.match(r'data:(.*?);base64,(.*)', base64_str)
        if not match:
            return base64_str
            
        content_type, encoded_data = match.groups()
        extension = content_type.split('/')[-1]
        
        # Decode data
        file_data = base64.b64decode(encoded_data)
        
        # Generate unique filename
        filename = f"{folder}/{filename_prefix}_{uuid.uuid4().hex}.{extension}"
        
        # Upload to Storage
        bucket = get_storage_bucket()
        blob = bucket.blob(filename)
        blob.upload_from_string(file_data, content_type=content_type)
        
        # Make public and get URL
        # Note: In production you might want to use signed URLs or Firebase's download tokens
        blob.make_public()
        return blob.public_url
        
    except Exception as e:
        print(f"Failed to upload to storage: {e}")
        return base64_str


@router.post(
    "/register",
    response_model=MerchantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register New Merchant",
    description="""
    Register a new merchant. Images are uploaded to Firebase Storage and URLs are stored in Firestore.
    
    **Process:**
    1. Validate required fields
    2. Upload all Base64 images to Firebase Storage
    3. Store merchant metadata and image URLs in Firestore
    4. Return success status
    """
)
async def register_merchant(
    merchant: MerchantRegistration
):
    """Register a new merchant via Firebase Storage & Firestore"""
    try:
        # Validate email verification
        if not merchant.isEmailVerified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email must be verified before registration"
            )
        
        firestore_db = get_firestore()
        
        # Check if email already exists
        existing_docs = firestore_db.collection('merchants').where('email', '==', merchant.email).limit(1).get()
        if len(list(existing_docs)) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Merchant with this email already exists"
            )
        
        # Create a new document reference
        new_doc_ref = firestore_db.collection('merchants').document()
        merchant_id = new_doc_ref.id
        
        # Prepare data
        merchant_data = merchant.model_dump()
        
        # Define fields to upload to storage
        image_fields = [
            'outletLogo', 'brDocument', 'taxCertificate', 'tdlDocument', 
            'nicFront', 'nicBack', 'menuDocument', 'itemImages', 'bankStatement'
        ]
        
        # Process image uploads
        for field in image_fields:
            field_value = merchant_data.get(field)
            if field_value:
                print(f"Uploading {field} to storage...")
                if isinstance(field_value, list):
                    # Handle multiple images (e.g., itemImages)
                    urls = []
                    for i, img_data in enumerate(field_value):
                        url = upload_base64_to_storage(
                            img_data, 
                            folder=f"merchants/{merchant.email}", 
                            filename_prefix=f"{field}_{i}"
                        )
                        urls.append(url)
                    merchant_data[field] = urls
                else:
                    # Handle single image
                    merchant_data[field] = upload_base64_to_storage(
                        field_value, 
                        folder=f"merchants/{merchant.email}", 
                        filename_prefix=field
                    )
        
        merchant_data['status'] = 'pending'
        merchant_data['createdAt'] = datetime.now(timezone.utc).isoformat()
        merchant_data['merchantId'] = merchant_id
        
        # Save to Firestore
        new_doc_ref.set(merchant_data)
        
        return MerchantResponse(
            success=True,
            message="Merchant registered successfully with document storage",
            merchantId=merchant_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error registering merchant: {str(e)}"
        )


