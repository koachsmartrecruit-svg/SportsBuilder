"""
Database migration script to add new customization fields
Run this once to update your existing database
"""
from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        with db.engine.connect() as conn:
            # Add new color columns
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN accent_color VARCHAR(20) DEFAULT '#f59e0b'"))
                print("✓ Added accent_color column")
            except Exception as e:
                print(f"  accent_color: {e}")
            
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN background_color VARCHAR(20) DEFAULT '#ffffff'"))
                print("✓ Added background_color column")
            except Exception as e:
                print(f"  background_color: {e}")
            
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN text_color VARCHAR(20) DEFAULT '#1a1a2e'"))
                print("✓ Added text_color column")
            except Exception as e:
                print(f"  text_color: {e}")
            
            # Add typography
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN font_family VARCHAR(100) DEFAULT 'Inter'"))
                print("✓ Added font_family column")
            except Exception as e:
                print(f"  font_family: {e}")
            
            # Add logo
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN logo VARCHAR(300)"))
                print("✓ Added logo column")
            except Exception as e:
                print(f"  logo: {e}")
            
            # Add hero content
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN hero_title VARCHAR(300)"))
                print("✓ Added hero_title column")
            except Exception as e:
                print(f"  hero_title: {e}")
            
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN hero_subtitle TEXT"))
                print("✓ Added hero_subtitle column")
            except Exception as e:
                print(f"  hero_subtitle: {e}")
            
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN cta_button_text VARCHAR(100) DEFAULT 'Get Started'"))
                print("✓ Added cta_button_text column")
            except Exception as e:
                print(f"  cta_button_text: {e}")
            
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN cta_button_url VARCHAR(300) DEFAULT '#contact'"))
                print("✓ Added cta_button_url column")
            except Exception as e:
                print(f"  cta_button_url: {e}")
            
            # Add about section
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN about_title VARCHAR(200) DEFAULT 'About Us'"))
                print("✓ Added about_title column")
            except Exception as e:
                print(f"  about_title: {e}")
            
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN about_text TEXT"))
                print("✓ Added about_text column")
            except Exception as e:
                print(f"  about_text: {e}")
            
            # Add features
            for i in range(1, 5):
                try:
                    conn.execute(text(f"ALTER TABLE websites ADD COLUMN feature{i}_title VARCHAR(200)"))
                    print(f"✓ Added feature{i}_title column")
                except Exception as e:
                    print(f"  feature{i}_title: {e}")
                
                try:
                    conn.execute(text(f"ALTER TABLE websites ADD COLUMN feature{i}_text TEXT"))
                    print(f"✓ Added feature{i}_text column")
                except Exception as e:
                    print(f"  feature{i}_text: {e}")
                
                try:
                    conn.execute(text(f"ALTER TABLE websites ADD COLUMN feature{i}_icon VARCHAR(50)"))
                    print(f"✓ Added feature{i}_icon column")
                except Exception as e:
                    print(f"  feature{i}_icon: {e}")
            
            # Add stats
            for i in range(1, 5):
                try:
                    conn.execute(text(f"ALTER TABLE websites ADD COLUMN stat{i}_number VARCHAR(50)"))
                    print(f"✓ Added stat{i}_number column")
                except Exception as e:
                    print(f"  stat{i}_number: {e}")
                
                try:
                    conn.execute(text(f"ALTER TABLE websites ADD COLUMN stat{i}_label VARCHAR(100)"))
                    print(f"✓ Added stat{i}_label column")
                except Exception as e:
                    print(f"  stat{i}_label: {e}")
            
            # Add contact fields
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN whatsapp VARCHAR(50)"))
                print("✓ Added whatsapp column")
            except Exception as e:
                print(f"  whatsapp: {e}")
            
            # Add social media
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN linkedin VARCHAR(200)"))
                print("✓ Added linkedin column")
            except Exception as e:
                print(f"  linkedin: {e}")
            
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN youtube VARCHAR(200)"))
                print("✓ Added youtube column")
            except Exception as e:
                print(f"  youtube: {e}")
            
            # Add settings
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN show_gallery BOOLEAN DEFAULT 1"))
                print("✓ Added show_gallery column")
            except Exception as e:
                print(f"  show_gallery: {e}")
            
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN show_stats BOOLEAN DEFAULT 1"))
                print("✓ Added show_stats column")
            except Exception as e:
                print(f"  show_stats: {e}")
            
            try:
                conn.execute(text("ALTER TABLE websites ADD COLUMN show_features BOOLEAN DEFAULT 1"))
                print("✓ Added show_features column")
            except Exception as e:
                print(f"  show_features: {e}")
            
            conn.commit()
        
        print("\n✅ Migration completed!")
        print("Your database now supports all the new customization options.")

if __name__ == "__main__":
    migrate()
