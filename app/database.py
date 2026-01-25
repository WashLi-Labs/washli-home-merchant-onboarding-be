from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
import os
import ssl
from app.config import get_settings

settings = get_settings()

# Create base class for models
Base = declarative_base()

# Database engine
engine = None
async_session_maker = None


def get_database_url() -> str:
    """Construct MySQL database URL"""
    return (
        f"mysql+aiomysql://{settings.db_user}:{settings.db_password}"
        f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )


def get_ssl_args() -> dict:
    """Get SSL configuration for MySQL connection"""
    if not settings.db_ssl_enabled:
        return {}
    
    ssl_ca_path = settings.db_ssl_ca
    
    # Check if SSL certificate exists
    if not os.path.exists(ssl_ca_path):
        print(f"Warning: SSL certificate not found at {ssl_ca_path}")
        print("Proceeding without SSL. Set DB_SSL_ENABLED=false to disable this warning.")
        return {}
    
    # Create SSL context for aiomysql
    ssl_context = ssl.create_default_context(cafile=ssl_ca_path)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    
    return {
        "ssl": ssl_context
    }


async def connect_to_database():
    """Initialize database connection"""
    global engine, async_session_maker
    
    database_url = get_database_url()
    ssl_args = get_ssl_args()
    
    # Create async engine
    engine = create_async_engine(
        database_url,
        echo=False,  # Set to True for SQL query logging
        poolclass=NullPool,
        connect_args=ssl_args
    )
    
    # Create session maker
    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print(f"✓ Connected to MySQL database: {settings.db_name}")


async def close_database_connection():
    """Close database connection"""
    global engine
    if engine:
        await engine.dispose()
        print("✓ Closed MySQL connection")


async def get_session() -> AsyncSession:
    """Get database session"""
    async with async_session_maker() as session:
        yield session
