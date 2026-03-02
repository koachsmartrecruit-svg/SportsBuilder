import os
import re
from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from jinja2 import ChoiceLoader, FileSystemLoader
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Website, Gallery

# ── App Config ──────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///sportsbuilder.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Allow rendering public site templates stored outside the default `templates/` directory.
app.jinja_loader = ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader(os.path.join(app.root_path, "builder_templates")),
])


# ── Helpers ──────────────────────────────────────────────────────────────────
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text


def save_upload(file):
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Make unique
        base, ext = os.path.splitext(filename)
        import uuid
        filename = f"{base}_{uuid.uuid4().hex[:8]}{ext}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        return f"uploads/{filename}"
    return None


def delete_upload_if_unused(rel_path):
    if not rel_path or not isinstance(rel_path, str):
        return
    if not rel_path.startswith("uploads/"):
        return

    used_by_hero = Website.query.filter_by(hero_image=rel_path).count()
    used_by_gallery = Gallery.query.filter_by(image_path=rel_path).count()
    if used_by_hero + used_by_gallery > 1:
        return

    abs_path = os.path.join(app.root_path, "static", rel_path)
    try:
        if os.path.exists(abs_path):
            os.remove(abs_path)
    except OSError:
        pass


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


TEMPLATES = {
    "academy_template": {"label": "Sports Academy", "icon": "🏆", "desc": "Perfect for academies & clubs"},
    "gym_template":     {"label": "Gym & Fitness",  "icon": "💪", "desc": "Ideal for gyms & fitness studios"},
    "tournament_template": {"label": "Tournament",  "icon": "🥇", "desc": "Built for tournaments & leagues"},
    "coach_template":   {"label": "Coaching Platform", "icon": "🚀", "desc": "Modern platform for coaches & recruiters"},
}


