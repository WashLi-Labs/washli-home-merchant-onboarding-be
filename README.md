# Washli Merchant Onboarding Backend

**Production-ready FastAPI backend for merchant registration.**

This project acts as the backend service for onboarding new merchants to the Washli platform. It handles the submission of comprehensive merchant details, including business information, location data, operating hours, and document proofs (as Base64 encoded images).

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
1│  Routes Layer:                                           │
│  └─ /api/v1/merchants  → Merchant Registration          │
├─────────────────────────────────────────────────────────┤
│  Data Layer:                                             │
│  ├─ SQLAlchemy ORM (Async)                              │
│  └─ MySQL 8.0+ with SSL                                 │
└─────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
washli-home-merchant-onboarding-be/
│
├── app/                          # Application package
│   ├── __init__.py              # Package initializer
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Environment configuration
│   ├── database.py              # Database connection management
│   ├── db_models.py             # SQLAlchemy ORM models
│   ├── models.py                # Pydantic validation models
│   │
│   └── routes/                  # API endpoint handlers
│       ├── __init__.py
│       └── merchants.py         # POST /api/v1/merchants/register
│
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 📂 Key Concepts

### **1. Base64 Image Storage**
Instead of using a file system or external object storage (like S3), this service accepts images (logos, documents, NICs) as **Base64 encoded strings** within the JSON payload. These strings are stored directly in `TEXT` or `LONGTEXT` columns in the MySQL database.
- **Frontend Resp:** Convert files to Base64 strings before sending.
- **Backend Resp:** Store and retrieve strings as is.

### **2. Pydantic Models (`json_schema_extra`)**
In `app/models.py`, you will see a `Config` class with `json_schema_extra`. 
- **Purpose**: This dictionary provides the **Example Value** you see in the Swagger UI (`/docs`). 
- **Usage**: It helps frontend developers understand exactly what the payload should look like without guessing. It **does not** affect the actual validation logic; it is purely for documentation.

---

## 🚀 Quick Start

### **1. Environment Setup**

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# Required: DB credentials, SSL certificate path (if enabled)
```

### **2. Install Dependencies**

```bash
# Create virtual environment
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### **3. Database Setup**

Ensure you have a MySQL database running.

```sql
-- Create database
CREATE DATABASE merchant_onboarding;
```

The application will automatically create the necessary tables on startup.

### **4. Start Server**

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📡 API Endpoints

### **Merchant Registration**

**POST** `/api/v1/merchants/register`

Submit a new merchant registration.

**Request Body Example:**

```json
{
  "email": "merchant@example.com",
  "howDidYouHear": "Social Media",
  "merchantType": "Laundromat",
  "outletName": "Clean & Fresh Laundry",
  "outletAddress": "123 Main Street",
  "city": "Colombo",
  "phoneNumber": "+94771234567",
  "location": {
    "lat": 6.9271,
    "lng": 79.8612
  },
  "isEmailVerified": true,
  "ownerName": "John Doe",
  "ownerPhone": "+94771234567",
  "ownerEmail": "owner@example.com",
  "operatingHours": [
    {
      "day": "Monday",
      "isOpen": true,
      "openTime": "08:00",
      "closeTime": "18:00"
    }
  ],
  "businessRegistered": true,
  "brNumber": "BR123456",
  "brDocument": "base64...",
  "taxRegistered": true,
  "vatRegistered": false,
  "nicFront": "base64...",
  "nicBack": "base64...",
  "hasImages": "Yes",
  "beneficiaryName": "John Doe",
  "accountNumber": "1234567890",
  "bankName": "Commercial Bank",
  "branchName": "Colombo Main",
  "branchCode": "001"
}
```

---

## 🧪 Testing

### **Interactive API Documentation**

Visit **[http://localhost:8000/docs](http://localhost:8000/docs)** to see the Swagger UI. You can try out the API directly from your browser.

---

## 📝 License

Copyright © 2026 Washli. All rights reserved.
