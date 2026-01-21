# Washli Merchant Onboarding Backend

**Production-ready FastAPI backend for merchant registration and onboarding**

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
├─────────────────────────────────────────────────────────┤
│  Routes Layer:                                           │
│  ├─ /api/v1/merchants  → Merchant Registration          │
│  └─ /api/v1/otp        → Email OTP Verification         │
├─────────────────────────────────────────────────────────┤
│  Business Logic:                                         │
│  ├─ OTP Generation & Validation (In-Memory)             │
│  ├─ Email Service (Async SMTP)                          │
│  └─ Data Validation (Pydantic)                          │
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
│   ├── routes/                  # API endpoint handlers
│   │   ├── __init__.py
│   │   ├── merchants.py         # POST /api/v1/merchants/register
│   │   └── otp.py               # POST /api/v1/otp/send & verify
│   │
│   └── utils/                   # Business logic utilities
│       ├── __init__.py
│       └── otp.py               # OTP generation & email service
│
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 📂 File-by-File Explanation

### **Core Application Files**

#### `app/main.py` - Application Entry Point
- Creates FastAPI instance with auto-generated docs
- Includes API routers (merchants, otp)
- Configures CORS middleware
- Manages database lifecycle (startup/shutdown)

#### `app/config.py` - Configuration Management
- Loads environment variables from `.env` file
- Validates configuration using Pydantic Settings
- Provides database credentials, SMTP settings, SSL paths
- Uses singleton pattern for efficiency

---

### **Database Layer**

#### `app/database.py` - Database Connection
- Creates async SQLAlchemy engine with SSL support
- Manages connection pooling
- Provides session factory for dependency injection

#### `app/db_models.py` - Database Schema (ORM)
- Defines `Merchant` table structure
- Maps Python class to MySQL table
- Stores images as Base64 TEXT columns (no file system)

**Why separate from models.py?**
- `db_models.py` = Database schema (snake_case columns)
- `models.py` = API validation (camelCase JSON)
- Allows independent changes to API vs database

---

### **Data Validation Layer**

#### `app/models.py` - API Request/Response Validation
- Validates incoming JSON payloads using Pydantic
- Generates OpenAPI documentation
- Provides type safety for API contracts

**Purpose of `json_schema_extra`:**
- Provides example payloads for Swagger UI `/docs`
- **Only used for documentation**, not validation
- Helps developers see realistic API examples

---

### **Business Logic**

#### `app/routes/merchants.py` - Merchant Registration
- **Endpoint**: `POST /api/v1/merchants/register`
- Accepts registration form data
- Stores Base64 images directly in database TEXT columns
- Returns merchant ID on success

#### `app/routes/otp.py` - Email Verification
- **Endpoints**: 
  - `POST /api/v1/otp/send` - Generate and email OTP
  - `POST /api/v1/otp/verify` - Validate OTP code
- 4-digit OTP with 5-minute expiry
- Asynchronous email sending

#### `app/utils/otp.py` - OTP Business Logic
- Generates random 4-digit OTP codes
- In-memory storage with automatic expiry
- Async email sending via SMTP
- **Why in-memory?** Simple, fast, no external dependencies needed

---

### **Configuration Files**

#### `requirements.txt` - Python Dependencies
**Key packages:**
- `fastapi` - Web framework
- `sqlalchemy` + `aiomysql` - Async database ORM
- `pydantic` - Data validation
- `aiosmtplib` - Async email sending
- `cryptography` - SSL support

#### `.env.example` - Environment Template
- Template for environment variables
- **Must copy to `.env`** and fill with actual credentials
- Contains: Database credentials, SMTP settings, SSL paths

---

## 🚀 Quick Start

### **1. Environment Setup**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# Required: DB credentials, SMTP settings, SSL certificate path
```

### **2. Install Dependencies**
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### **3. Database Setup**
```sql
-- Create database
CREATE DATABASE washli_merchants 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER 'washli_app'@'%' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON washli_merchants.* TO 'washli_app'@'%';
FLUSH PRIVILEGES;
```

### **4. Create Tables**
```python
# Run this once to create tables
python -c "from app.database import Base, engine; import asyncio; asyncio.run(Base.metadata.create_all(bind=engine))"
```

### **5. Start Server**
```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 📡 API Endpoints

### **1. OTP Verification**

#### Send OTP
```http
POST /api/v1/otp/send
Content-Type: application/json

{
  "email": "merchant@example.com"
}
```

#### Verify OTP
```http
POST /api/v1/otp/verify
Content-Type: application/json

{
  "email": "merchant@example.com",
  "otp": "1234"
}
```

