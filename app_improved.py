"""
SportsBuilder - Improved Production-Ready Application
Multi-tenant website builder for sports organizations
"""
import os
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config

# Import models and extensions
from models import db, User
from flask_login import LoginManager

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.environ.get("FLASK_ENV", "development")
app.config.from_object(config[env])

# Initialize extensions
db.init_app(app)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config["RATELIMIT_STORAGE_URL"]
)

# Login manager
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Security headers (production only)
if env == "production":
    from flask_talisman import Talisman
    Talisman(app, 
             force_https=True,
             strict_transport_security=True,
             content_security_policy=None)  # Customize as needed

# Template loader for builder templates
from jinja2 import ChoiceLoader, FileSystemLoader
app.jinja_loader = ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader(os.path.join(app.root_path, "builder_templates")),
])

# Create upload folder
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Import routes (after app initialization)
from routes import auth, sites, api, errors

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(sites.bp)
app.register_blueprint(api.bp)
app.register_blueprint(errors.bp)

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=(env == "development"))
