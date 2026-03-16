from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from app.models import MerchantRegistration, MerchantResponse
from app.database import get_session
from app.db_models import Merchant
from app.firebase import get_firestore

router = APIRouter(prefix="/merchants", tags=["Merchant Management"])


@router.post(
    "/register",
    response_model=MerchantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register New Merchant",
    description="""
    Register a new merchant with complete business information.
    
    **Process:**
    1. Validate all required fields
    2. Store Base64 encoded images directly in database
    3. Return merchant ID
    
    **Image Handling:**
    - Images should be sent as Base64 encoded strings
    - Images are stored directly in the database (no file system storage)
    - Frontend should handle image compression before sending
    - Supported formats: PNG, JPG, PDF (as Base64)
    
    **Validation:**
    - Email must be verified (isEmailVerified = true)
    - Location coordinates are required
    - Operating hours for all days
    
    **Required Documents:**
    - NIC Front and Back (mandatory)
    - Business Registration (if businessRegistered = true)
    - Tax Certificate (if taxRegistered = true)
    - Bank Statement (optional)
    """
)
async def register_merchant(
    merchant: MerchantRegistration,
    db: AsyncSession = Depends(get_session)
):
    """Register a new merchant"""
    try:
        # Validate email verification
        if not merchant.isEmailVerified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email must be verified before registration"
            )
        
        # Check if email already exists
        stmt = select(Merchant).where(Merchant.email == merchant.email)
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Merchant with this email already exists"
            )
        
        # Create merchant record - store Base64 images directly
        new_merchant = Merchant(
            email=merchant.email,
            phone_number=merchant.phoneNumber,
            merchant_type=merchant.merchantType,
            outlet_name=merchant.outletName,
            outlet_address=merchant.outletAddress,
            city=merchant.city,
            # region removed
            location=merchant.location.model_dump(),
            outlet_logo=merchant.outletLogo,  # Base64 string
            how_did_you_hear=merchant.howDidYouHear,
            is_email_verified=merchant.isEmailVerified,
            owner_name=merchant.ownerName,
            owner_phone=merchant.ownerPhone,
            owner_email=merchant.ownerEmail,
            manager_name=merchant.managerName,
            manager_phone=merchant.managerPhone,
            manager_email=merchant.managerEmail,
            operating_hours=[hour.model_dump() for hour in merchant.operatingHours],
            business_registered=merchant.businessRegistered,
            parent_name=merchant.parentName,
            br_number=merchant.brNumber,
            br_document=merchant.brDocument,  # Base64 string
            tax_registered=merchant.taxRegistered,
            tin_number=merchant.tinNumber,
            tax_certificate=merchant.taxCertificate,  # Base64 string
            tdl_document=merchant.tdlDocument,  # Base64 string
            vat_registered=merchant.vatRegistered,
            vat_number=merchant.vatNumber,
            nic_front=merchant.nicFront,  # Base64 string
            nic_back=merchant.nicBack,  # Base64 string
            menu_document=merchant.menuDocument,  # Base64 string
            has_images=merchant.hasImages,
            item_images=merchant.itemImages,  # Base64 string
            beneficiary_name=merchant.beneficiaryName,
            account_number=merchant.accountNumber,
            bank_name=merchant.bankName,
            branch_name=merchant.branchName,
            branch_code=merchant.branchCode,
            bank_statement=merchant.bankStatement,  # Base64 string
            status='pending'
        )
        
        db.add(new_merchant)
        await db.commit()
        await db.refresh(new_merchant)
        
        # Save to Firebase Firestore
        try:
            firestore_db = get_firestore()
            # We don't save large base64 images to Firestore to save costs/storage limits,
            # or you can include them by just dumping `merchant.model_dump()`.
            # Let's save a condensed version
            merchant_data = merchant.model_dump(exclude={
                'outletLogo', 'brDocument', 'taxCertificate', 'tdlDocument', 
                'nicFront', 'nicBack', 'menuDocument', 'itemImages', 'bankStatement'
            })
            merchant_data['sql_id'] = str(new_merchant.id)
            merchant_data['status'] = 'pending'
            merchant_data['createdAt'] = datetime.now(timezone.utc).isoformat()
            
            # Using email as document ID, or using auto-generated
            firestore_db.collection('merchants').document(merchant.email).set(merchant_data)
        except Exception as fb_err:
            print(f"Warning: Failed to sync to Firestore: {fb_err}")
            # we continue even if Firebase fails, or you could raise an exception
        
        return MerchantResponse(
            success=True,
            message="Merchant registered successfully",
            merchantId=str(new_merchant.id)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error registering merchant: {str(e)}"
        )
