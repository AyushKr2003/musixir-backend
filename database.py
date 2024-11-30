from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# PostgreSQL Database URL Format:
# postgresql://<username>:<password>@<host>:<port>/<database_name>
# Note: Special characters in password must be URL encoded
# Example: @ becomes %40, # becomes %23, etc.
"""
Database Configuration:

Currently using SQLite for:
- Local development and testing
- Simplified setup with no need for external database server
- Self-contained database file (musicapp.db)

To switch to PostgreSQL (for production/deployment):
1. Install psycopg2 package: pip install psycopg2-binary
2. Change DATABASE_URL to PostgreSQL format:
   DATABASE_URL = "postgresql://username:password@host:port/dbname"
   Example: 
   DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/musicapp"
3. Remove the connect_args parameter from create_engine()
4. Ensure PostgreSQL server is running and database is created

Note: For production, store credentials in environment variables:
   DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./musicapp.db')
"""

load_dotenv()

# Get database credentials from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construct database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# DATABASE_URL = "sqlite:///./musicapp.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# DATABASE_URL = "postgresql://postgres:Ayush%40@localhost:5432/musicapp" # "postgresql://username:password@host:port/dbname"





# Create engine
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""
This function uses FastAPI's dependency injection system to manage database sessions.
Instead of directly importing and using the database session in routes:
1. It ensures proper session handling (auto-closing) even if errors occur
2. Makes testing easier as we can replace the database session with a mock
3. Prevents sharing database connections between requests, which could cause issues
4. Follows dependency injection best practices for better code maintainability
"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()