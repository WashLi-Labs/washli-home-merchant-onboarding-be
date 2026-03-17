from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.firebase import init_firebase
from app.routes import merchants
from app.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    init_firebase()
    yield
    # Shutdown



# Initialize FastAPI app
app = FastAPI(
    title="Merchant Onboarding API",
    lifespan=lifespan,
    description="""
    ## FastAPI Backend for Merchant Registration and Onboarding
    
    This API provides merchant onboarding functionality including:
    
    ### Features
    - 📝 **Merchant Registration**: Complete merchant registration with document upload
    - 📍 **Location Tracking**: Support for GPS coordinates via Google Maps
    - 📸 **Image Handling**: Store Base64 encoded images directly in database
    
    ### Image Upload Guide
    
    **Frontend Implementation:**
    ```javascript
    // Convert file to Base64
    const fileToBase64 = (file) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
      });
    };
    
    // Usage
    const base64Image = await fileToBase64(imageFile);
    // Send base64Image in the request body
    ```
    
    **Backend Processing:**
    - Receives Base64 encoded images
    - Stores directly in MySQL database as TEXT
    - No file system dependencies
    - Images retrieved with merchant data
    
    ### Workflow
    
    1. **Register Merchant** → `POST /api/v1/merchants/register`
    
    ### Error Handling
    All endpoints return standard HTTP status codes:
    - `200/201`: Success
    - `400`: Bad Request (validation errors)
    - `404`: Not Found
    - `500`: Internal Server Error
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "API Support",
        "email": "support@yourcompany.com",
    },
    license_info={
        "name": "MIT License",
    }
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(merchants.router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Merchant Onboarding API",
        "version": "1.0.0",
        "status": "active",
        "documentation": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "firebase": "connected"
    }
