#!/usr/bin/env python3
"""
Clear all data from the database
"""

import sqlite3
import os

def clear_database():
    """Clear all data from SQLite database"""
    db_path = 'certificate_verification.db'
    
    if os.path.exists(db_path):
        print('🗑️ Deleting all data from database...')
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        # Delete all data from each table
        for (table_name,) in tables:
            cursor.execute(f'DELETE FROM {table_name}')
            print(f'   ✅ Cleared table: {table_name}')
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print('✅ All data deleted successfully!')
        print('📊 Database is now empty and ready for new accounts.')
    else:
        print('ℹ️ Database file does not exist yet.')

if __name__ == "__main__":
    clear_database()