from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime


class Location(BaseModel):
    """Geographic location coordinates"""
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")


class OperatingHours(BaseModel):
    """Operating hours for a specific day"""
    day: str = Field(..., description="Day of the week")
    isOpen: bool = Field(..., description="Whether the outlet is open")
    openTime: Optional[str] = Field(None, description="Opening time (HH:MM)")
    closeTime: Optional[str] = Field(None, description="Closing time (HH:MM)")
    
    @validator('openTime', 'closeTime')
    def validate_time_format(cls, v):
        if v and ':' not in v:
            raise ValueError('Time must be in HH:MM format')
        return v


class MerchantRegistration(BaseModel):
    """Complete merchant registration data"""
    # Contact Information
    email: EmailStr = Field(..., description="Merchant email address")
    phoneNumber: str = Field(..., description="Merchant phone number")
    
    # Business Information
    merchantType: str = Field(..., description="Type of merchant (e.g., Laundromat)")
    outletName: str = Field(..., description="Name of the outlet")
    outletAddress: str = Field(..., description="Physical address")
    city: str = Field(..., description="City")
    # region removed
    location: Location = Field(..., description="GPS coordinates")
    outletLogo: Optional[str] = Field(None, description="Base64 encoded logo")
    
    # Marketing
    howDidYouHear: str = Field(..., description="How the merchant heard about the service")
    
    # Email Verification
    isEmailVerified: bool = Field(False, description="Email verification status")
    
    # Owner Information
    ownerName: str = Field(..., description="Owner full name")
    ownerPhone: str = Field(..., description="Owner phone number")
    ownerEmail: EmailStr = Field(..., description="Owner email")
    
    # Manager Information (Optional)
    managerName: Optional[str] = Field(None, description="Manager full name")
    managerPhone: Optional[str] = Field(None, description="Manager phone number")
    managerEmail: Optional[EmailStr] = Field(None, description="Manager email")
    
    # Operating Hours
    operatingHours: List[OperatingHours] = Field(..., description="Weekly operating hours")
    
    # Business Registration
    businessRegistered: bool = Field(..., description="Is business registered")
    parentName: Optional[str] = Field(None, description="Parent company name")
    brNumber: Optional[str] = Field(None, description="Business registration number")
    brDocument: Optional[str] = Field(None, description="Base64 encoded BR document")
    
    # Tax Information
    taxRegistered: bool = Field(..., description="Is tax registered")
    tinNumber: Optional[str] = Field(None, description="Tax identification number")
    taxCertificate: Optional[str] = Field(None, description="Base64 encoded tax certificate")
    tdlDocument: Optional[str] = Field(None, description="Base64 encoded TDL document")
    
    # VAT Information
    vatRegistered: bool = Field(..., description="Is VAT registered")
    vatNumber: Optional[str] = Field(None, description="VAT number")
    
    # Identity Documents
    nicFront: str = Field(..., description="Base64 encoded NIC front")
    nicBack: str = Field(..., description="Base64 encoded NIC back")
    
    # Business Documents
    menuDocument: Optional[str] = Field(None, description="Base64 encoded menu")
    
    # Images
    hasImages: str = Field(..., description="Whether outlet has images")
    itemImages: Optional[List[str]] = Field(None, description="Base64 encoded item images")
    
    # Banking Information
    beneficiaryName: str = Field(..., description="Bank account beneficiary name")
    accountNumber: str = Field(..., description="Bank account number")
    bankName: str = Field(..., description="Bank name")
    branchName: str = Field(..., description="Branch name")
    branchCode: Optional[str] = Field(None, description="Branch code")
    bankStatement: Optional[str] = Field(None, description="Base64 encoded bank statement")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "merchant@example.com",
                "howDidYouHear": "Social Media",
                "region": "Western",
                "merchantType": "Laundromat",
                "outletName": "Clean & Fresh Laundry",
                "outletAddress": "123 Main Street",
                "city": "Colombo",
                "phoneNumber": "+94771234567",
                "location": {
                    "lat": 6.9271,
                    "lng": 79.8612
                },
                "isEmailVerified": True,
                "ownerName": "John Doe",
                "ownerPhone": "+94771234567",
                "ownerEmail": "owner@example.com",
                "operatingHours": [
                    {
                        "day": "Monday",
                        "isOpen": True,
                        "openTime": "08:00",
                        "closeTime": "18:00"
                    }
                ],
                "businessRegistered": True,
                "brNumber": "BR123456",
                "taxRegistered": True,
                "vatRegistered": False,
                "nicFront": "base64_encoded_string",
                "nicBack": "base64_encoded_string",
                "hasImages": "Yes",
                "beneficiaryName": "John Doe",
                "accountNumber": "1234567890",
                "bankName": "Commercial Bank",
                "branchName": "Colombo Main",
                "branchCode": "001"
            }
        }


class MerchantResponse(BaseModel):
    """Response after merchant registration"""
    success: bool = Field(..., description="Registration success status")
    message: str = Field(..., description="Response message")
    merchantId: Optional[str] = Field(None, description="Generated merchant ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Merchant registered successfully",
                "merchantId": "65abc123def456789"
            }
        }
