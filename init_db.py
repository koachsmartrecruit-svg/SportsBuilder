"""
Database initialization script for production deployment
Run this after first deployment to create all tables
"""
from app import app, db

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Print table info
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\n📊 Created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")

if __name__ == "__main__":
    init_database()
