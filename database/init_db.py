#!/usr/bin/env python3
import sqlite3
import os
from pathlib import Path

class DatabaseInitializer:
    def __init__(self):
        # Ensure database directory exists
        self.db_dir = Path(__file__).parent
        self.db_dir.mkdir(exist_ok=True)
        
        # Database file path
        self.db_path = self.db_dir / "db.sqlite"
        
        # Schema file path
        self.schema_path = self.db_dir / "schema.sql"

    def init_database(self):
        """Initialize the database with the schema"""
        print(f"Initializing database at {self.db_path}")
        
        # Read schema file
        try:
            with open(self.schema_path, 'r') as f:
                schema = f.read()
        except FileNotFoundError:
            print("Error: schema.sql not found!")
            return False

        # Connect to database and create tables
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Execute schema
            cursor.executescript(schema)
            
            # Commit changes and close connection
            conn.commit()
            conn.close()
            
            print("Database initialized successfully!")
            return True
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        
    def reset_database(self):
        """Reset the database by removing it and reinitializing"""
        try:
            if self.db_path.exists():
                os.remove(self.db_path)
                print("Existing database removed.")
            return self.init_database()
        except Exception as e:
            print(f"Error resetting database: {e}")
            return False

def main():
    initializer = DatabaseInitializer()
    
    # Check if database already exists
    if initializer.db_path.exists():
        response = input("Database already exists. Do you want to reset it? (y/N): ")
        if response.lower() == 'y':
            success = initializer.reset_database()
        else:
            print("Database initialization cancelled.")
            success = True
    else:
        success = initializer.init_database()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