# ── Auth Routes ───────────────────────────────────────────────────────────────
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if not email or not password:
            flash("Email and password are required.", "error")
        elif password != confirm:
            flash("Passwords do not match.", "error")
        elif len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
        elif User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
        else:
            user = User(email=email, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Welcome! Your account has been created.", "success")
            return redirect(url_for("dashboard"))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=request.form.get("remember"))
            flash("Welcome back!", "success")
            return redirect(request.args.get("next") or url_for("dashboard"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ── Dashboard ─────────────────────────────────────────────────────────────────
@app.route("/dashboard")
@login_required
def dashboard():
    sites = Website.query.filter_by(user_id=current_user.id).order_by(Website.created_at.desc()).all()
    return render_template("dashboard.html", sites=sites, templates=TEMPLATES)


# ── Create Site ───────────────────────────────────────────────────────────────
@app.route("/create-site", methods=["GET", "POST"])
@login_required
def create_site():
    if request.method == "POST":
        site_name = request.form.get("site_name", "").strip()
        template_name = request.form.get("template_name", "academy_template")
        
        if not site_name:
            flash("Site name is required.", "error")
            return render_template("create_site.html", templates=TEMPLATES)

        # Build unique slug
        base_slug = slugify(site_name)
        slug = base_slug
        counter = 1
        while Website.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        # Handle image uploads
        hero_image = save_upload(request.files.get("hero_image")) if "hero_image" in request.files else None
        logo = save_upload(request.files.get("logo")) if "logo" in request.files else None

        site = Website(
            user_id=current_user.id,
            site_name=site_name,
            slug=slug,
            template_name=template_name,
            
            # Colors
            primary_color=request.form.get("primary_color", "#e63946"),
            secondary_color=request.form.get("secondary_color", "#1d3557"),
            accent_color=request.form.get("accent_color", "#f59e0b"),
            background_color=request.form.get("background_color", "#ffffff"),
            text_color=request.form.get("text_color", "#1a1a2e"),
            
            # Typography
            font_family=request.form.get("font_family", "Inter"),
            
            # Images
            logo=logo,
            hero_image=hero_image,
            
            # Content
            description=request.form.get("description", "").strip(),
            tagline=request.form.get("tagline", "").strip(),
            hero_title=request.form.get("hero_title", "").strip(),
            hero_subtitle=request.form.get("hero_subtitle", "").strip(),
            cta_button_text=request.form.get("cta_button_text", "Get Started"),
            cta_button_url=request.form.get("cta_button_url", "#contact"),
            
            # About
            about_title=request.form.get("about_title", "About Us"),
            about_text=request.form.get("about_text", "").strip(),
            
            # Features
            feature1_title=request.form.get("feature1_title", "").strip(),
            feature1_text=request.form.get("feature1_text", "").strip(),
            feature1_icon=request.form.get("feature1_icon", "🎯"),
            feature2_title=request.form.get("feature2_title", "").strip(),
            feature2_text=request.form.get("feature2_text", "").strip(),
            feature2_icon=request.form.get("feature2_icon", "⚡"),
            feature3_title=request.form.get("feature3_title", "").strip(),
            feature3_text=request.form.get("feature3_text", "").strip(),
            feature3_icon=request.form.get("feature3_icon", "🏆"),
            feature4_title=request.form.get("feature4_title", "").strip(),
            feature4_text=request.form.get("feature4_text", "").strip(),
            feature4_icon=request.form.get("feature4_icon", "💪"),
            
            # Stats
            stat1_number=request.form.get("stat1_number", "").strip(),
            stat1_label=request.form.get("stat1_label", "").strip(),
            stat2_number=request.form.get("stat2_number", "").strip(),
            stat2_label=request.form.get("stat2_label", "").strip(),
            stat3_number=request.form.get("stat3_number", "").strip(),
            stat3_label=request.form.get("stat3_label", "").strip(),
            stat4_number=request.form.get("stat4_number", "").strip(),
            stat4_label=request.form.get("stat4_label", "").strip(),
            
            # Contact
            contact_email=request.form.get("contact_email", "").strip(),
            phone=request.form.get("phone", "").strip(),
            address=request.form.get("address", "").strip(),
            whatsapp=request.form.get("whatsapp", "").strip(),
            
            # Social
            facebook=request.form.get("facebook", "").strip(),
            instagram=request.form.get("instagram", "").strip(),
            twitter=request.form.get("twitter", "").strip(),
            linkedin=request.form.get("linkedin", "").strip(),
            youtube=request.form.get("youtube", "").strip(),
            
            # Settings
            is_published=request.form.get("is_published", "on") == "on",
            show_gallery=request.form.get("show_gallery", "on") == "on",
            show_stats=request.form.get("show_stats", "on") == "on",
            show_features=request.form.get("show_features", "on") == "on",
        )
        db.session.add(site)
        db.session.flush()  # Get site.id

        # Handle gallery images
        if "gallery_images" in request.files:
            for gfile in request.files.getlist("gallery_images"):
                path = save_upload(gfile)
                if path:
                    db.session.add(Gallery(website_id=site.id, image_path=path))

        db.session.commit()
        flash(f'Site "{site_name}" created successfully!', "success")
        return redirect(url_for("dashboard"))

    return render_template("create_site.html", templates=TEMPLATES)


# ── Edit Site ─────────────────────────────────────────────────────────────────
@app.route("/edit-site/<int:site_id>", methods=["GET", "POST"])
@login_required
def edit_site(site_id):
    site = Website.query.filter_by(id=site_id, user_id=current_user.id).first_or_404()

    if request.method == "POST":
        to_delete = []
        
        # Basic info
        site.site_name = request.form.get("site_name", site.site_name).strip()
        site.template_name = request.form.get("template_name", site.template_name)
        
        # Colors
        site.primary_color = request.form.get("primary_color", site.primary_color)
        site.secondary_color = request.form.get("secondary_color", site.secondary_color)
        site.accent_color = request.form.get("accent_color", site.accent_color)
        site.background_color = request.form.get("background_color", site.background_color)
        site.text_color = request.form.get("text_color", site.text_color)
        
        # Typography
        site.font_family = request.form.get("font_family", site.font_family)
        
        # Content
        site.description = request.form.get("description", "").strip()
        site.tagline = request.form.get("tagline", "").strip()
        site.hero_title = request.form.get("hero_title", "").strip()
        site.hero_subtitle = request.form.get("hero_subtitle", "").strip()
        site.cta_button_text = request.form.get("cta_button_text", site.cta_button_text)
        site.cta_button_url = request.form.get("cta_button_url", site.cta_button_url)
        
        # About
        site.about_title = request.form.get("about_title", site.about_title)
        site.about_text = request.form.get("about_text", "").strip()
        
        # Features
        site.feature1_title = request.form.get("feature1_title", "").strip()
        site.feature1_text = request.form.get("feature1_text", "").strip()
        site.feature1_icon = request.form.get("feature1_icon", site.feature1_icon)
        site.feature2_title = request.form.get("feature2_title", "").strip()
        site.feature2_text = request.form.get("feature2_text", "").strip()
        site.feature2_icon = request.form.get("feature2_icon", site.feature2_icon)
        site.feature3_title = request.form.get("feature3_title", "").strip()
        site.feature3_text = request.form.get("feature3_text", "").strip()
        site.feature3_icon = request.form.get("feature3_icon", site.feature3_icon)
        site.feature4_title = request.form.get("feature4_title", "").strip()
        site.feature4_text = request.form.get("feature4_text", "").strip()
        site.feature4_icon = request.form.get("feature4_icon", site.feature4_icon)
        
        # Stats
        site.stat1_number = request.form.get("stat1_number", "").strip()
        site.stat1_label = request.form.get("stat1_label", "").strip()
        site.stat2_number = request.form.get("stat2_number", "").strip()
        site.stat2_label = request.form.get("stat2_label", "").strip()
        site.stat3_number = request.form.get("stat3_number", "").strip()
        site.stat3_label = request.form.get("stat3_label", "").strip()
        site.stat4_number = request.form.get("stat4_number", "").strip()
        site.stat4_label = request.form.get("stat4_label", "").strip()
        
        # Contact
        site.contact_email = request.form.get("contact_email", "").strip()
        site.phone = request.form.get("phone", "").strip()
        site.address = request.form.get("address", "").strip()
        site.whatsapp = request.form.get("whatsapp", "").strip()
        
        # Social
        site.facebook = request.form.get("facebook", "").strip()
        site.instagram = request.form.get("instagram", "").strip()
        site.twitter = request.form.get("twitter", "").strip()
        site.linkedin = request.form.get("linkedin", "").strip()
        site.youtube = request.form.get("youtube", "").strip()
        
        # Settings
        site.is_published = request.form.get("is_published") == "on"
        site.show_gallery = request.form.get("show_gallery") == "on"
        site.show_stats = request.form.get("show_stats") == "on"
        site.show_features = request.form.get("show_features") == "on"

        # Handle logo removal
        if request.form.get("remove_logo") == "on" and site.logo:
            prev = site.logo
            site.logo = None
            to_delete.append(prev)

        # Handle logo upload
        if "logo" in request.files:
            path = save_upload(request.files["logo"])
            if path:
                prev = site.logo
                site.logo = path
                if prev:
                    to_delete.append(prev)

        # Handle hero image removal
        if request.form.get("remove_hero_image") == "on" and site.hero_image:
            prev = site.hero_image
            site.hero_image = None
            to_delete.append(prev)

        # Handle hero image upload
        if "hero_image" in request.files:
            path = save_upload(request.files["hero_image"])
            if path:
                prev = site.hero_image
                site.hero_image = path
                if prev:
                    to_delete.append(prev)

        # Handle gallery images
        if "gallery_images" in request.files:
            for gfile in request.files.getlist("gallery_images"):
                path = save_upload(gfile)
                if path:
                    db.session.add(Gallery(website_id=site.id, image_path=path))

        db.session.commit()
        flash("Site updated successfully!", "success")
        for prev in to_delete:
            delete_upload_if_unused(prev)
        return redirect(url_for("dashboard"))

    return render_template("edit_site.html", site=site, templates=TEMPLATES)


@app.route("/delete-site/<int:site_id>", methods=["POST"])
@login_required
def delete_site(site_id):
    site = Website.query.filter_by(id=site_id, user_id=current_user.id).first_or_404()
    hero = site.hero_image
    gallery_paths = [img.image_path for img in site.gallery]
    db.session.delete(site)
    db.session.commit()
    delete_upload_if_unused(hero)
    for path in gallery_paths:
        delete_upload_if_unused(path)
    flash("Site deleted.", "info")
    return redirect(url_for("dashboard"))


@app.route("/delete-gallery/<int:img_id>", methods=["POST"])
@login_required
def delete_gallery(img_id):
    img = Gallery.query.get_or_404(img_id)
    site = Website.query.get_or_404(img.website_id)
    if site.user_id != current_user.id:
        abort(403)
    path = img.image_path
    db.session.delete(img)
    db.session.commit()
    delete_upload_if_unused(path)
    return redirect(url_for("edit_site", site_id=site.id))


# ── Public Site Rendering ─────────────────────────────────────────────────────
@app.route("/site/<slug>")
def site(slug):
    website = Website.query.filter_by(slug=slug).first_or_404()
    if not website.is_published:
        abort(404)
    template_path = f"{website.template_name}/index.html"
    return render_template(template_path, site=website)


@app.route("/preview/<slug>")
@login_required
def preview(slug):
    website = Website.query.filter_by(slug=slug, user_id=current_user.id).first_or_404()
    template_path = f"{website.template_name}/index.html"
    return render_template(template_path, site=website)


# ── Init DB ───────────────────────────────────────────────────────────────────
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
