from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    websites = db.relationship("Website", backref="owner", lazy=True, cascade="all, delete-orphan")

class Website(db.Model):
    __tablename__ = "websites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    site_name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    template_name = db.Column(db.String(100), nullable=False, default="academy_template")
    
    # Colors
    primary_color = db.Column(db.String(20), default="#e63946")
    secondary_color = db.Column(db.String(20), default="#1d3557")
    accent_color = db.Column(db.String(20), default="#f59e0b")
    background_color = db.Column(db.String(20), default="#ffffff")
    text_color = db.Column(db.String(20), default="#1a1a2e")
    
    # Typography
    font_family = db.Column(db.String(100), default="Inter")
    
    # Images
    logo = db.Column(db.String(300))
    hero_image = db.Column(db.String(300))
    
    # Content
    description = db.Column(db.Text)
    tagline = db.Column(db.String(300))
    hero_title = db.Column(db.String(300))
    hero_subtitle = db.Column(db.Text)
    cta_button_text = db.Column(db.String(100), default="Get Started")
    cta_button_url = db.Column(db.String(300), default="#contact")
    
    # About Section
    about_title = db.Column(db.String(200), default="About Us")
    about_text = db.Column(db.Text)
    
    # Features/Services
    feature1_title = db.Column(db.String(200))
    feature1_text = db.Column(db.Text)
    feature1_icon = db.Column(db.String(50))
    feature2_title = db.Column(db.String(200))
    feature2_text = db.Column(db.Text)
    feature2_icon = db.Column(db.String(50))
    feature3_title = db.Column(db.String(200))
    feature3_text = db.Column(db.Text)
    feature3_icon = db.Column(db.String(50))
    feature4_title = db.Column(db.String(200))
    feature4_text = db.Column(db.Text)
    feature4_icon = db.Column(db.String(50))
    
    # Stats
    stat1_number = db.Column(db.String(50))
    stat1_label = db.Column(db.String(100))
    stat2_number = db.Column(db.String(50))
    stat2_label = db.Column(db.String(100))
    stat3_number = db.Column(db.String(50))
    stat3_label = db.Column(db.String(100))
    stat4_number = db.Column(db.String(50))
    stat4_label = db.Column(db.String(100))
    
    # Contact
    contact_email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    address = db.Column(db.String(300))
    whatsapp = db.Column(db.String(50))
    
    # Social Media
    facebook = db.Column(db.String(200))
    instagram = db.Column(db.String(200))
    twitter = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))
    youtube = db.Column(db.String(200))
    
    # Settings
    is_published = db.Column(db.Boolean, default=True)
    show_gallery = db.Column(db.Boolean, default=True)
    show_stats = db.Column(db.Boolean, default=True)
    show_features = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    gallery = db.relationship("Gallery", backref="website", lazy=True, cascade="all, delete-orphan")

class Gallery(db.Model):
    __tablename__ = "gallery"
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, db.ForeignKey("websites.id"), nullable=False)
    image_path = db.Column(db.String(300), nullable=False)
    caption = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)