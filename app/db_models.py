from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, JSON
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.sql import func
from app.database import Base


class Merchant(Base):
    """Merchant table - stores all merchant registration data"""
    __tablename__ = "merchant_registrations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Contact Information
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    
    # Business Information
    merchant_type = Column(String(100), nullable=False)
    outlet_name = Column(String(255), nullable=False)
    outlet_address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    # region removed
    
    # Location (stored as JSON)
    location = Column(JSON, nullable=False)  # {"lat": 6.9271, "lng": 79.8612}
    
    outlet_logo = Column(LONGTEXT)  # Base64 encoded image
    
    # Marketing
    how_did_you_hear = Column(String(100), nullable=False)
    
    # Email Verification
    is_email_verified = Column(Boolean, default=False)
    
    # Owner Information
    owner_name = Column(String(255), nullable=False)
    owner_phone = Column(String(20), nullable=False)
    owner_email = Column(String(255), nullable=False)
    
    # Manager Information
    manager_name = Column(String(255))
    manager_phone = Column(String(20))
    manager_email = Column(String(255))
    
    # Operating Hours (stored as JSON array)
    operating_hours = Column(JSON, nullable=False)
    
    # Business Registration
    business_registered = Column(Boolean, nullable=False)
    parent_name = Column(String(255))
    br_number = Column(String(100))
    br_document = Column(LONGTEXT)  # Base64 encoded document
    
    # Tax Information
    tax_registered = Column(Boolean, nullable=False)
    tin_number = Column(String(100))
    tax_certificate = Column(LONGTEXT)  # Base64 encoded certificate
    tdl_document = Column(LONGTEXT)  # Base64 encoded document
    
    # VAT Information
    vat_registered = Column(Boolean, nullable=False)
    vat_number = Column(String(100))
    
    # Identity Documents
    nic_front = Column(LONGTEXT, nullable=False)  # Base64 encoded image
    nic_back = Column(LONGTEXT, nullable=False)  # Base64 encoded image
    
    # Business Documents
    menu_document = Column(LONGTEXT)  # Base64 encoded document
    
    # Images
    has_images = Column(String(10), nullable=False)
    item_images = Column(LONGTEXT)  # Base64 encoded images
    
    # Banking Information
    beneficiary_name = Column(String(255), nullable=False)
    account_number = Column(String(50), nullable=False)
    bank_name = Column(String(255), nullable=False)
    branch_name = Column(String(255), nullable=False)
    branch_code = Column(String(100))
    bank_statement = Column(LONGTEXT)  # Base64 encoded statement
    
    # Status and Metadata
    status = Column(String(20), default='pending', index=True)  # pending, approved, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
