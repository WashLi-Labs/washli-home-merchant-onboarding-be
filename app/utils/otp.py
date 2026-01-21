import random
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, Optional
from app.config import get_settings

settings = get_settings()

# In-memory OTP storage (for production, use Redis)
otp_storage: Dict[str, Dict] = {}


def generate_otp() -> str:
    """Generate a 4-digit OTP"""
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])


def store_otp(email: str, otp: str) -> None:
    """Store OTP in memory with expiry time"""
    expiry_time = datetime.now() + timedelta(minutes=settings.otp_expiry_minutes)
    otp_storage[email] = {
        'otp': otp,
        'expiry': expiry_time,
        'attempts': 0
    }


def verify_otp(email: str, otp: str) -> tuple[bool, str]:
    """
    Verify OTP for an email
    Returns: (success, message)
    """
    if email not in otp_storage:
        return False, "No OTP found for this email"
    
    stored_data = otp_storage[email]
    
    # Check expiry
    if datetime.now() > stored_data['expiry']:
        del otp_storage[email]
        return False, "OTP has expired"
    
    # Check attempts
    if stored_data['attempts'] >= 3:
        del otp_storage[email]
        return False, "Maximum verification attempts exceeded"
    
    # Verify OTP
    if stored_data['otp'] == otp:
        del otp_storage[email]
        return True, "OTP verified successfully"
    else:
        otp_storage[email]['attempts'] += 1
        remaining = 3 - otp_storage[email]['attempts']
        return False, f"Invalid OTP. {remaining} attempts remaining"


async def send_email_otp(email: str, otp: str) -> bool:
    """Send OTP via email"""
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Merchant Registration OTP"
        message["From"] = settings.from_email
        message["To"] = email
        
        # HTML content
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #f5f5f5; padding: 30px; border-radius: 10px;">
                    <h2 style="color: #333;">Merchant Registration Verification</h2>
                    <p style="font-size: 16px; color: #555;">
                        Thank you for registering as a merchant. Please use the following OTP to verify your email:
                    </p>
                    <div style="background-color: #fff; padding: 20px; text-align: center; border-radius: 5px; margin: 20px 0;">
                        <h1 style="color: #4CAF50; letter-spacing: 10px; margin: 0;">{otp}</h1>
                    </div>
                    <p style="font-size: 14px; color: #777;">
                        This OTP will expire in {settings.otp_expiry_minutes} minutes.
                    </p>
                    <p style="font-size: 14px; color: #777;">
                        If you didn't request this OTP, please ignore this email.
                    </p>
                </div>
            </body>
        </html>
        """
        
        # Attach HTML content
        part = MIMEText(html, "html")
        message.attach(part)
        
        # Send email
        await aiosmtplib.send(
            message,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_user,
            password=settings.smtp_password,
            start_tls=True
        )
        
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def clear_expired_otps():
    """Clear expired OTPs from storage"""
    current_time = datetime.now()
    expired_emails = [
        email for email, data in otp_storage.items()
        if current_time > data['expiry']
    ]
    for email in expired_emails:
        del otp_storage[email]
