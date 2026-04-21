"""
Database connection and configuration for MongoDB with SQLite fallback
"""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging
from app.core.config import settings
from app.core.database_fallback import get_fallback_database

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    database = None
    is_fallback = False

db = Database()

async def connect_to_mongo():
    """Create database connection with fallback to SQLite"""
    try:
        # Try MongoDB connection first
        logger.info("[DB] Attempting to connect to MongoDB Atlas...")
        
        # MongoDB connection with SSL/TLS configuration
        db.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            maxPoolSize=10,
            minPoolSize=1,
            serverSelectionTimeoutMS=8000,  # Reduced timeout for faster fallback
            connectTimeoutMS=8000,
            socketTimeoutMS=15000,
            # SSL/TLS configuration
            tls=True,
            tlsAllowInvalidCertificates=False,
            tlsAllowInvalidHostnames=False,
            # Retry configuration
            retryWrites=True,
            retryReads=True
        )
        
        # Test the connection
        await db.client.admin.command('ping')
        
        db.database = db.client[settings.DATABASE_NAME]
        db.is_fallback = False
        
        # Create indexes for better performance
        await create_indexes()
        
        logger.info("[OK] Connected to MongoDB Atlas successfully")
        
    except Exception as e:
        logger.warning(f"[WARN] MongoDB connection failed: {e}")
        logger.info("[DB] Falling back to SQLite database for development...")
        
        try:
            # Use SQLite fallback
            db.database = await get_fallback_database()
            db.client = None
            db.is_fallback = True
            
            logger.info("[OK] Connected to SQLite fallback database successfully")
            logger.info("[NOTE] Using SQLite for development. Data will be stored locally.")
            
        except Exception as fallback_error:
            logger.error(f"[ERR] Fallback database connection also failed: {fallback_error}")
            raise fallback_error

async def close_mongo_connection():
    """Close database connection"""
    if db.is_fallback:
        if db.database:
            await db.database.close()
            logger.info("[OK] SQLite connection closed")
    else:
        if db.client:
            db.client.close()
            logger.info("[OK] MongoDB connection closed")

async def create_indexes():
    """Create database indexes for optimal performance"""
    try:
        if db.is_fallback:
            # SQLite indexes are created during table creation
            logger.info("[OK] SQLite indexes already created")
            return
        
        # MongoDB indexes
        await db.database.certificates.create_index("user_id")
        await db.database.certificates.create_index("batch_id")
        await db.database.certificates.create_index([("user_id", 1), ("upload_timestamp", -1)])
        await db.database.certificates.create_index([("verification_status", 1), ("trust_score", -1)])
        
        # Users collection indexes
        await db.database.users.create_index("email", unique=True)
        await db.database.users.create_index("institution_id")
        
        # Verification results indexes
        await db.database.verification_results.create_index("certificate_id")
        await db.database.verification_results.create_index("verification_timestamp")
        
        # Duplicate detection indexes
        await db.database.duplicate_detections.create_index("certificate_id")
        await db.database.duplicate_detections.create_index("hash_matches")
        
        # Batch uploads indexes
        await db.database.batch_uploads.create_index("user_id")
        await db.database.batch_uploads.create_index("start_time")
        
        logger.info("[OK] Database indexes created successfully")
        
    except Exception as e:
        logger.error(f"[ERR] Error creating indexes: {e}")

def get_database():
    """Get database instance"""
    return db.database

def is_using_fallback():
    """Check if using fallback database"""
    return db.is_fallback