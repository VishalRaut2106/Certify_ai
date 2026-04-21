"""
Fallback database implementation using SQLite for development
when MongoDB Atlas is not accessible
"""

import sqlite3
import aiosqlite
import logging
from pathlib import Path
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

class SQLiteDatabase:
    def __init__(self, db_path: str = "certificate_verification.db"):
        self.db_path = db_path
        self.connection = None
    
    async def connect(self):
        """Initialize SQLite database with required tables"""
        try:
            # Create database directory if it doesn't exist
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Create tables
            async with aiosqlite.connect(self.db_path) as db:
                await self._create_tables(db)
                await db.commit()
            
            logger.info("[OK] Connected to SQLite database successfully")
            return True
            
        except Exception as e:
            logger.error(f"[ERR] Failed to connect to SQLite: {e}")
            return False
    
    async def _create_tables(self, db):
        """Create all required tables"""
        
        # Users table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                full_name TEXT,
                institution_name TEXT,
                institution_id TEXT,
                role TEXT DEFAULT 'teacher',
                permissions TEXT DEFAULT '[]',
                is_active BOOLEAN DEFAULT TRUE,
                is_verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                login_count INTEGER DEFAULT 0,
                certificates_uploaded INTEGER DEFAULT 0,
                verifications_performed INTEGER DEFAULT 0
            )
        """)
        
        # Certificates table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS certificates (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                batch_id TEXT,
                original_filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                verification_status TEXT DEFAULT 'pending',
                trust_score REAL,
                upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processing_time REAL,
                metadata TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Verification results table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS verification_results (
                id TEXT PRIMARY KEY,
                certificate_id TEXT NOT NULL,
                verification_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ocr_results TEXT,
                qr_results TEXT,
                template_match_results TEXT,
                fraud_indicators TEXT,
                trust_score REAL,
                verification_details TEXT,
                FOREIGN KEY (certificate_id) REFERENCES certificates (id)
            )
        """)
        
        # Batch uploads table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS batch_uploads (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                total_files INTEGER NOT NULL,
                processed_files INTEGER DEFAULT 0,
                failed_files INTEGER DEFAULT 0,
                status TEXT DEFAULT 'processing',
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Duplicate detections table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS duplicate_detections (
                id TEXT PRIMARY KEY,
                certificate_id TEXT NOT NULL,
                duplicate_certificate_id TEXT,
                similarity_score REAL,
                hash_matches TEXT,
                detection_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (certificate_id) REFERENCES certificates (id)
            )
        """)
        
        # Create indexes
        await db.execute("CREATE INDEX IF NOT EXISTS idx_certificates_user_id ON certificates (user_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_certificates_batch_id ON certificates (batch_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_certificates_status ON certificates (verification_status)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_verification_results_cert_id ON verification_results (certificate_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_batch_uploads_user_id ON batch_uploads (user_id)")
    
    async def close(self):
        """Close database connection"""
        if self.connection:
            await self.connection.close()
            logger.info("[OK] SQLite connection closed")

# Database adapter class to provide MongoDB-like interface
class DatabaseAdapter:
    def __init__(self, sqlite_db: SQLiteDatabase):
        self.sqlite_db = sqlite_db
        self.client = None
        self.database = self
    
    async def connect(self):
        return await self.sqlite_db.connect()
    
    async def close(self):
        return await self.sqlite_db.close()
    
    # Collection-like interfaces
    @property
    def users(self):
        return SQLiteCollection(self.sqlite_db, "users")
    
    @property
    def certificates(self):
        return SQLiteCollection(self.sqlite_db, "certificates")
    
    @property
    def verification_results(self):
        return SQLiteCollection(self.sqlite_db, "verification_results")
    
    @property
    def batch_uploads(self):
        return SQLiteCollection(self.sqlite_db, "batch_uploads")
    
    @property
    def duplicate_detections(self):
        return SQLiteCollection(self.sqlite_db, "duplicate_detections")

class SQLiteCollection:
    def __init__(self, sqlite_db: SQLiteDatabase, table_name: str):
        self.sqlite_db = sqlite_db
        self.table_name = table_name
    
    async def insert_one(self, document: Dict[str, Any]):
        """Insert a single document"""
        async with aiosqlite.connect(self.sqlite_db.db_path) as db:
            columns = list(document.keys())
            placeholders = ["?" for _ in columns]
            values = [json.dumps(v) if isinstance(v, (dict, list)) else v for v in document.values()]
            
            query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            await db.execute(query, values)
            await db.commit()
            return {"inserted_id": document.get("id")}
    
    async def find_one(self, filter_dict: Dict[str, Any] = None):
        """Find a single document"""
        async with aiosqlite.connect(self.sqlite_db.db_path) as db:
            if filter_dict:
                conditions = []
                values = []
                for key, value in filter_dict.items():
                    conditions.append(f"{key} = ?")
                    values.append(value)
                
                query = f"SELECT * FROM {self.table_name} WHERE {' AND '.join(conditions)} LIMIT 1"
                cursor = await db.execute(query, values)
            else:
                query = f"SELECT * FROM {self.table_name} LIMIT 1"
                cursor = await db.execute(query)
            
            row = await cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    
    async def find(self, filter_dict: Dict[str, Any] = None, limit: int = None, skip: int = None):
        """Find multiple documents"""
        async with aiosqlite.connect(self.sqlite_db.db_path) as db:
            query = f"SELECT * FROM {self.table_name}"
            values = []
            
            if filter_dict:
                conditions = []
                for key, value in filter_dict.items():
                    conditions.append(f"{key} = ?")
                    values.append(value)
                query += f" WHERE {' AND '.join(conditions)}"
            
            if skip:
                query += f" OFFSET {skip}"
            if limit:
                query += f" LIMIT {limit}"
            
            cursor = await db.execute(query, values)
            rows = await cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    async def update_one(self, filter_dict: Dict[str, Any], update_dict: Dict[str, Any]):
        """Update a single document"""
        async with aiosqlite.connect(self.sqlite_db.db_path) as db:
            # Handle $set operator
            if "$set" in update_dict:
                update_data = update_dict["$set"]
            else:
                update_data = update_dict
            
            set_clauses = []
            values = []
            for key, value in update_data.items():
                set_clauses.append(f"{key} = ?")
                values.append(json.dumps(value) if isinstance(value, (dict, list)) else value)
            
            conditions = []
            for key, value in filter_dict.items():
                conditions.append(f"{key} = ?")
                values.append(value)
            
            query = f"UPDATE {self.table_name} SET {', '.join(set_clauses)} WHERE {' AND '.join(conditions)}"
            await db.execute(query, values)
            await db.commit()
    
    async def delete_one(self, filter_dict: Dict[str, Any]):
        """Delete a single document"""
        async with aiosqlite.connect(self.sqlite_db.db_path) as db:
            conditions = []
            values = []
            for key, value in filter_dict.items():
                conditions.append(f"{key} = ?")
                values.append(value)
            
            query = f"DELETE FROM {self.table_name} WHERE {' AND '.join(conditions)}"
            await db.execute(query, values)
            await db.commit()
    
    async def count_documents(self, filter_dict: Dict[str, Any] = None):
        """Count documents"""
        async with aiosqlite.connect(self.sqlite_db.db_path) as db:
            query = f"SELECT COUNT(*) FROM {self.table_name}"
            values = []
            
            if filter_dict:
                conditions = []
                for key, value in filter_dict.items():
                    conditions.append(f"{key} = ?")
                    values.append(value)
                query += f" WHERE {' AND '.join(conditions)}"
            
            cursor = await db.execute(query, values)
            result = await cursor.fetchone()
            return result[0] if result else 0
    
    async def create_index(self, index_spec, **kwargs):
        """Create index (no-op for SQLite as indexes are created during table creation)"""
        pass

# Global database instance
fallback_db = None

async def get_fallback_database():
    """Get or create fallback database instance"""
    global fallback_db
    if fallback_db is None:
        sqlite_db = SQLiteDatabase()
        fallback_db = DatabaseAdapter(sqlite_db)
        await fallback_db.connect()
    return fallback_db