### **2. Merchant Registration**
```http
POST /api/v1/merchants/register
Content-Type: application/json

{
  "email": "merchant@example.com",
  "phoneNumber": "+94771234567",
  "merchantType": "Laundromat",
  "outletName": "Clean & Fresh Laundry",
  "outletAddress": "123 Main Street",
  "city": "Colombo",
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
  "taxRegistered": true,
  "vatRegistered": false,
  "nicFront": "base64_encoded_image_string",
  "nicBack": "base64_encoded_image_string",
  "bankName": "Commercial Bank",
  "branchName": "Colombo Main",
  "accountNumber": "1234567890",
  "beneficiaryName": "John Doe"
}
```

---

## 🧪 Testing

### **Interactive API Documentation**
```bash
# Swagger UI (interactive)
http://localhost:8000/docs

# ReDoc (alternative)
http://localhost:8000/redoc

# OpenAPI JSON
http://localhost:8000/openapi.json
```

### **Health Check**
```bash
curl http://localhost:8000/
# Response: {"message": "Merchant Onboarding API", "version": "1.0.0", "status": "active"}

curl http://localhost:8000/health
# Response: {"status": "healthy", "database": "connected"}
```

---

## 📊 Technology Stack

| Component           | Technology         | Version    |
|--------------------|--------------------|------------|
| Web Framework      | FastAPI            | 0.109.0    |
| Server             | Uvicorn            | 0.27.0     |
| Database           | MySQL              | 8.0+       |
| ORM                | SQLAlchemy (Async) | 2.0.25     |
| DB Driver          | aiomysql           | 0.2.0      |
| Validation         | Pydantic           | 2.5.3      |
| Email              | aiosmtplib         | 3.0.1      |
| Security           | cryptography       | 41.0.7     |

---

## 🎯 Design Decisions

### **Why Base64 Images in Database?**
✅ **Pros:**
- No file system dependencies (simpler deployment)
- Atomic transactions (images + data together)
- No file path management issues
- Docker-friendly (no volume mounts needed)

⚠️ **Cons:**
- Larger database size (~33% overhead)
- Slower queries if images are large

**Recommendation:** Good for small-medium scale. For large scale, use cloud storage (S3, Azure Blob).

### **Why In-Memory OTP Storage?**
✅ **Pros:**
- Simple implementation
- Fast access
- No external dependencies (Redis not needed)
- Automatic cleanup with TTL

⚠️ **Cons:**
- Lost on server restart (acceptable for OTP)
- Not suitable for multi-server deployments

**Recommendation:** Use Redis for production multi-server setup.

### **Why Async SQLAlchemy?**
✅ **Benefits:**
- Handle more concurrent requests
- Non-blocking I/O for email sending
- Better resource utilization
- Scales well with high traffic

---

## 🔒 Security Best Practices

### **Environment Variables**
- ✅ Never commit `.env` file
- ✅ Use strong database passwords
- ✅ Enable SSL for database (`DB_SSL_ENABLED=true`)
- ✅ Set production SMTP credentials

### **CORS Configuration**
```python
# In production, specify exact origins
allow_origins=["https://yourfrontend.com"]  # Not ["*"]
```

### **SSL/TLS**
- ✅ Use HTTPS in production
- ✅ Place `ca.pem` certificate in project root
- ✅ Set `DB_SSL_ENABLED=true` in `.env`

### **Rate Limiting** (Recommended)
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/v1/otp/send")
@limiter.limit("5/minute")
async def send_otp():
    ...
```

---

## 🐛 Troubleshooting

### **Database Connection Failed**
```bash
# Check MySQL is running
mysql -u washli_app -p washli_merchants

# Verify SSL certificate exists
ls -la ca.pem

# Test connection
python -c "from app.database import connect_to_database; import asyncio; asyncio.run(connect_to_database())"
```

### **OTP Email Not Sending**
```bash
# Check SMTP credentials in .env
# Verify SMTP settings (port 587 for TLS, 465 for SSL)
# Test SMTP connection
python -c "import aiosmtplib; import asyncio; asyncio.run(aiosmtplib.SMTP(hostname='smtp.gmail.com', port=587).connect())"
```

### **Import Errors**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📈 Production Deployment

### **Using Docker**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### **Using Nginx Reverse Proxy**
```nginx
server {
    listen 80;
    server_name api.example.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **Environment Variables (Production)**
```bash
# Database
DB_SSL_ENABLED=true
DB_HOST=production-mysql.example.com

# SMTP
SMTP_HOST=smtp.gmail.com
SMTP_USER=noreply@example.com
SMTP_PASSWORD=app_specific_password
```

---

## 📝 License

Copyright © 2026 Washli. All rights reserved.

---

## 📞 Support

- **Documentation**: http://localhost:8000/docs
- **Issues**: Create GitHub issue
- **Email**: support@washli.com
