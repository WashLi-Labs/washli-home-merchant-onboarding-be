from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import connect_to_database, close_database_connection
from app.routes import otp, merchants
from app.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await connect_to_database()
    yield
    # Shutdown
    await close_database_connection()


# Initialize FastAPI app
app = FastAPI(
    title="Merchant Onboarding API",
    description="""
    ## FastAPI Backend for Merchant Registration and Onboarding
    
    This API provides comprehensive merchant onboarding functionality including:
    
    ### Features
    - 📧 **Email OTP Verification**: Send and verify 4-digit OTP codes
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
    
    ### Google Maps Integration
    
    **Frontend Setup:**
    ```html
    <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY"></script>
    ```
    
    **JavaScript Implementation:**
    ```javascript
    // Initialize map
    const map = new google.maps.Map(document.getElementById('map'), {
      center: { lat: 6.9271, lng: 79.8612 },
      zoom: 13
    });
    
    // Add draggable marker
    const marker = new google.maps.Marker({
      position: map.getCenter(),
      map: map,
      draggable: true
    });
    
    // Capture location on marker drag
    marker.addListener('dragend', (event) => {
      const location = {
        lat: event.latLng.lat(),
        lng: event.latLng.lng()
      };
      // Send this location object with registration
    });
    ```
    
    ### Workflow
    
    1. **Send OTP** → `POST /api/v1/otp/send`
    2. **Verify OTP** → `POST /api/v1/otp/verify`
    3. **Register Merchant** → `POST /api/v1/merchants/register`
    
    ### Authentication
    Currently, no authentication is required. For production, implement JWT or OAuth2.
    
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
app.include_router(otp.router, prefix="/api/v1")
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
        "database": "connected"
    }
