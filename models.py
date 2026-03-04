from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    reset_token = db.Column(db.String(100), unique=True)
    reset_token_expiry = db.Column(db.DateTime)
    email_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    websites = db.relationship("Website", backref="owner", lazy=True, cascade="all, delete-orphan")
    
    def generate_reset_token(self):
        """Generate a secure password reset token"""
        self.reset_token = secrets.token_urlsafe(32)
        from datetime import timedelta
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token
    
    def verify_reset_token(self, token):
        """Verify if reset token is valid and not expired"""
        if not self.reset_token or self.reset_token != token:
            return False
        if not self.reset_token_expiry or datetime.utcnow() > self.reset_token_expiry:
            return False
        return True
    
    def clear_reset_token(self):
        """Clear reset token after use"""
        self.reset_token = None
        self.reset_token_expiry = None

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
    
    # SEO
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.Text)
    meta_keywords = db.Column(db.String(500))
    og_image = db.Column(db.String(300))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    gallery = db.relationship("Gallery", backref="website", lazy=True, cascade="all, delete-orphan")

class Gallery(db.Model):
    __tablename__ = "gallery"
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, db.ForeignKey("websites.id"), nullable=False)
    image_path = db.Column(db.String(300), nullable=False)
    caption = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ContactSubmission(db.Model):
    __tablename__ = "contact_submissions"
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, db.ForeignKey("websites.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="new")  # new, read, replied, archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    website = db.relationship("Website", backref=db.backref("submissions", lazy=True, cascade="all, delete-orphan"))


class SiteAnalytics(db.Model):
    __tablename__ = "site_analytics"
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, db.ForeignKey("websites.id"), nullable=False)
    page_views = db.Column(db.Integer, default=0)
    unique_visitors = db.Column(db.Integer, default=0)
    last_viewed = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    website = db.relationship("Website", backref=db.backref("analytics", uselist=False, cascade="all, delete-orphan"))