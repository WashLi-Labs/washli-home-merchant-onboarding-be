from fastapi import APIRouter, HTTPException, status
from app.models import SendOTPRequest, VerifyOTPRequest, OTPResponse
from app.utils.otp import generate_otp, store_otp, verify_otp, send_email_otp

router = APIRouter(prefix="/otp", tags=["OTP Management"])


@router.post(
    "/send",
    response_model=OTPResponse,
    summary="Send OTP to Email",
    description="""
    Send a 4-digit OTP to the specified email address.
    
    **Process:**
    1. Generate a random 4-digit OTP
    2. Store it in memory with expiry time
    3. Send via email
    
    **Note:** OTP expires in 5 minutes by default
    """
)
async def send_otp(request: SendOTPRequest):
    """Send OTP to email address"""
    try:
        # Generate OTP
        otp = generate_otp()
        
        # Store OTP in memory
        store_otp(request.email, otp)
        
        # Send OTP via email
        email_sent = await send_email_otp(request.email, otp)
        
        if not email_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send OTP email. Please check email configuration."
            )
        
        return OTPResponse(
            success=True,
            message=f"OTP sent successfully to {request.email}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending OTP: {str(e)}"
        )


@router.post(
    "/verify",
    response_model=OTPResponse,
    summary="Verify OTP",
    description="""
    Verify the OTP sent to an email address.
    
    **Validation Rules:**
    - OTP must be 4 digits
    - Maximum 3 verification attempts
    - OTP expires after configured time (default 5 minutes)
    
    **Response:**
    - Success: OTP is valid and will be removed from storage
    - Failure: Invalid OTP or expired
    """
)
async def verify_otp_endpoint(request: VerifyOTPRequest):
    """Verify OTP for email address"""
    try:
        # Verify OTP
        success, message = verify_otp(request.email, request.otp)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        return OTPResponse(
            success=True,
            message=message
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying OTP: {str(e)}"
        )
