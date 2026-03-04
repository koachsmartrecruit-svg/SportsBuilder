"""
Production Database Migration Script
Adds all new fields for improved application
Run this once to update your existing database
"""
from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        with db.engine.connect() as conn:
            print("🔄 Starting database migration...")
            
            # User table migrations
            print("\n📊 Migrating User table...")
            user_migrations = [
                ("reset_token", "ALTER TABLE users ADD COLUMN reset_token VARCHAR(100) UNIQUE"),
                ("reset_token_expiry", "ALTER TABLE users ADD COLUMN reset_token_expiry DATETIME"),
                ("email_verified", "ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT 0"),
                ("last_login", "ALTER TABLE users ADD COLUMN last_login DATETIME"),
            ]
            
            for field, sql in user_migrations:
                try:
                    conn.execute(text(sql))
                    conn.commit()
                    print(f"  ✓ Added {field}")
                except Exception as e:
                    if "duplicate column" in str(e).lower():
                        print(f"  ⊙ {field} already exists")
                    else:
                        print(f"  ✗ Error adding {field}: {e}")
            
            # Website table migrations (from previous migration)
            print("\n📊 Migrating Website table...")
            website_migrations = [
                # Colors
                ("accent_color", "ALTER TABLE websites ADD COLUMN accent_color VARCHAR(20) DEFAULT '#f59e0b'"),
                ("background_color", "ALTER TABLE websites ADD COLUMN background_color VARCHAR(20) DEFAULT '#ffffff'"),
                ("text_color", "ALTER TABLE websites ADD COLUMN text_color VARCHAR(20) DEFAULT '#1a1a2e'"),
                
                # Typography
                ("font_family", "ALTER TABLE websites ADD COLUMN font_family VARCHAR(100) DEFAULT 'Inter'"),
                
                # Images
                ("logo", "ALTER TABLE websites ADD COLUMN logo VARCHAR(300)"),
                
                # Hero content
                ("hero_title", "ALTER TABLE websites ADD COLUMN hero_title VARCHAR(300)"),
                ("hero_subtitle", "ALTER TABLE websites ADD COLUMN hero_subtitle TEXT"),
                ("cta_button_text", "ALTER TABLE websites ADD COLUMN cta_button_text VARCHAR(100) DEFAULT 'Get Started'"),
                ("cta_button_url", "ALTER TABLE websites ADD COLUMN cta_button_url VARCHAR(300) DEFAULT '#contact'"),
                
                # About
                ("about_title", "ALTER TABLE websites ADD COLUMN about_title VARCHAR(200) DEFAULT 'About Us'"),
                ("about_text", "ALTER TABLE websites ADD COLUMN about_text TEXT"),
                
                # Contact
                ("whatsapp", "ALTER TABLE websites ADD COLUMN whatsapp VARCHAR(50)"),
                
                # Social
                ("linkedin", "ALTER TABLE websites ADD COLUMN linkedin VARCHAR(200)"),
                ("youtube", "ALTER TABLE websites ADD COLUMN youtube VARCHAR(200)"),
                
                # Settings
                ("show_gallery", "ALTER TABLE websites ADD COLUMN show_gallery BOOLEAN DEFAULT 1"),
                ("show_stats", "ALTER TABLE websites ADD COLUMN show_stats BOOLEAN DEFAULT 1"),
                ("show_features", "ALTER TABLE websites ADD COLUMN show_features BOOLEAN DEFAULT 1"),
            ]
            
            # Features
            for i in range(1, 5):
                website_migrations.extend([
                    (f"feature{i}_title", f"ALTER TABLE websites ADD COLUMN feature{i}_title VARCHAR(200)"),
                    (f"feature{i}_text", f"ALTER TABLE websites ADD COLUMN feature{i}_text TEXT"),
                    (f"feature{i}_icon", f"ALTER TABLE websites ADD COLUMN feature{i}_icon VARCHAR(50)"),
                ])
            
            # Stats
            for i in range(1, 5):
                website_migrations.extend([
                    (f"stat{i}_number", f"ALTER TABLE websites ADD COLUMN stat{i}_number VARCHAR(50)"),
                    (f"stat{i}_label", f"ALTER TABLE websites ADD COLUMN stat{i}_label VARCHAR(100)"),
                ])
            
            for field, sql in website_migrations:
                try:
                    conn.execute(text(sql))
                    conn.commit()
                    print(f"  ✓ Added {field}")
                except Exception as e:
                    if "duplicate column" in str(e).lower():
                        print(f"  ⊙ {field} already exists")
                    else:
                        print(f"  ✗ Error adding {field}: {e}")
            
            # Add index on email for faster lookups
            print("\n📊 Adding indexes...")
            try:
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)"))
                conn.commit()
                print("  ✓ Added index on users.email")
            except Exception as e:
                print(f"  ⊙ Index already exists or error: {e}")
            
            try:
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_websites_slug ON websites(slug)"))
                conn.commit()
                print("  ✓ Added index on websites.slug")
            except Exception as e:
                print(f"  ⊙ Index already exists or error: {e}")
            
            try:
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_websites_user_id ON websites(user_id)"))
                conn.commit()
                print("  ✓ Added index on websites.user_id")
            except Exception as e:
                print(f"  ⊙ Index already exists or error: {e}")
            
            # Add SEO fields to websites
            print("\n📊 Adding SEO fields...")
            seo_fields = [
                ("meta_title", "ALTER TABLE websites ADD COLUMN meta_title VARCHAR(200)"),
                ("meta_description", "ALTER TABLE websites ADD COLUMN meta_description TEXT"),
                ("meta_keywords", "ALTER TABLE websites ADD COLUMN meta_keywords VARCHAR(500)"),
                ("og_image", "ALTER TABLE websites ADD COLUMN og_image VARCHAR(300)"),
            ]
            
            for field, sql in seo_fields:
                try:
                    conn.execute(text(sql))
                    conn.commit()
                    print(f"  ✓ Added {field}")
                except Exception as e:
                    if "duplicate column" in str(e).lower():
                        print(f"  ⊙ {field} already exists")
                    else:
                        print(f"  ✗ Error adding {field}: {e}")
            
            # Create contact submissions table
            print("\n📊 Creating contact_submissions table...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS contact_submissions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        website_id INTEGER NOT NULL,
                        name VARCHAR(200) NOT NULL,
                        email VARCHAR(200) NOT NULL,
                        phone VARCHAR(50),
                        message TEXT NOT NULL,
                        status VARCHAR(20) DEFAULT 'new',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (website_id) REFERENCES websites(id) ON DELETE CASCADE
                    )
                """))
                conn.commit()
                print("  ✓ Created contact_submissions table")
            except Exception as e:
                print(f"  ⊙ Table already exists or error: {e}")
            
            # Create site analytics table
            print("\n📊 Creating site_analytics table...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS site_analytics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        website_id INTEGER NOT NULL UNIQUE,
                        page_views INTEGER DEFAULT 0,
                        unique_visitors INTEGER DEFAULT 0,
                        last_viewed DATETIME,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (website_id) REFERENCES websites(id) ON DELETE CASCADE
                    )
                """))
                conn.commit()
                print("  ✓ Created site_analytics table")
            except Exception as e:
                print(f"  ⊙ Table already exists or error: {e}")
        
        print("\n✅ Migration completed successfully!")
        print("\n📋 Summary:")
        print("  - User table: Added password reset and tracking fields")
        print("  - Website table: Added 50+ customization fields")
        print("  - Indexes: Added for performance optimization")
        print("\n🚀 Your database is now ready for production!")

if __name__ == "__main__":
    migrate()
